import pytest
from unittest.mock import MagicMock
from knowledge_graph.seed_graph import seed_database

def test_knowledge_graph_fallback_queries():
    from app.ai.concept_engine.graph import KnowledgeGraphService
    kg_service = KnowledgeGraphService()
    ctx = kg_service.get_concept_context("Quadratic Factorization")
    assert ctx["concept"] == "Quadratic Factorization"
    assert "Polynomials" in ctx["hierarchy"] or "Algebra" in ctx["hierarchy"]
    assert len(ctx["prerequisites"]) > 0 or len(ctx["related_concepts"]) > 0

def test_seeding_script_idempotent(tmp_path):
    concepts_file = tmp_path / "concepts.json"
    relationships_file = tmp_path / "relationships.json"

    concepts_file.write_text('[{"name": "Quadratic Factorization", "description": "Test", "subject": "Math", "domain": "Algebra", "topic": "Polynomials", "subtopic": "Factorization", "difficulty": "intermediate"}]')
    relationships_file.write_text('[{"from": "Quadratic Factorization", "from_label": "Concept", "relationship": "REQUIRES", "to": "Factor Pairs", "to_label": "Concept"}]')

    mock_driver = MagicMock()
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session

    seed_database(mock_driver, database="neo4j", concepts_path=concepts_file, relationships_path=relationships_file)
    assert mock_session.run.called
