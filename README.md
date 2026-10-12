# SEC-Knowledge-Graph-Chat-System



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





### Additional Resources

- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)



---
