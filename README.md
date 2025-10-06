# SEC-Knowledge-Graph-Chat-System

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [Usage Guide](#usage-guide)
6. [API Reference](#api-reference)
7. [Query Examples](#query-examples)
8. [Development Guide](#development-guide)
9. [Troubleshooting](#troubleshooting)
10. [Monitoring & Logging](#monitoring--logging)

## Overview

The SEC Knowledge Graph Chat System is an intelligent query interface that allows users to interact with SEC (U.S. Securities and Exchange Commission) financial data through natural language. The system combines graph database technology with large language models to provide insightful answers about companies, investment firms, and financial relationships.

### Key Features

- **Natural Language Interface**: Ask questions in plain English
- **Graph Database Backend**: Powered by Neo4j for efficient relationship queries
- **LLM-Powered Cypher Generation**: Automatically converts questions to database queries
- **Spatial Queries**: Find entities based on geographic proximity
- **Full-Text Search**: Robust search across company and manager names
- **Form 10K Analysis**: Access detailed company descriptions from SEC filings
- **Production Ready**: Comprehensive error handling, logging, and monitoring

### Use Cases

- Financial analysts researching investment patterns
- Compliance officers monitoring regulatory requirements
- Researchers studying corporate relationships
- Investors analyzing market opportunities

## System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Interface │◄──►│   Query Engine   │◄──►│   Graph Manager  │
│   (CLI/API)     │    │                 │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                         │
                              │                         │
                              ▼                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Cypher Generator │    │   Configuration  │    │   Neo4j Database │
│    (LLM)        │    │     Manager      │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Data Flow

1. **User Input**: Natural language question received
2. **Query Processing**: Question analyzed and routed to appropriate handler
3. **Cypher Generation**: LLM converts question to Cypher query (if needed)
4. **Query Execution**: Cypher query executed against Neo4j database
5. **Result Processing**: Raw results formatted for display
6. **Response Delivery**: Formatted results returned to user

### Core Components

| Component | Purpose | Key Technologies |
|-----------|---------|------------------|
| **Query Engine** | Orchestrates query processing | Python, LangChain |
| **Graph Manager** | Database operations & connection management | Neo4j, LangChain |
| **Cypher Generator** | Natural language to Cypher translation | OpenAI GPT, LangChain |
| **Configuration Manager** | System configuration management | Python, YAML, dotenv |

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Neo4j Database (version 4.4+ recommended)
- OpenAI API access
- 4GB+ RAM recommended

### Step-by-Step Installation

#### 1. Clone and Setup Environment

```bash
# Create project directory
mkdir sec_kg_chat && cd sec_kg_chat

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Database Setup

Ensure Neo4j is running and accessible:

```bash
# Check Neo4j status (if installed locally)
neo4j status

# Or connect to remote instance
# Update connection details in environment variables
```

#### 3. Environment Configuration

Copy the example environment file and update with your values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_secure_password
NEO4J_DATABASE=neo4j

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4-turbo
OPENAI_TEMPERATURE=0

# Application Settings
LOG_LEVEL=INFO
```

#### 4. Verify Installation

```bash
# Run health check
python main.py --health

# Expected output:
# System Health Check:
#   graph_database: healthy
#   cypher_generation: healthy
#   overall: healthy
```

### Docker Deployment (Optional)

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

## Configuration

### Configuration Sources

The system supports multiple configuration sources with the following precedence:

1. **Command Line Arguments** (Highest priority)
2. **Environment Variables**
3. **Configuration File** (config.yaml)
4. **Default Values** (Lowest priority)

### Environment Variables

#### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEO4J_URI` | Neo4j database connection URI | `bolt://localhost:7687` |
| `NEO4J_USERNAME` | Neo4j username | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j password | `secure_password` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |

#### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEO4J_DATABASE` | `neo4j` | Neo4j database name |
| `OPENAI_MODEL` | `gpt-4-turbo` | LLM model to use |
| `OPENAI_TEMPERATURE` | `0` | LLM creativity setting |
| `OPENAI_BASE_URL` | OpenAI default | Custom API endpoint |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `VECTOR_INDEX_NAME` | `form_10k_chunks` | Vector index name |

### Configuration File

Create `config.yaml` for application-specific settings:

```yaml
# config.yaml
log_level: INFO

# Optional: Override default query limits
query_limits:
  default: 50
  full_text: 10
  spatial: 20
```

## Usage Guide

### Command Line Interface

#### Interactive Mode

```bash
python main.py

# Or with custom config
python main.py --config path/to/config.yaml
```

Example session:
```
SEC Knowledge Graph Chat System
Type 'quit' or 'exit' to end the session
Type 'health' to check system status
--------------------------------------------------

Question: What investment firms are in San Francisco?

Processing...

Result:
managerName: BLACKROCK ADVISORS LLC
managerName: VANGUARD GROUP INC
managerName: FIDELITY MANAGEMENT & RESEARCH CO
```

#### Single Query Mode

```bash
python main.py --question "What companies are in Santa Clara?"

# Output:
# Question: What companies are in Santa Clara?
# Result:
# companyName: NVIDIA CORP
# companyName: INTEL CORP
```

#### Health Check

```bash
python main.py --health

# Output:
# System Health Check:
#   graph_database: healthy
#   cypher_generation: healthy
#   overall: healthy
```

### Programmatic Usage

```python
from src.config import ConfigManager
from src.query_engine import QueryEngine

# Initialize system
config_manager = ConfigManager()
app_config = config_manager.get_app_config()
query_engine = QueryEngine(app_config)

# Execute query
result = query_engine.process_query("What investment firms are near Palo Alto?")
formatted_result = query_engine.format_result(result)

print(formatted_result)
```

### Query Patterns

The system understands several query patterns:

#### Location-Based Queries
- "What investment firms are in [city]?"
- "What companies are located in [city]?"
- "What investment firms are near [city]?"

#### Company Information
- "What does [company] do?"
- "Describe [company]'s business"

#### Analytical Queries
- "Which state has the most investment firms?"
- "What are the top investment firms in [city] by assets?"

#### Spatial Queries
- "What companies are near [landmark/company]?"
- "Find investment firms within [distance] of [location]"

## API Reference

### QueryEngine Class

Main interface for processing natural language queries.

#### Methods

##### `process_query(question: str, use_llm: bool = True) -> Dict[str, Any]`

Process a natural language question and return results.

**Parameters:**
- `question`: Natural language question
- `use_llm`: Whether to use LLM for Cypher generation (default: True)

**Returns:**
```python
{
    "success": bool,
    "question": str,
    "result": Any,  # Query results
    "error": Optional[str]  # Error message if failed
}
```

**Example:**
```python
result = query_engine.process_query("What investment firms are in Boston?")
if result["success"]:
    print(query_engine.format_result(result))
```

##### `format_result(result: Dict[str, Any], width: int = 80) -> str`

Format query results for display.

**Parameters:**
- `result`: Result dictionary from `process_query`
- `width`: Maximum line width for formatting

##### `health_check() -> Dict[str, str]`

Check system health status.

**Returns:**
```python
{
    "graph_database": "healthy" | "unhealthy",
    "cypher_generation": "healthy" | "unhealthy", 
    "overall": "healthy" | "unhealthy"
}
```

### GraphManager Class

Manages Neo4j database operations.

#### Key Methods

##### `execute_cypher(query: str, parameters: Optional[Dict] = None) -> List[Dict]`

Execute raw Cypher query with parameters.

**Example:**
```python
result = graph_manager.execute_cypher(
    "MATCH (c:Company) RETURN c.name LIMIT 10"
)
```

##### `full_text_search(index_name: str, query: str, limit: int = 10) -> List[Dict]`

Perform full-text search on specified index.

**Example:**
```python
results = graph_manager.full_text_search(
    "fullTextCompanyNames", 
    "Apple", 
    limit=5
)
```

##### `spatial_query(city: str, distance_meters: int = 10000, entity_type: str = "Manager") -> List[Dict]`

Find entities near a specified city.

**Example:**
```python
# Find managers within 10km of San Francisco
managers = graph_manager.spatial_query("San Francisco", 10000, "Manager")
```

##### `get_company_description(company_name: str) -> List[Dict]`

Retrieve company descriptions from Form 10K filings.

### CypherGenerator Class

Generates Cypher queries from natural language using LLM.

#### Methods

##### `generate_and_execute(question: str) -> Dict[str, Any]`

Generate and execute Cypher query for a question.

##### `update_template(new_template: str)`

Update the Cypher generation prompt template at runtime.

## Query Examples

### Basic Location Queries

```bash
# Find investment firms in a city
Question: What investment firms are in Boston?

# Find companies in a city  
Question: What companies are in Austin?

# Combined location query
Question: What investment firms and companies are in Chicago?
```

### Advanced Spatial Queries

```bash
# Find entities near a location
Question: What investment firms are near Santa Clara?

# Find companies near a specific company
Question: What companies are near Apple headquarters?

# Custom distance queries
Question: What investment firms are within 5km of San Francisco?
```

### Company Research

```bash
# Company descriptions
Question: What does Microsoft do?
Question: Describe Tesla's business

# Company relationships
Question: Who invests in Apple?
Question: What companies does BlackRock invest in?
```

### Analytical Queries

```bash
# Geographic analysis
Question: Which state has the most investment firms?
Question: What are the top cities for tech companies?

# Investment analysis
Question: What are the top investment firms in New York by assets?
Question: Which investment firms hold the most Tesla stock?
```

### Full-Text Search

```bash
# Fuzzy company search
Question: Find information about Palo Alto Networks
Question: Search for investment firms named "Capital"

# Partial name matching
Question: Find companies with "Bio" in the name
```

## Development Guide

### Project Structure

```
sec_kg_chat/
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── graph_manager.py    # Neo4j database operations
│   ├── cypher_generator.py # LLM-powered Cypher generation
│   ├── query_engine.py     # Main query processing logic
│   └── utils.py           # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_graph_manager.py
│   └── test_query_engine.py
├── requirements.txt
├── config.yaml
├── .env.example
└── main.py                # CLI entry point
```

### Adding New Query Patterns

#### 1. Update Cypher Generation Template

Modify the template in `cypher_generator.py`:

```python
def _get_cypher_generation_template(self) -> str:
    template = """
    # Existing examples...
    
    # New pattern: Find companies by industry
    # What tech companies are in California?
    CALL db.index.fulltext.queryNodes("fullTextCompanyNames", $industry) 
    YIELD node, score
    WITH node as com
    MATCH (com)-[:LOCATED_AT]->(addr:Address {state: $state})
    RETURN com.companyName
    """
    return template
```

#### 2. Add Direct Query Handler

Update `query_engine.py`:

```python
def _process_direct_query(self, question: str) -> Dict[str, Any]:
    question_lower = question.lower()
    
    # Existing patterns...
    
    # New pattern: Industry + location queries
    elif "companies" in question_lower and "in" in question_lower:
        industry = self._extract_industry(question)
        state = self._extract_state(question)
        if industry and state:
            return self._handle_industry_location_query(industry, state)
    
    # Fall back to LLM
    return self._process_with_llm(question)
```

### Customizing Cypher Generation

#### Modify Prompt Template

```python
# In cypher_generator.py
CUSTOM_TEMPLATE = """
# Add custom instructions or examples
# Use specific relationship patterns
# Include domain-specific knowledge

# Example: Add financial relationship queries
# How much Apple stock does Vanguard own?
MATCH (mgr:Manager {managerName: $manager_name})-[:OWNS_STOCK_IN]->
      (com:Company {companyName: $company_name})
RETURN mgr.managerName, com.companyName, owns.value as ownershipValue
"""

cypher_generator.update_template(CUSTOM_TEMPLATE)
```

### Testing

#### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_graph_manager.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

#### Writing New Tests

```python
# tests/test_new_feature.py
import unittest
from src.query_engine import QueryEngine

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.query_engine = QueryEngine(...)
    
    def test_industry_query(self):
        result = self.query_engine.process_query("What tech companies are in California?")
        self.assertTrue(result["success"])
        self.assertIsNotNone(result["result"])
```

## Troubleshooting

### Common Issues

#### Connection Problems

**Problem**: Cannot connect to Neo4j database
```
Error: Failed to initialize graph connections: Connection refused
```

**Solution**:
1. Verify Neo4j is running: `neo4j status`
2. Check connection details in `.env` file
3. Test connection: `cypher-shell -u neo4j -p password`

#### API Key Issues

**Problem**: OpenAI API authentication failed
```
Error: OpenAI API request failed: Invalid API key
```

**Solution**:
1. Verify `OPENAI_API_KEY` in `.env` file
2. Check API key validity in OpenAI dashboard
3. Ensure no extra spaces in the key

#### Query Performance

**Problem**: Slow query execution
```
Query took 30+ seconds to complete
```

**Solution**:
1. Add indexes on frequently queried properties
2. Use query parameters instead of string concatenation
3. Limit result sets with `LIMIT` clauses

### Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `Schema refresh failed` | Database connection issue | Check Neo4j status and credentials |
| `Cypher generation failed` | LLM API issue | Verify OpenAI API key and quota |
| `No results found` | Query didn't match data | Reformulate question or check data |
| `Invalid question format` | Input validation failed | Use proper question format |

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
# Set debug level
export LOG_LEVEL=DEBUG

# Run with verbose output
python main.py --question "Your question"
```

## Monitoring & Logging

### Log Files

The system creates detailed logs in `sec_kg_chat.log`:

```
2024-01-15 10:30:45 - src.graph_manager - INFO - Successfully initialized graph connection
2024-01-15 10:31:02 - src.query_engine - INFO - Processing question: What companies are in Boston?
2024-01-15 10:31:03 - src.cypher_generator - DEBUG - Generated Cypher: MATCH (c:Company)...
```

### Performance Monitoring

Key metrics to monitor:

- **Query Response Time**: Target < 5 seconds for most queries
- **LLM API Latency**: Monitor OpenAI response times
- **Database Connection Pool**: Watch for connection limits
- **Error Rates**: Track failed query percentage

### Health Check Endpoint

For production deployment, implement a health check endpoint:

```python
# In production, you might expose this as a REST endpoint
health_status = query_engine.health_check()
```

## Support & Resources

### Getting Help

- Check the troubleshooting section above
- Review application logs in `sec_kg_chat.log`
- Verify system health with `python main.py --health`

### Additional Resources

- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

### Contributing

When contributing to this project:

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Use meaningful commit messages
5. Test with multiple query types

---

This documentation provides comprehensive guidance for installing, configuring, using, and extending the SEC Knowledge Graph Chat System. For additional support or feature requests, please refer to the project's issue tracker or contact the development team.
