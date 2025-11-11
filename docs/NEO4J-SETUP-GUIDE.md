# Neo4j Database Setup & Deployment Guide

**Last Updated**: November 11, 2025  
**Schema Version**: 2.0 (metadata-schema.cypher)  
**Target**: Neo4j 5.15.0 Enterprise Edition

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Docker Setup (Recommended)](#docker-setup)
3. [Schema Installation](#schema-installation)
4. [Verification & Testing](#verification--testing)
5. [Performance Tuning](#performance-tuning)
6. [Troubleshooting](#troubleshooting)
7. [Production Checklist](#production-checklist)

---

## Prerequisites

### System Requirements
- Docker 20.10+ OR Neo4j Desktop 1.5+
- 8GB+ RAM (4GB minimum for Neo4j)
- 50GB+ disk space (for full dataset with ~5,000 German laws)
- Ubuntu 20.04+ OR Windows with WSL2 OR macOS 10.15+

### Software Requirements
```bash
# Python 3.11+
python3 --version

# Docker (if using Docker)
docker --version
docker-compose --version

# Neo4j CLI tools (optional)
cypher-shell --version
```

### Environment Setup
```bash
# Create Python virtual environment
python3.11 -m venv venv
source venv/bin/activate  # WSL/Linux/macOS
# or
venv\Scripts\activate  # Windows CMD

# Install dependencies
pip install neo4j langchain openai sentence-transformers
```

---

## Docker Setup (Recommended)

### Option 1: Using Existing docker-compose.yml

```bash
# Navigate to project root
cd ~/projects/EU_GraphRAG

# Start Neo4j with Docker Compose
docker-compose up -d neo4j

# Verify container is running
docker-compose ps

# Check logs (wait ~30 seconds for startup)
docker-compose logs -f neo4j
```

### Option 2: Custom Docker Run

```bash
# Pull Neo4j Enterprise image
docker pull neo4j:5.15-enterprise

# Run container
docker run -d \
  --name eu-graphrag-neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
  -e NEO4J_AUTH=neo4j/password \
  -e NEO4J_server_memory_heap_initial__size=2g \
  -e NEO4J_server_memory_heap_max__size=4g \
  -v neo4j-data:/var/lib/neo4j/data \
  neo4j:5.15-enterprise
```

### Neo4j Configuration (docker-compose.yml)
```yaml
neo4j:
  image: neo4j:5.15-enterprise
  container_name: eu-graphrag-neo4j
  environment:
    NEO4J_ACCEPT_LICENSE_AGREEMENT: "yes"
    NEO4J_AUTH: "neo4j/password"
    # Memory settings (adjust based on available RAM)
    NEO4J_server_memory_heap_initial__size: "2g"
    NEO4J_server_memory_heap_max__size: "4g"
    # Plugins
    NEO4J_PLUGINS: '["apoc", "graph-data-science"]'
    # Server settings
    NEO4J_server_default__listen__address: "0.0.0.0:7687"
  ports:
    - "7474:7474"  # HTTP (Browser)
    - "7687:7687"  # Bolt
  volumes:
    - neo4j-data:/var/lib/neo4j/data
    - ./ontologies:/imports
  healthcheck:
    test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "password", "RETURN 1"]
    interval: 10s
    timeout: 5s
    retries: 5
```

### Connection Verification

```bash
# Wait for Neo4j to be ready
docker-compose exec neo4j cypher-shell -u neo4j -p password "RETURN 1"

# Should output: 1
# If error, wait 30 seconds and retry
```

---

## Schema Installation

### Step 1: Wait for Neo4j Ready

```bash
# Check if Neo4j is accepting connections
curl -i http://localhost:7474

# Should return: HTTP/1.1 200 OK (or redirect)
# If fails, wait and retry
```

### Step 2: Load Schema from Cypher File

#### Method A: Using cypher-shell (Recommended)

```bash
# Navigate to ontologies directory
cd ontologies

# Execute schema file
cat metadata-schema.cypher | \
  docker-compose exec -i neo4j \
  cypher-shell -u neo4j -p password --format verbose

# Expected output:
# +---+
# | 1 |
# +---+
# 1 row | 0ms
# [Constraint created, index created] x N
```

#### Method B: Using Python Client

```python
from src.graph.neo4j_client import Neo4jClient

client = Neo4jClient(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password"
)

# Load schema
client.load_schema("ontologies/metadata-schema.cypher")

# Validate
is_valid, issues = client.validate_schema()
print(f"Schema valid: {is_valid}")
if issues:
    print(f"Issues: {issues}")

client.close()
```

#### Method C: Using Neo4j Browser

1. Open `http://localhost:7474` in browser
2. Click "Connect" → Enter credentials (neo4j / password)
3. Open `ontologies/metadata-schema.cypher`
4. Copy contents into query editor
5. Execute (highlight all with Ctrl+A, then Ctrl+Enter)

### Step 3: Verify Schema Installation

```bash
# Check constraints
docker-compose exec neo4j cypher-shell -u neo4j -p password \
  "SHOW CONSTRAINTS"

# Expected output: 12 constraints
# - eli_uri_unique
# - celex_number_unique
# - ecli_unique
# - eurovoc_id_unique
# - authority_id_unique
# - etc.

# Check indexes
docker-compose exec neo4j cypher-shell -u neo4j -p password \
  "SHOW INDEXES"

# Expected output: 16+ indexes
# - articles_index (full-text)
# - laws_index (full-text)
# - concepts_index (full-text)
# - temporal_index (effectiveness)
# - etc.
```

---

## Verification & Testing

### Test 1: Node Type Creation

```bash
docker-compose exec neo4j cypher-shell -u neo4j -p password \
  "MATCH (n) RETURN labels(n) as node_types, count(n) as count GROUP BY labels(n)"

# Expected: Shows all 12 node types with 0 count initially
```

### Test 2: Sample Data Insertion

```bash
# Execute sample data queries from metadata-schema.cypher
docker-compose exec neo4j cypher-shell -u neo4j -p password << 'EOF'

// Insert sample German law
CREATE (law:GermanLaw {
  eli_uri: "eli:de:sgb:6:2023",
  title_de: "Test: Rentenversicherung",
  date_document: date("2023-01-01"),
  first_date_entry_in_force: date("2023-02-01"),
  bgbl_reference: "BGBl 2023 I Nr. 1",
  policy_area: "social_affairs",
  completeness_score: 0.92,
  validation_status: "passed"
});

// Insert sample EU regulation
CREATE (reg:EURegulation {
  eli_uri: "eli:eu:reg:2004:883",
  celex_number: "32004R0883",
  title_en: "Social Security Coordination",
  date_document: date("2004-04-29"),
  first_date_entry_in_force: date("2010-05-01"),
  ojeu_reference: "OJ L 166/1",
  policy_area: "social_affairs",
  completeness_score: 0.96,
  validation_status: "passed"
});

// Query inserted data
MATCH (n) RETURN n LIMIT 10;

EOF
```

### Test 3: Relationship Creation

```bash
# Create IMPLEMENTS relationship
docker-compose exec neo4j cypher-shell -u neo4j -p password << 'EOF'

MATCH (from:GermanLaw {eli_uri: "eli:de:sgb:6:2023"})
MATCH (to:EURegulation {eli_uri: "eli:eu:reg:2004:883"})
CREATE (from)-[:IMPLEMENTS {
  status: "fully_implemented",
  implementation_date: date("2010-05-01")
}]->(to)
RETURN from.eli_uri, to.eli_uri;

EOF
```

### Test 4: Query Validation

```bash
# Test query: Amendment chains
docker-compose exec neo4j cypher-shell -u neo4j -p password \
  "MATCH path = (a:LegalDocument)-[:SUPERSEDES*]->(b:LegalDocument) RETURN path LIMIT 5"

# Test query: Implementation mapping
docker-compose exec neo4j cypher-shell -u neo4j -p password \
  "MATCH (law:GermanLaw)-[impl:IMPLEMENTS]->(directive:EUDirective) RETURN law, impl, directive"

# Test query: Full-text search
docker-compose exec neo4j cypher-shell -u neo4j -p password \
  "CALL db.index.fulltext.queryNodes('articles_index', 'Rentenversicherung') YIELD node RETURN node LIMIT 5"
```

---

## Performance Tuning

### Memory Configuration

```yaml
# Adjust these in docker-compose.yml based on available RAM

# System with 16GB RAM
NEO4J_server_memory_heap_initial__size: "4g"
NEO4J_server_memory_heap_max__size: "8g"

# System with 8GB RAM (minimum)
NEO4J_server_memory_heap_initial__size: "2g"
NEO4J_server_memory_heap_max__size: "4g"

# System with 4GB RAM (not recommended)
NEO4J_server_memory_heap_initial__size: "1g"
NEO4J_server_memory_heap_max__size: "2g"
```

### Index Optimization

```cypher
// Check index usage statistics
CALL db.index.fulltext.listIndexes() 
YIELD indexName, entityType, properties, state
RETURN indexName, entityType, properties, state;

// Analyze query performance
PROFILE MATCH (a:Article)-[:CONCERNS]->(c:LegalConcept) 
RETURN a, c LIMIT 100;

// Rebuild indexes if needed
CALL db.index.fulltext.drop("articles_index");
CALL db.index.fulltext.createNodeIndex(
  "articles_index", 
  ["Article"], 
  ["title_de", "content_de", "eli_uri"]
);
```

### Cache Warming

```python
# Pre-load frequently accessed data
from src.graph.neo4j_client import Neo4jClient

client = Neo4jClient("bolt://localhost:7687", "neo4j", "password")

# Query common patterns
client.query_amendments("eli:de:sgb:6:2023")
client.query_implementations("eli:eu:dir:2014:50")
client.query_concepts("eli:de:sgb:6:43")

client.close()
```

---

## Troubleshooting

### Issue: Container fails to start

```bash
# Check logs
docker-compose logs neo4j

# Common causes:
# 1. Port 7474/7687 already in use
#    Solution: docker-compose down, then docker-compose up

# 2. License agreement not accepted
#    Solution: NEO4J_ACCEPT_LICENSE_AGREEMENT=yes in env

# 3. Insufficient disk space
#    Solution: docker system prune; docker volume prune
```

### Issue: Cannot connect with cypher-shell

```bash
# Verify container is running
docker-compose ps

# Check Neo4j logs
docker-compose logs -f neo4j | grep -i "started"

# Retry connection
docker-compose exec neo4j cypher-shell -u neo4j -p password "RETURN 1"

# If still failing, restart
docker-compose restart neo4j
sleep 30
docker-compose exec neo4j cypher-shell -u neo4j -p password "RETURN 1"
```

### Issue: Schema installation hangs

```bash
# Interrupt (Ctrl+C) and check what's running
docker-compose exec neo4j cypher-shell -u neo4j -p password \
  "CALL dbms.listQueries()"

# If queries stuck, kill them
docker-compose exec neo4j cypher-shell -u neo4j -p password \
  "CALL dbms.killQuery('query-id')"

# Restart Neo4j
docker-compose restart neo4j
```

### Issue: Out of memory errors

```bash
# Increase heap size in docker-compose.yml
NEO4J_server_memory_heap_max__size: "8g"

# Restart
docker-compose down
docker-compose up -d neo4j

# Monitor memory
docker stats neo4j
```

### Issue: Queries are slow

```bash
# Check if indexes are built
docker-compose exec neo4j cypher-shell -u neo4j -p password \
  "CALL db.indexes() YIELD state WHERE state != 'ONLINE' RETURN *"

# If not online, wait for index building
# Check index progress
docker-compose exec neo4j cypher-shell -u neo4j -p password \
  "CALL db.index.fulltext.listIndexes()"
```

---

## Production Checklist

### Pre-Deployment

- [ ] System has 8GB+ RAM available
- [ ] 50GB+ disk space available
- [ ] Docker or Neo4j Desktop installed
- [ ] Python 3.11+ with virtualenv created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with Neo4j credentials
- [ ] `docker-compose.yml` reviewed and customized

### Deployment Steps

- [ ] Run `docker-compose up -d neo4j`
- [ ] Wait 30 seconds for startup
- [ ] Verify connection: `docker-compose exec neo4j cypher-shell -u neo4j -p password "RETURN 1"`
- [ ] Load schema: `cat ontologies/metadata-schema.cypher | docker-compose exec -i neo4j cypher-shell -u neo4j -p password`
- [ ] Verify schema: `docker-compose exec neo4j cypher-shell -u neo4j -p password "SHOW CONSTRAINTS"`
- [ ] Run validation tests (see Verification & Testing section)
- [ ] Test sample data insertion
- [ ] Confirm all 12 node types and 16 relationships available
- [ ] Run performance tests

### Post-Deployment

- [ ] Set up regular backups: `docker-compose exec neo4j neo4j-admin backup --to-path=/backup --backup-dir=/backups`
- [ ] Enable audit logging in Neo4j config
- [ ] Configure user authentication (change default password)
- [ ] Set up monitoring and alerting
- [ ] Document connection parameters
- [ ] Create disaster recovery plan

### Data Ingestion Preparation

- [ ] Validate metadata model against 10+ sample laws (see METADATA-VALIDATION.md)
- [ ] Test Python ingestion pipeline
- [ ] Prepare data sources (gesetze-im-internet.de, EUR-Lex SPARQL)
- [ ] Set up rate limiting for web scrapers
- [ ] Create staging environment
- [ ] Plan incremental loading strategy
- [ ] Estimate data volume: ~5,000 German laws + 300,000+ EU acts

---

## Next Steps

1. **Data Ingestion**: See `IMPLEMENTATION-SUMMARY.md` for pipeline setup
2. **Query Development**: Use Neo4j Browser to build and test queries
3. **Vector Integration**: Configure vector search for semantic queries
4. **API Development**: Build GraphQL/REST API on top of graph queries
5. **UI Development**: Create web interface for query building and visualization

---

## Resources

- **Neo4j Documentation**: https://neo4j.com/docs/
- **Cypher Query Language**: https://neo4j.com/docs/cypher-manual/
- **Neo4j Python Driver**: https://neo4j.com/docs/python-manual/
- **Neo4j Desktop**: https://neo4j.com/download/neo4j-desktop/
- **APOC Library**: https://github.com/neo4j-contrib/neo4j-apoc-procedures

