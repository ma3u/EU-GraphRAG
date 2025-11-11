# EU GraphRAG - AI Agent Instructions

## Project Overview
EU GraphRAG is a **developing** GraphRAG system for European Union regulations and German legal documents (SGB, BGB) built on Neo4j. The system implements ELI (European Legislation Identifier), ECLI (European Case Law Identifier), and EuroVoc ontologies for cross-border legal knowledge representation.

**Current State**: Early development - comprehensive documentation and schemas exist, source code implementation in progress.

## Critical Architecture Decisions

### Ontology-First Development Philosophy
**Always reference `ontologies/*.yaml` before creating nodes/properties**:
- `eli-core.yaml` - European Legislation Identifier (Work→Expression→Manifestation hierarchy)
- `ecli-core.yaml` - European Case Law Identifier (Country.Court.Year.Number.Decision)  
- `eurovoc-core.yaml` - EU multilingual thesaurus concepts
- `sgb-extension.yaml` - German Social Law Book domain model

### Graph Schema Constraints
Apply `ontologies/graph-schema.cypher` constraints FIRST:
```cypher
// Example: ELI URIs must be unique
CREATE CONSTRAINT eli_work_uri FOR (w:ELIWork) REQUIRE w.eli_uri IS UNIQUE;
```

### ELI URI Standardization
Use consistent ELI patterns: `eli:{jurisdiction}:{type}:{year}:{number}:{subdivision}`
- EU Directive: `eli:dir:2016:680`
- German Law: `eli:bund:sgbvi:2023:11:09:43` 
- Article: `eli:bund:sgbvi:2023:11:09:43:art:1`

## Development Environment

### Neo4j Setup (Required First Step)
```bash
# Start Neo4j with plugins
docker-compose up -d neo4j

# Initialize schema (wait for Neo4j startup)
cat ontologies/graph-schema.cypher | docker exec -i eu-graphrag-neo4j cypher-shell -u neo4j -p password
```
- Credentials: `neo4j/password`
- Browser: `http://localhost:7474` 
- Bolt: `bolt://localhost:7687`

### Python Environment Pattern
```bash
python3.11 -m venv venv
source venv/bin/activate  # WSL/Linux
pip install -r requirements.txt
```

## Project Structure Pattern

### Current State: Documentation-Heavy
```
ontologies/           # ✅ Complete - YAML schemas + Cypher
docs/                # ✅ GraphRAG-Concept.md (comprehensive spec)
src/                 # ❌ Not implemented yet
tests/               # ❌ Not implemented yet  
data/                # ✅ Directory structure only
```

### When Creating src/ modules:
- `src/graph/neo4j_client.py` - Neo4j connection management
- `src/ingestion/scrapers/` - gesetze-im-internet.de, EUR-Lex API
- `src/llm/prompt_templates.py` - Consistent entity extraction
- `src/retrieval/hybrid_retriever.py` - Vector + graph search

## Code Conventions

### Node Creation Pattern
Always validate ELI/ECLI format before insertion:
```python
# Required pattern for legal documents
result = session.run(
    "MATCH (a:Article {eli_uri: $uri}) RETURN a",
    uri="eli:bund:sgbvi:2023:11:09:43"  # Parameterized queries
)
```

### Multilingual Content Handling
- German laws: `title_de`, `text_de`
- EU legislation: `title@en`, `title@de`, `title@fr` (RDF-style)
- EuroVoc concepts: Support all 24 EU languages

## Key Integration Points

### GraphRAG Retrieval Pattern (Planned)
Hybrid approach combining:
1. **Vector Search**: Semantic similarity on article embeddings
2. **Graph Traversal**: Following `REFERENCES`, `SUPERSEDES`, `IMPLEMENTS` 
3. **Community Detection**: Neo4j GDS for concept clusters

### Multi-jurisdictional Tracking
```cypher
// EU-to-German law transposition analysis
MATCH (directive:EUDirective)-[:IMPLEMENTS]->(law:GermanLaw)
RETURN directive.eli_uri, law.title_de, law.transposition_deadline
```

### Temporal Versioning
```cypher
// Legal amendment chains
MATCH path = (latest:Article)-[:SUPERSEDES*]->(historical:Article)
WHERE latest.eli_uri STARTS WITH 'eli:bund:sgbvi'
RETURN path ORDER BY latest.effective_date DESC
```

## Development Gotchas

### Memory Management
Neo4j configured for 4GB heap in `docker-compose.yml` - adjust for larger datasets

### Transaction Safety
Always use transactions for multi-step operations (create nodes + relationships)

### Data Sources Integration
- **gesetze-im-internet.de**: HTML scraping with BeautifulSoup
- **EUR-Lex SPARQL**: SPARQL queries for EU legislation
- **EuroVoc**: RDF/SKOS thesaurus data

## Environment Configuration
Copy `.env.example` to `.env` and configure:
- `OPENAI_API_KEY` for LLM operations
- `NEO4J_URI` and `NEO4J_PASSWORD` for graph database

## Testing Strategy (Planned)
- `tests/unit/` - Component tests (graph operations, parsers)
- `tests/integration/` - End-to-end workflows with test Neo4j instance
- `pytest --cov=src` for coverage reporting