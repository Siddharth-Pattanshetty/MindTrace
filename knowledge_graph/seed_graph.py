import json
import logging
import os
from pathlib import Path
from neo4j import GraphDatabase, Driver

logger = logging.getLogger("mindtrace.knowledge_graph.seeder")

def seed_database(driver: Driver, database: str = "neo4j", concepts_path: Path = None, relationships_path: Path = None):
    base_dir = Path(__file__).resolve().parent
    if concepts_path is None:
        concepts_path = base_dir / "concepts.json"
    if relationships_path is None:
        relationships_path = base_dir / "relationships.json"

    with open(concepts_path, "r", encoding="utf-8") as f:
        concepts_data = json.load(f)

    with open(relationships_path, "r", encoding="utf-8") as f:
        relationships_data = json.load(f)

    with driver.session(database=database) as session:
        # Create unique constraint on Concept name if possible
        try:
            session.run("CREATE CONSTRAINT concept_name_unique IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS UNIQUE")
            session.run("CREATE CONSTRAINT subject_name_unique IF NOT EXISTS FOR (s:Subject) REQUIRE s.name IS UNIQUE")
            session.run("CREATE CONSTRAINT domain_name_unique IF NOT EXISTS FOR (d:Domain) REQUIRE d.name IS UNIQUE")
            session.run("CREATE CONSTRAINT topic_name_unique IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE")
            session.run("CREATE CONSTRAINT errortype_name_unique IF NOT EXISTS FOR (e:ErrorType) REQUIRE e.name IS UNIQUE")
        except Exception as e:
            logger.warning(f"Constraint creation warning: {e}")

        # Seed Concepts and Hierarchy Nodes
        for item in concepts_data:
            c_name = item["name"]
            c_desc = item.get("description", "")
            subject = item.get("subject", "Mathematics")
            domain = item.get("domain", "Algebra")
            topic = item.get("topic", "Polynomials")
            subtopic = item.get("subtopic", "General")
            difficulty = item.get("difficulty", "intermediate")

            # Merge Subject, Domain, Topic, Subtopic, Concept idempotently
            cypher = """
            MERGE (s:Subject {name: $subject})
            MERGE (d:Domain {name: $domain})
            MERGE (t:Topic {name: $topic})
            MERGE (st:Subtopic {name: $subtopic})
            MERGE (c:Concept {name: $c_name})
            SET c.description = $c_desc,
                c.subject = $subject,
                c.domain = $domain,
                c.topic = $topic,
                c.subtopic = $subtopic,
                c.difficulty = $difficulty

            MERGE (s)-[:CONTAINS]->(d)
            MERGE (d)-[:CONTAINS]->(t)
            MERGE (t)-[:CONTAINS]->(st)
            MERGE (st)-[:CONTAINS]->(c)
            """
            session.run(cypher, subject=subject, domain=domain, topic=topic, subtopic=subtopic,
                        c_name=c_name, c_desc=c_desc, difficulty=difficulty)

        # Seed Relationships
        for rel in relationships_data:
            from_name = rel["from"]
            from_label = rel.get("from_label", "Concept")
            relationship = rel["relationship"]
            to_name = rel["to"]
            to_label = rel.get("to_label", "Concept")

            cypher_rel = f"""
            MERGE (a:{from_label} {{name: $from_name}})
            MERGE (b:{to_label} {{name: $to_name}})
            MERGE (a)-[r:{relationship}]->(b)
            """
            session.run(cypher_rel, from_name=from_name, to_name=to_name)

    logger.info("Knowledge Graph seeded successfully and idempotently.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "mindtrace_password")
    db = os.getenv("NEO4J_DATABASE", "neo4j")

    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        seed_database(driver, database=db)
        driver.close()
        print("Graph seeding complete.")
    except Exception as e:
        print(f"Graph seeding failed: {e}")
