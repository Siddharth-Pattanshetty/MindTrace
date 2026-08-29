import logging
import os
from typing import List, Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger("mindtrace.concept_engine.graph")

class KnowledgeGraphService:
    def __init__(self):
        self.uri = getattr(settings, "NEO4J_URI", "bolt://localhost:7687")
        self.username = getattr(settings, "NEO4J_USERNAME", "neo4j")
        self.password = getattr(settings, "NEO4J_PASSWORD", "mindtrace_password")
        self.database = getattr(settings, "NEO4J_DATABASE", "neo4j")
        self._driver = None

    def _get_driver(self):
        if self._driver is None:
            try:
                from neo4j import GraphDatabase
                self._driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
                logger.info("Connected to Neo4j Knowledge Graph successfully.")
            except Exception as e:
                logger.warning(f"Neo4j connection unavailable: {e}. Falling back to in-memory graph knowledge.")
                self._driver = None
        return self._driver

    def get_concept_context(self, concept_name: str) -> Dict[str, Any]:
        """
        Retrieves hierarchy, prerequisites, and related concepts from Neo4j or fallback in-memory taxonomy.
        """
        driver = self._get_driver()
        if driver is not None:
            try:
                with driver.session(database=self.database) as session:
                    # Query hierarchy
                    hier_query = """
                    MATCH (s:Subject)-[:CONTAINS]->(d:Domain)-[:CONTAINS]->(t:Topic)-[:CONTAINS]->(st:Subtopic)-[:CONTAINS]->(c:Concept {name: $concept_name})
                    RETURN s.name as subject, d.name as domain, t.name as topic, st.name as subtopic, c.name as concept
                    """
                    hier_result = session.run(hier_query, concept_name=concept_name).single()
                    
                    hierarchy = []
                    if hier_result:
                        hierarchy = [
                            hier_result["subject"],
                            hier_result["domain"],
                            hier_result["topic"],
                            hier_result["subtopic"],
                            hier_result["concept"]
                        ]
                    else:
                        hierarchy = ["Mathematics", "Algebra", concept_name]

                    # Query prerequisites
                    prereq_query = """
                    MATCH (c:Concept {name: $concept_name})-[:REQUIRES|PREREQUISITE_OF]-(p:Concept)
                    RETURN DISTINCT p.name as prereq
                    """
                    prereq_result = session.run(prereq_query, concept_name=concept_name)
                    prerequisites = [record["prereq"] for record in prereq_result]

                    # Query related concepts
                    related_query = """
                    MATCH (c:Concept {name: $concept_name})-[:RELATED_TO]-(r:Concept)
                    RETURN DISTINCT r.name as related
                    """
                    related_result = session.run(related_query, concept_name=concept_name)
                    related_concepts = [record["related"] for record in related_result]

                    return {
                        "concept": concept_name,
                        "hierarchy": hierarchy,
                        "prerequisites": prerequisites,
                        "related_concepts": related_concepts
                    }
            except Exception as e:
                logger.warning(f"Error querying Neo4j for '{concept_name}': {e}. Using fallback taxonomy.")

        # Fallback taxonomy lookup
        return self._fallback_context(concept_name)

    def _fallback_context(self, concept_name: str) -> Dict[str, Any]:
        # Pre-defined taxonomy mapping for robust execution when Neo4j is offline
        taxonomy = {
            "Quadratic Factorization": {
                "hierarchy": ["Mathematics", "Algebra", "Polynomials", "Factorization", "Quadratic Factorization"],
                "prerequisites": ["Polynomial Operations", "Factor Pairs"],
                "related_concepts": ["Quadratic Equations"]
            },
            "Quadratic Equations": {
                "hierarchy": ["Mathematics", "Algebra", "Quadratic Equations", "Algebraic Methods", "Quadratic Equations"],
                "prerequisites": ["Linear Equations", "Polynomial Operations"],
                "related_concepts": ["Quadratic Factorization"]
            },
            "Linear Equations": {
                "hierarchy": ["Mathematics", "Algebra", "Linear Equations", "Single Variable Equations", "Linear Equations"],
                "prerequisites": ["Arithmetic"],
                "related_concepts": ["Quadratic Equations", "Coordinate Geometry"]
            },
            "Fractions": {
                "hierarchy": ["Mathematics", "Arithmetic", "Fractions", "Rational Operations", "Fractions"],
                "prerequisites": [],
                "related_concepts": ["Percentages", "Ratios"]
            },
            "Percentages": {
                "hierarchy": ["Mathematics", "Arithmetic", "Percentages", "Proportional Calculations", "Percentages"],
                "prerequisites": ["Fractions"],
                "related_concepts": ["Ratios"]
            },
            "Triangles": {
                "hierarchy": ["Mathematics", "Geometry", "Triangles", "Planar Geometry", "Triangles"],
                "prerequisites": [],
                "related_concepts": ["Circles", "Coordinate Geometry"]
            },
            "Circles": {
                "hierarchy": ["Mathematics", "Geometry", "Circles", "Planar Geometry", "Circles"],
                "prerequisites": [],
                "related_concepts": ["Triangles"]
            },
            "Mean": {
                "hierarchy": ["Mathematics", "Statistics", "Mean", "Central Tendency", "Mean"],
                "prerequisites": ["Fractions"],
                "related_concepts": ["Median", "Mode"]
            }
        }
        
        ctx = taxonomy.get(concept_name, {
            "hierarchy": ["Mathematics", "General", concept_name],
            "prerequisites": [],
            "related_concepts": []
        })
        return {
            "concept": concept_name,
            "hierarchy": ctx["hierarchy"],
            "prerequisites": ctx["prerequisites"],
            "related_concepts": ctx["related_concepts"]
        }

    def close(self):
        if self._driver:
            self._driver.close()
