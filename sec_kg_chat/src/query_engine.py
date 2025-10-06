import logging
import textwrap
from typing import Dict, Any, List, Optional
from .graph_manager import GraphManager
from .cypher_generator import CypherGenerator


class QueryEngine:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.graph_manager = GraphManager(config)
        self.cypher_generator = CypherGenerator(config, self.graph_manager)
        
        # Predefined queries for common patterns
        self.common_queries = {
            "investment_firms_city": self.graph_manager.get_investment_firms_by_city,
            "companies_city": self.graph_manager.get_companies_by_city,
            "company_description": self.graph_manager.get_company_description,
            "spatial_query": self.graph_manager.spatial_query
        }
    
    def process_query(self, question: str, use_llm: bool = True) -> Dict[str, Any]:
        """Process a natural language question."""
        try:
            if use_llm:
                return self._process_with_llm(question)
            else:
                return self._process_direct_query(question)
                
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return {
                "success": False,
                "question": question,
                "result": None,
                "error": str(e)
            }
    
    def _process_with_llm(self, question: str) -> Dict[str, Any]:
        """Process question using LLM for Cypher generation."""
        return self.cypher_generator.generate_and_execute(question)
    
    def _process_direct_query(self, question: str) -> Dict[str, Any]:
        """Process question using predefined query patterns."""
        question_lower = question.lower()
        
        try:
            if "investment firms" in question_lower and "near" in question_lower:
                # Extract city from question
                city = self._extract_city_from_question(question)
                if city:
                    result = self.graph_manager.spatial_query(city, entity_type="Manager")
                    return {
                        "success": True,
                        "question": question,
                        "result": result,
                        "error": None
                    }
            
            elif "investment firms" in question_lower and "in" in question_lower:
                city = self._extract_city_from_question(question)
                if city:
                    result = self.graph_manager.get_investment_firms_by_city(city)
                    return {
                        "success": True,
                        "question": question,
                        "result": result,
                        "error": None
                    }
            
            elif "companies" in question_lower and "in" in question_lower:
                city = self._extract_city_from_question(question)
                if city:
                    result = self.graph_manager.get_companies_by_city(city)
                    return {
                        "success": True,
                        "question": question,
                        "result": result,
                        "error": None
                    }
            
            elif "what does" in question_lower and "do" in question_lower:
                # Extract company name
                company_name = self._extract_company_from_question(question)
                if company_name:
                    result = self.graph_manager.get_company_description(company_name)
                    return {
                        "success": True,
                        "question": question,
                        "result": result,
                        "error": None
                    }
            
            # Fall back to LLM if no pattern matches
            return self._process_with_llm(question)
            
        except Exception as e:
            self.logger.error(f"Error in direct query processing: {e}")
            return self._process_with_llm(question)
    
    def _extract_city_from_question(self, question: str) -> Optional[str]:
        """Extract city name from question (simple implementation)."""
        # This is a simplified implementation
        # In production, you might want to use NER or more sophisticated parsing
        words = question.split()
        for i, word in enumerate(words):
            if word.lower() in ['in', 'near', 'at'] and i + 1 < len(words):
                return words[i + 1].strip('.,!?')
        return None
    
    def _extract_company_from_question(self, question: str) -> Optional[str]:
        """Extract company name from question."""
        # Simple extraction - in production, use more sophisticated methods
        if "what does" in question.lower():
            start = question.lower().find("what does") + 9
            end = question.lower().find("do", start)
            if end != -1:
                return question[start:end].strip()
        return None
    
    def format_result(self, result: Dict[str, Any], width: int = 80) -> str:
        """Format the query result for display."""
        if not result["success"]:
            return f"Error: {result['error']}"
        
        if not result["result"]:
            return "No results found."
        
        # Format based on result type
        if isinstance(result["result"], list):
            if len(result["result"]) == 0:
                return "No results found."
            
            formatted_lines = []
            for item in result["result"]:
                if isinstance(item, dict):
                    line = " | ".join(f"{k}: {v}" for k, v in item.items() if v is not None)
                    formatted_lines.append(textwrap.fill(line, width))
                else:
                    formatted_lines.append(textwrap.fill(str(item), width))
            
            return "\n\n".join(formatted_lines)
        else:
            return textwrap.fill(str(result["result"]), width)
    
    def health_check(self) -> Dict[str, Any]:
        """Perform system health check."""
        graph_healthy = self.graph_manager.health_check()
        
        # Test Cypher generation with a simple query
        cypher_test = self.process_query("What investment firms are in San Francisco?")
        cypher_healthy = cypher_test["success"]
        
        return {
            "graph_database": "healthy" if graph_healthy else "unhealthy",
            "cypher_generation": "healthy" if cypher_healthy else "unhealthy",
            "overall": "healthy" if (graph_healthy and cypher_healthy) else "unhealthy"
        }