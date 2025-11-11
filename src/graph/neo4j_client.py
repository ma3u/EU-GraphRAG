"""
Neo4j Database Client for EU_GraphRAG

Manages connections and operations with Neo4j graph database.
Handles document ingestion, schema initialization, and query execution.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from contextlib import contextmanager
import json

try:
    from neo4j import GraphDatabase, Session, Transaction, Result
    from neo4j.exceptions import Neo4jError, AuthError, ServiceUnavailable
except ImportError:
    raise ImportError("neo4j package required. Install: pip install neo4j")

logger = logging.getLogger(__name__)


class Neo4jClient:
    """Neo4j database client with connection pooling and transaction management"""
    
    def __init__(self, uri: str, user: str, password: str, 
                 encrypted: bool = False, max_pool_size: int = 50):
        """
        Initialize Neo4j client
        
        Args:
            uri: Neo4j URI (bolt://host:port)
            user: Database user
            password: Database password
            encrypted: Use encrypted connection
            max_pool_size: Maximum connection pool size
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.encrypted = encrypted
        
        self.driver = None
        self.session = None
        
        try:
            self.connect(max_pool_size)
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j client: {e}")
            raise
    
    def connect(self, max_pool_size: int = 50):
        """Establish connection to Neo4j"""
        logger.info(f"Connecting to Neo4j: {self.uri}")
        
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                encrypted=self.encrypted,
                max_pool_size=max_pool_size,
            )
            # Test connection
            self.driver.verify_connectivity()
            logger.info("✓ Connected to Neo4j")
        except AuthError as e:
            logger.error(f"Authentication failed: {e}")
            raise
        except ServiceUnavailable as e:
            logger.error(f"Neo4j service unavailable: {e}")
            raise
        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    @contextmanager
    def session_scope(self):
        """Context manager for session"""
        session = self.driver.session()
        try:
            yield session
        finally:
            session.close()
    
    def execute_query(self, cypher: str, parameters: Dict = None) -> Result:
        """
        Execute Cypher query
        
        Args:
            cypher: Cypher query string
            parameters: Query parameters
            
        Returns:
            Query result
        """
        parameters = parameters or {}
        
        with self.session_scope() as session:
            try:
                result = session.run(cypher, parameters)
                return result
            except Exception as e:
                logger.error(f"Query execution error: {e}\nQuery: {cypher}")
                raise
    
    def execute_query_single(self, cypher: str, parameters: Dict = None) -> Optional[Dict]:
        """Execute query and return single result"""
        result = self.execute_query(cypher, parameters)
        record = result.single()
        return dict(record) if record else None
    
    def execute_query_list(self, cypher: str, parameters: Dict = None) -> List[Dict]:
        """Execute query and return all results as list"""
        result = self.execute_query(cypher, parameters)
        return [dict(record) for record in result]
    
    def load_schema(self, schema_file: str):
        """
        Load Cypher schema file and execute
        
        Args:
            schema_file: Path to .cypher schema file
        """
        logger.info(f"Loading schema from: {schema_file}")
        
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_content = f.read()
            
            # Split by semicolons and execute each statement
            statements = [s.strip() for s in schema_content.split(';') if s.strip()]
            
            with self.session_scope() as session:
                for stmt in statements:
                    if stmt and not stmt.startswith('//'):
                        try:
                            session.run(stmt)
                            logger.debug(f"✓ Executed: {stmt[:60]}...")
                        except Exception as e:
                            logger.warning(f"⚠ Statement failed (may be expected): {e}")
            
            logger.info(f"✓ Schema loaded ({len(statements)} statements)")
        
        except FileNotFoundError:
            logger.error(f"Schema file not found: {schema_file}")
            raise
        except Exception as e:
            logger.error(f"Error loading schema: {e}")
            raise
    
    def ingest_document(self, document: Dict, merge: bool = True) -> bool:
        """
        Ingest a legal document into graph
        
        Args:
            document: Document dict with metadata
            merge: Use MERGE (idempotent) vs CREATE
            
        Returns:
            Success status
        """
        try:
            eli_uri = document.get('eli_uri')
            if not eli_uri:
                logger.error("Document missing eli_uri")
                return False
            
            cypher = self._build_document_insert_cypher(document, merge)
            self.execute_query(cypher, {'doc': document})
            
            logger.debug(f"✓ Ingested: {eli_uri}")
            return True
        
        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            return False
    
    def _build_document_insert_cypher(self, document: Dict, merge: bool = True) -> str:
        """Build Cypher for document insertion"""
        operation = "MERGE" if merge else "CREATE"
        
        # Determine node type based on source_type
        source_type = document.get('source_type', 'german_law')
        node_type = self._get_node_type(source_type)
        
        # Build properties string
        props = ', '.join(f"{k}: ${k}" for k in document.keys())
        
        cypher = f"""
        {operation} (doc:{node_type} {{eli_uri: $doc.eli_uri}})
        SET doc += $doc
        RETURN doc
        """
        
        return cypher
    
    def _get_node_type(self, source_type: str) -> str:
        """Map source type to Neo4j node label"""
        type_mapping = {
            'german_law': 'GermanLaw',
            'eu_regulation': 'EURegulation',
            'eu_directive': 'EUDirective',
            'case_law': 'CourtDecision',
        }
        return type_mapping.get(source_type, 'LegalDocument')
    
    def ingest_documents_batch(self, documents: List[Dict], batch_size: int = 100) -> Tuple[int, int]:
        """
        Ingest multiple documents in batches
        
        Args:
            documents: List of document dicts
            batch_size: Documents per transaction
            
        Returns:
            (successfully_ingested, failed)
        """
        success_count = 0
        failed_count = 0
        
        logger.info(f"Starting batch ingest of {len(documents)} documents")
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            batch_num = i // batch_size + 1
            
            with self.session_scope() as session:
                with session.begin_transaction() as tx:
                    for doc in batch:
                        try:
                            cypher = self._build_document_insert_cypher(doc)
                            tx.run(cypher, {'doc': doc})
                            success_count += 1
                        except Exception as e:
                            logger.error(f"Error in batch: {e}")
                            failed_count += 1
            
            logger.info(f"✓ Batch {batch_num} complete ({success_count} ingested, {failed_count} failed)")
        
        return success_count, failed_count
    
    def create_relationship(self, from_uri: str, to_uri: str, rel_type: str, 
                          from_label: str = "LegalDocument", 
                          to_label: str = "LegalDocument",
                          properties: Dict = None) -> bool:
        """
        Create relationship between documents
        
        Args:
            from_uri: Source document ELI URI
            to_uri: Target document ELI URI
            rel_type: Relationship type (e.g., IMPLEMENTS, SUPERSEDES)
            from_label: Source node label
            to_label: Target node label
            properties: Relationship properties
            
        Returns:
            Success status
        """
        try:
            properties = properties or {}
            props_str = ', '.join(f"{k}: ${k}" for k in properties.keys())
            props_str = f" {{{props_str}}}" if props_str else ""
            
            cypher = f"""
            MATCH (from:{from_label} {{eli_uri: $from_uri}})
            MATCH (to:{to_label} {{eli_uri: $to_uri}})
            MERGE (from)-[r:{rel_type}{props_str}]->(to)
            SET r += $props
            RETURN r
            """
            
            params = {
                'from_uri': from_uri,
                'to_uri': to_uri,
                **properties
            }
            params['props'] = properties
            
            result = self.execute_query_single(cypher, params)
            return result is not None
        
        except Exception as e:
            logger.error(f"Error creating relationship: {e}")
            return False
    
    def query_amendments(self, law_uri: str) -> List[Dict]:
        """Query amendment chain for a law"""
        cypher = """
        MATCH path = (law:LegalDocument {eli_uri: $uri})-[:SUPERSEDES*]->(prev:LegalDocument)
        RETURN 
            law.eli_uri as current_version,
            [n in nodes(path) | n.eli_uri] as version_chain,
            [r in relationships(path) | r.amendment_type] as amendment_types
        """
        
        return self.execute_query_list(cypher, {'uri': law_uri})
    
    def query_implementations(self, directive_uri: str) -> List[Dict]:
        """Query implementation mapping (EU → National)"""
        cypher = """
        MATCH (directive:EUDirective {eli_uri: $uri})-[impl:IMPLEMENTED_BY]->(law:GermanLaw)
        RETURN 
            directive.celex_number as directive_celex,
            directive.title_en as directive_title,
            law.eli_uri as implementing_law,
            law.title_de as law_title,
            impl.status as implementation_status,
            impl.implementation_date as date_implemented
        ORDER BY impl.implementation_date
        """
        
        return self.execute_query_list(cypher, {'uri': directive_uri})
    
    def query_concepts(self, article_uri: str) -> List[Dict]:
        """Query EuroVoc concepts related to article"""
        cypher = """
        MATCH (article:Article {eli_uri: $uri})-[rel:CONCERNS]->(concept:LegalConcept)
        RETURN 
            concept.eurovoc_id as concept_id,
            concept.pref_label_de as concept_de,
            concept.pref_label_en as concept_en,
            rel.relevance_score as relevance
        ORDER BY rel.relevance_score DESC
        """
        
        return self.execute_query_list(cypher, {'uri': article_uri})
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        cypher = """
        RETURN 
            count(n:GermanLaw) as german_laws,
            count(n:EURegulation) as eu_regulations,
            count(n:EUDirective) as eu_directives,
            count(n:Article) as articles,
            count(n:LegalConcept) as concepts
        """
        
        return self.execute_query_single(cypher) or {}
    
    def search_full_text(self, query: str, node_type: str = "LegalDocument") -> List[Dict]:
        """Full-text search across documents"""
        cypher = f"""
        CALL db.index.fulltext.queryNodes(
            "articles_index",
            $query
        ) YIELD node, score
        RETURN 
            node.eli_uri as uri,
            node.title_de as title,
            score
        ORDER BY score DESC
        LIMIT 50
        """
        
        return self.execute_query_list(cypher, {'query': query})
    
    def validate_schema(self) -> Tuple[bool, List[str]]:
        """Validate schema constraints and indexes"""
        logger.info("Validating schema...")
        
        issues = []
        
        # Check constraints
        constraint_check = """
        SHOW CONSTRAINTS
        """
        try:
            result = self.execute_query_list(constraint_check)
            if len(result) == 0:
                issues.append("No constraints found - schema may not be loaded")
            logger.info(f"✓ Found {len(result)} constraints")
        except Exception as e:
            issues.append(f"Error checking constraints: {e}")
        
        # Check indexes
        index_check = """
        SHOW INDEXES
        """
        try:
            result = self.execute_query_list(index_check)
            if len(result) == 0:
                issues.append("No indexes found - performance may be degraded")
            logger.info(f"✓ Found {len(result)} indexes")
        except Exception as e:
            issues.append(f"Error checking indexes: {e}")
        
        return len(issues) == 0, issues


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize client
    client = Neo4jClient(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )
    
    try:
        # Get statistics
        stats = client.get_statistics()
        print(f"Database statistics: {stats}")
        
        # Validate schema
        is_valid, issues = client.validate_schema()
        print(f"Schema valid: {is_valid}")
        if issues:
            print(f"Issues: {issues}")
    
    finally:
        client.close()

