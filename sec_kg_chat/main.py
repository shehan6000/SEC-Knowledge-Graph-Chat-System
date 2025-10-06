#!/usr/bin/env python3
"""
SEC Knowledge Graph Chat System - Main Entry Point
"""

import argparse
import sys
import logging
from src.config import ConfigManager
from src.query_engine import QueryEngine
from src.utils import setup_logging, validate_question


class SECChatApplication:
    def __init__(self, config_path: str = None):
        self.config_manager = ConfigManager(config_path)
        self.app_config = self.config_manager.get_app_config()
        
        # Setup logging
        self.logger = setup_logging(self.app_config.log_level, "sec_kg_chat.log")
        
        # Initialize query engine
        self.query_engine = QueryEngine(self.app_config)
        
        self.logger.info("SEC Knowledge Graph Chat System initialized")
    
    def run_interactive(self):
        """Run the application in interactive mode."""
        print("SEC Knowledge Graph Chat System")
        print("Type 'quit' or 'exit' to end the session")
        print("Type 'health' to check system status")
        print("-" * 50)
        
        while True:
            try:
                question = input("\nQuestion: ").strip()
                
                if question.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                if question.lower() == 'health':
                    health_status = self.query_engine.health_check()
                    print("\nSystem Health Check:")
                    for component, status in health_status.items():
                        print(f"  {component}: {status}")
                    continue
                
                if not question:
                    continue
                
                # Validate question
                is_valid, error_msg = validate_question(question)
                if not is_valid:
                    print(f"Invalid question: {error_msg}")
                    continue
                
                # Process question
                print("\nProcessing...")
                result = self.query_engine.process_query(question)
                formatted_result = self.query_engine.format_result(result)
                
                print(f"\nResult:\n{formatted_result}")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                print(f"An error occurred: {e}")
    
    def run_single_query(self, question: str):
        """Run a single query and return results."""
        is_valid, error_msg = validate_question(question)
        if not is_valid:
            print(f"Error: {error_msg}")
            return
        
        result = self.query_engine.process_query(question)
        formatted_result = self.query_engine.format_result(result)
        
        print(f"Question: {question}")
        print(f"Result:\n{formatted_result}")
        
        if not result["success"]:
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="SEC Knowledge Graph Chat System")
    parser.add_argument("--config", "-c", type=str, help="Path to config file")
    parser.add_argument("--question", "-q", type=str, help="Single question to process")
    parser.add_argument("--health", action="store_true", help="Run health check and exit")
    
    args = parser.parse_args()
    
    try:
        app = SECChatApplication(args.config)
        
        if args.health:
            health_status = app.query_engine.health_check()
            print("System Health Check:")
            for component, status in health_status.items():
                print(f"  {component}: {status}")
            sys.exit(0 if health_status["overall"] == "healthy" else 1)
        
        if args.question:
            app.run_single_query(args.question)
        else:
            app.run_interactive()
            
    except Exception as e:
        logging.error(f"Application failed to start: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()