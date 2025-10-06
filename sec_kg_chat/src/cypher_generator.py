import logging
from typing import Dict, Any
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from .config import AppConfig


class CypherGenerator:
    def __init__(self, config: AppConfig, graph_manager):
        self.config = config
        self.graph_manager = graph_manager
        self.logger = logging.getLogger(__name__)
        self.cypher_chain = None
        self._initialize_cypher_chain()
    
    def _get_cypher_generation_template(self) -> str:
        """Return the Cypher generation template with examples."""
        return """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
Examples: Here are a few examples of generated Cypher statements for particular questions:

# What investment firms are in San Francisco?
MATCH (mgr:Manager)-[:LOCATED_AT]->(mgrAddress:Address)
    WHERE mgrAddress.city = 'San Francisco'
RETURN mgr.managerName

# What investment firms are near Santa Clara?
MATCH (address:Address)
    WHERE address.city = "Santa Clara"
MATCH (mgr:Manager)-[:LOCATED_AT]->(managerAddress:Address)
    WHERE point.distance(address.location, managerAddress.location) < 10000
RETURN mgr.managerName, mgr.managerAddress

# What companies are in Santa Clara?
MATCH (com:Company)-[:LOCATED_AT]->(address:Address)
    WHERE address.city = "Santa Clara"
RETURN com.companyName

# What does Palo Alto Networks do?
CALL db.index.fulltext.queryNodes("fullTextCompanyNames", "Palo Alto Networks") YIELD node, score
WITH node as com
MATCH (com)-[:FILED]->(f:Form),
    (f)-[s:SECTION]->(c:Chunk)
WHERE s.f10kItem = "item1"
RETURN c.text

# Which state has the most investment firms?
MATCH (mgr:Manager)-[:LOCATED_AT]->(address:Address)
RETURN address.state as state, count(address.state) as numManagers
ORDER BY numManagers DESC
LIMIT 10

The question is:
{question}"""
    
    def _initialize_cypher_chain(self):
        """Initialize the Cypher generation chain."""
        try:
            cypher_prompt = PromptTemplate(
                input_variables=["schema", "question"],
                template=self._get_cypher_generation_template()
            )
            
            llm = ChatOpenAI(
                model=self.config.openai.model,
                temperature=self.config.openai.temperature,
                openai_api_key=self.config.openai.api_key,
                openai_api_base=self.config.openai.base_url
            )
            
            self.cypher_chain = GraphCypherQAChain.from_llm(
                llm=llm,
                graph=self.graph_manager.graph,
                verbose=False,
                cypher_prompt=cypher_prompt,
                return_direct=True  # Return raw Cypher results
            )
            
            self.logger.info("Cypher generation chain initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Cypher chain: {e}")
            raise
    
    def generate_and_execute(self, question: str) -> Dict[str, Any]:
        """Generate Cypher query and execute it."""
        try:
            self.logger.info(f"Processing question: {question}")
            
            # Refresh schema to ensure it's up to date
            self.graph_manager.refresh_schema()
            
            # Generate and execute Cypher
            result = self.cypher_chain.run(question)
            
            return {
                "success": True,
                "question": question,
                "result": result,
                "error": None
            }
            
        except Exception as e:
            self.logger.error(f"Error generating/executing Cypher for question '{question}': {e}")
            return {
                "success": False,
                "question": question,
                "result": None,
                "error": str(e)
            }
    
    def update_template(self, new_template: str):
        """Update the Cypher generation template at runtime."""
        try:
            cypher_prompt = PromptTemplate(
                input_variables=["schema", "question"],
                template=new_template
            )
            
            llm = ChatOpenAI(
                model=self.config.openai.model,
                temperature=self.config.openai.temperature,
                openai_api_key=self.config.openai.api_key
            )
            
            self.cypher_chain = GraphCypherQAChain.from_llm(
                llm=llm,
                graph=self.graph_manager.graph,
                verbose=False,
                cypher_prompt=cypher_prompt,
                return_direct=True
            )
            
            self.logger.info("Cypher generation template updated successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to update Cypher template: {e}")
            raise