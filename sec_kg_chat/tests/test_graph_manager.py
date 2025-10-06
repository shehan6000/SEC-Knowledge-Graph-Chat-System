import unittest
from unittest.mock import Mock, patch
from src.config import ConfigManager
from src.graph_manager import GraphManager


class TestGraphManager(unittest.TestCase):
    def setUp(self):
        self.config = Mock()
        self.config.neo4j.uri = "bolt://localhost:7687"
        self.config.neo4j.username = "neo4j"
        self.config.neo4j.password = "password"
        self.config.neo4j.database = "neo4j"
        self.config.openai.api_key = "test-key"
        self.config.openai.base_url = None
    
    @patch('src.graph_manager.Neo4jGraph')
    @patch('src.graph_manager.Neo4jVector')
    def test_initialization(self, mock_vector, mock_graph):
        """Test graph manager initialization."""
        manager = GraphManager(self.config)
        self.assertIsNotNone(manager.graph)
        self.assertIsNotNone(manager.vector_store)
    
    # Add more tests as needed


if __name__ == '__main__':
    unittest.main()