import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
import yaml
from dotenv import load_dotenv


@dataclass
class Neo4jConfig:
    uri: str
    username: str
    password: str
    database: str = "neo4j"


@dataclass
class OpenAIConfig:
    api_key: str
    model: str = "gpt-4-turbo"
    temperature: float = 0
    base_url: Optional[str] = None


@dataclass
class VectorConfig:
    index_name: str = "form_10k_chunks"
    node_label: str = "Chunk"
    source_property: str = "text"
    embedding_property: str = "textEmbedding"


@dataclass
class AppConfig:
    neo4j: Neo4jConfig
    openai: OpenAIConfig
    vector: VectorConfig
    log_level: str = "INFO"


class ConfigManager:
    def __init__(self, config_path: Optional[str] = None, env_path: str = ".env"):
        # Load environment variables
        load_dotenv(env_path)
        
        # Load configuration from file if provided
        self.config_data = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as file:
                self.config_data = yaml.safe_load(file) or {}
        
        self._validate_required_vars()
    
    def _validate_required_vars(self):
        """Validate that required environment variables are set."""
        required_vars = ['NEO4J_URI', 'NEO4J_USERNAME', 'NEO4J_PASSWORD', 'OPENAI_API_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def get_neo4j_config(self) -> Neo4jConfig:
        return Neo4jConfig(
            uri=os.getenv('NEO4J_URI'),
            username=os.getenv('NEO4J_USERNAME'),
            password=os.getenv('NEO4J_PASSWORD'),
            database=os.getenv('NEO4J_DATABASE', 'neo4j')
        )
    
    def get_openai_config(self) -> OpenAIConfig:
        return OpenAIConfig(
            api_key=os.getenv('OPENAI_API_KEY'),
            model=os.getenv('OPENAI_MODEL', 'gpt-4-turbo'),
            temperature=float(os.getenv('OPENAI_TEMPERATURE', '0')),
            base_url=os.getenv('OPENAI_BASE_URL')
        )
    
    def get_vector_config(self) -> VectorConfig:
        return VectorConfig(
            index_name=os.getenv('VECTOR_INDEX_NAME', 'form_10k_chunks'),
            node_label=os.getenv('VECTOR_NODE_LABEL', 'Chunk'),
            source_property=os.getenv('VECTOR_SOURCE_PROPERTY', 'text'),
            embedding_property=os.getenv('VECTOR_EMBEDDING_PROPERTY', 'textEmbedding')
        )
    
    def get_app_config(self) -> AppConfig:
        return AppConfig(
            neo4j=self.get_neo4j_config(),
            openai=self.get_openai_config(),
            vector=self.get_vector_config(),
            log_level=os.getenv('LOG_LEVEL', 'INFO')
        )