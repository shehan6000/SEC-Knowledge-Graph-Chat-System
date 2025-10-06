import logging
from typing import List, Dict, Any, Optional
from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
from .config import AppConfig


class GraphManager:
    def __init__(self, config: AppConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.graph = None
        self.vector_store = None
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Initialize Neo4j graph and vector store connections."""
        try:
            # Initialize Neo4j graph connection
            self.graph = Neo4jGraph(
                url=self.config.neo4j.uri,
                username=self.config.neo4j.username,
                password=self.config.neo4j.password,
                database=self.config.neo4j.database
            )
            
            # Initialize embeddings
            embeddings = OpenAIEmbeddings(
                openai_api_key=self.config.openai.api_key,
                openai_api_base=self.config.openai.base_url
            )
            
            # Initialize vector store
            self.vector_store = Neo4jVector.from_existing_index(
                embedding=embeddings,
                index_name=self.config.vector.index_name,
                node_label=self.config.vector.node_label,
                text_node_property=self.config.vector.source_property,
                embedding_node_property=self.config.vector.embedding_property,
                url=self.config.neo4j.uri,
                username=self.config.neo4j.username,
                password=self.config.neo4j.password,
                database=self.config.neo4j.database
            )
            
            self.logger.info("Successfully initialized graph and vector store connections")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize graph connections: {e}")
            raise
    
    def refresh_schema(self) -> str:
        """Refresh and return the graph schema."""
        try:
            self.graph.refresh_schema()
            return self.graph.schema
        except Exception as e:
            self.logger.error(f"Error refreshing schema: {e}")
            raise
    
    def execute_cypher(self, query: str, parameters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Execute a Cypher query with error handling."""
        try:
            self.logger.debug(f"Executing Cypher query: {query}")
            result = self.graph.query(query, parameters=parameters or {})
            return result
        except Exception as e:
            self.logger.error(f"Cypher query execution failed: {e}")
            raise
    
    def full_text_search(self, index_name: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Perform full-text search on specified index."""
        cypher_query = f"""
        CALL db.index.fulltext.queryNodes($index_name, $query) 
        YIELD node, score
        RETURN node, score
        LIMIT $limit
        """
        return self.execute_cypher(cypher_query, {
            "index_name": index_name,
            "query": query,
            "limit": limit
        })
    
    def spatial_query(self, city: str, distance_meters: int = 10000, entity_type: str = "Manager") -> List[Dict[str, Any]]:
        """Perform spatial query to find entities near a city."""
        cypher_query = f"""
        MATCH (address:Address {{city: $city}})
        MATCH (entity:{entity_type})-[:LOCATED_AT]->(entityAddress:Address)
        WHERE point.distance(address.location, entityAddress.location) < $distance
        RETURN entity, point.distance(address.location, entityAddress.location) as distance
        ORDER BY distance
        """
        return self.execute_cypher(cypher_query, {
            "city": city,
            "distance": distance_meters
        })
    
    def get_companies_by_city(self, city: str) -> List[Dict[str, Any]]:
        """Get all companies in a specific city."""
        cypher_query = """
        MATCH (com:Company)-[:LOCATED_AT]->(address:Address)
        WHERE address.city = $city
        RETURN com.companyName
        """
        return self.execute_cypher(cypher_query, {"city": city})
    
    def get_investment_firms_by_city(self, city: str) -> List[Dict[str, Any]]:
        """Get investment firms in a specific city."""
        cypher_query = """
        MATCH (mgr:Manager)-[:LOCATED_AT]->(address:Address)
        WHERE address.city = $city
        RETURN mgr.managerName
        """
        return self.execute_cypher(cypher_query, {"city": city})
    
    def get_company_description(self, company_name: str) -> List[Dict[str, Any]]:
        """Get company description from Form 10K chunks."""
        cypher_query = """
        CALL db.index.fulltext.queryNodes("fullTextCompanyNames", $company_name) 
        YIELD node, score
        WITH node as com
        MATCH (com)-[:FILED]->(f:Form),
            (f)-[s:SECTION]->(c:Chunk)
        WHERE s.f10kItem = "item1"
        RETURN c.text
        LIMIT 5
        """
        return self.execute_cypher(cypher_query, {"company_name": company_name})
    
    def health_check(self) -> bool:
        """Check if the graph database is accessible."""
        try:
            self.graph.query("RETURN 1 as test")
            return True
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False