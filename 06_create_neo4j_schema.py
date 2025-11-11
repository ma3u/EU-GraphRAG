
# Create Neo4j schema initialization script
schema_cypher = """// EU GraphRAG - Neo4j Graph Schema
// Date: November 9, 2025
// Version: 1.0

// ============================================================================
// CONSTRAINTS (Unique Identifiers)
// ============================================================================

// ELI constraints
CREATE CONSTRAINT eli_work_uri IF NOT EXISTS
FOR (w:ELIWork) REQUIRE w.eli_uri IS UNIQUE;

CREATE CONSTRAINT eli_expression_uri IF NOT EXISTS
FOR (e:ELIExpression) REQUIRE e.eli_uri IS UNIQUE;

CREATE CONSTRAINT article_eli_uri IF NOT EXISTS
FOR (a:Article) REQUIRE a.eli_uri IS UNIQUE;

// ECLI constraints
CREATE CONSTRAINT ecli_identifier IF NOT EXISTS
FOR (d:CourtDecision) REQUIRE d.ecli IS UNIQUE;

CREATE CONSTRAINT court_code IF NOT EXISTS
FOR (c:Court) REQUIRE (c.country_code, c.court_code) IS UNIQUE;

// EuroVoc constraints
CREATE CONSTRAINT eurovoc_concept_id IF NOT EXISTS
FOR (lc:LegalConcept) REQUIRE lc.eurovoc_id IS UNIQUE;

// SGB constraints
CREATE CONSTRAINT sgb_book IF NOT EXISTS
FOR (b:SocialLawBook) REQUIRE b.book_number IS UNIQUE;

CREATE CONSTRAINT process_id IF NOT EXISTS
FOR (p:BusinessProcess) REQUIRE p.process_id IS UNIQUE;

// ============================================================================
// INDEXES (Performance Optimization)
// ============================================================================

// Full-text search indexes
CREATE FULLTEXT INDEX article_text IF NOT EXISTS
FOR (a:Article) ON EACH [a.title, a.text_content];

CREATE FULLTEXT INDEX decision_text IF NOT EXISTS
FOR (d:CourtDecision) ON EACH [d.title, d.summary];

// Property indexes for filtering
CREATE INDEX article_date IF NOT EXISTS
FOR (a:Article) ON (a.effective_date);

CREATE INDEX decision_date IF NOT EXISTS
FOR (d:CourtDecision) ON (d.decision_date);

CREATE INDEX document_type IF NOT EXISTS
FOR (w:ELIWork) ON (w.type_document);

// Composite indexes for common queries
CREATE INDEX article_book_number IF NOT EXISTS
FOR (a:Article) ON (a.sgb_book, a.article_number);

// ============================================================================
// VECTOR INDEX (Semantic Search)
// ============================================================================

// Article embeddings for semantic similarity search
CREATE VECTOR INDEX article_embeddings IF NOT EXISTS
FOR (a:Article) ON (a.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }
};

// Legal concept embeddings
CREATE VECTOR INDEX concept_embeddings IF NOT EXISTS
FOR (c:LegalConcept) ON (c.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }
};

// ============================================================================
// SAMPLE DATA CREATION (For Testing)
// ============================================================================

// Create sample ELI Work (EU Directive)
CREATE (dir:ELIWork:EUDirective {
  eli_uri: 'http://data.europa.eu/eli/dir/2016/680',
  type_document: 'directive',
  date_document: date('2016-04-27'),
  title_de: 'Richtlinie über den Schutz natürlicher Personen bei der Verarbeitung personenbezogener Daten',
  title_en: 'Directive on the protection of natural persons with regard to the processing of personal data',
  in_force: true,
  first_date_entry_in_force: date('2018-05-06')
});

// Create sample German Law (SGB VI)
CREATE (sgb6:ELIWork:GermanLaw:SocialLawBook {
  eli_uri: 'http://data.europa.eu/eli/de/sgb/6/oj',
  book_number: 'VI',
  type_document: 'federal_law',
  title_de: 'Gesetzliche Rentenversicherung',
  title_en: 'Statutory Pension Insurance',
  effective_date: date('1992-01-01'),
  latest_amendment: date('2023-10-01'),
  authority: 'Deutsche Rentenversicherung (DRV)'
});

// Create sample Article (SGB VI § 43)
CREATE (art43:Article {
  eli_uri: 'http://data.europa.eu/eli/de/sgb/6/43/oj',
  article_number: '43',
  title: 'Anspruch auf Rente wegen Erwerbsminderung',
  title_en: 'Entitlement to disability pension',
  sgb_book: 'VI',
  text_content: '(1) Versicherte haben bis zum Erreichen der Regelaltersgrenze Anspruch auf Rente wegen voller Erwerbsminderung, wenn sie...',
  effective_date: date('1992-01-01'),
  last_updated: date('2023-03-01')
})-[:BELONGS_TO]->(sgb6);

// Create sample TemporalVersion (Amendment tracking)
CREATE (v1:TemporalVersion {
  eli_uri: 'http://data.europa.eu/eli/de/sgb/6/43/2020-01-01',
  version_date: date('2020-01-01'),
  article_number: '43',
  text_content: '...original text from 2020...',
  bgbl_reference: 'BGBl. I 2019 Nr. 45 S. 2345'
});

CREATE (v2:TemporalVersion {
  eli_uri: 'http://data.europa.eu/eli/de/sgb/6/43/2023-03-01',
  version_date: date('2023-03-01'),
  article_number: '43',
  text_content: '...amended text from 2023...',
  bgbl_reference: 'BGBl. I 2023 Nr. 45 S. 1234'
})-[:SUPERSEDES {
  change_date: date('2023-03-01'),
  change_reason: 'Anpassung Einkommensgrenzen'
}]->(v1);

CREATE (art43)-[:CURRENT_VERSION]->(v2);
CREATE (art43)-[:HAS_VERSION]->(v1);
CREATE (art43)-[:HAS_VERSION]->(v2);

// Create sample Court and Decision
CREATE (bgh:Court {
  name: 'Bundesgerichtshof',
  court_code: 'BGH',
  country_code: 'DE',
  jurisdiction: 'federal',
  court_type: 'supreme'
});

CREATE (decision:CourtDecision {
  ecli: 'ECLI:DE:BGH:2023:120723U2STR456.22.0',
  title: 'BGH Urteil vom 12.07.2023 - 2 StR 456/22',
  decision_date: date('2023-07-12'),
  decision_type: 'Urteil',
  language: 'deu',
  summary: 'Entscheidung zum Strafverfahrensrecht...'
})-[:DECIDED_BY]->(bgh);

// Create sample EuroVoc concepts
CREATE (concept1:LegalConcept {
  eurovoc_id: '4530',
  pref_label_de: 'Rentenversicherung',
  pref_label_en: 'pension insurance',
  pref_label_fr: 'assurance pension',
  domain_code: '28',
  domain_label: 'Soziale Fragen',
  microthesaurus_code: '2826'
});

CREATE (concept2:LegalConcept {
  eurovoc_id: '446',
  pref_label_de: 'Arbeitslosengeld',
  pref_label_en: 'unemployment benefit',
  pref_label_fr: 'allocation de chômage',
  domain_code: '28',
  microthesaurus_code: '2821'
});

// Link article to concepts
CREATE (art43)-[:CONCERNS {relevance_score: 0.95}]->(concept1);

// Create sample Business Process
CREATE (process:BusinessProcess {
  process_id: 'DRV-P-001',
  name: 'Antrag auf Erwerbsminderungsrente',
  name_en: 'Disability Pension Application',
  authority: 'Deutsche Rentenversicherung',
  avg_duration_days: 90,
  annual_volume: 45000,
  process_steps: [
    'Antragseingang',
    'Prüfung Versicherungsverlauf',
    'Medizinische Begutachtung',
    'Einkommensprüfung',
    'Rentenbescheid'
  ]
})-[:BASED_ON]->(art43);

// Impact relationship
CREATE (art43)-[:IMPACTS {
  impact_type: 'eligibility_criteria',
  affected_population: 320000,
  change_probability: 'medium'
}]->(process);

// Create sample EU Regulation coordination
CREATE (eureg:ELIWork:EURegulation {
  eli_uri: 'http://data.europa.eu/eli/reg/2004/883/oj',
  type_document: 'regulation',
  title_en: 'Coordination of social security systems',
  title_de: 'Koordinierung der Systeme der sozialen Sicherheit',
  date_document: date('2004-04-29')
});

CREATE (sgb6)-[:COORDINATES_WITH {
  coordination_area: 'cross-border pension rights',
  articles: ['Art. 6', 'Art. 52']
}]->(eureg);

// ============================================================================
// QUERY EXAMPLES (Commented)
// ============================================================================

// Example 1: Find all articles in SGB VI
// MATCH (a:Article {sgb_book: 'VI'})
// RETURN a.article_number, a.title
// ORDER BY toInteger(a.article_number);

// Example 2: Track amendment history
// MATCH path = (latest:TemporalVersion {article_number: '43'})
//              -[:SUPERSEDES*]->(historical:TemporalVersion)
// RETURN path, [v IN nodes(path) | v.version_date] as dates
// ORDER BY latest.version_date DESC;

// Example 3: Find impacted processes for an article
// MATCH (a:Article {article_number: '43'})-[:IMPACTS]->(p:BusinessProcess)
// RETURN a.title, p.name, p.annual_volume, p.process_id;

// Example 4: Semantic search (with embeddings)
// CALL db.index.vector.queryNodes('article_embeddings', 10, $query_embedding)
// YIELD node as article, score
// MATCH (article)-[:CONCERNS]->(concept:LegalConcept)
// RETURN article.title, score, collect(concept.pref_label_de) as concepts
// ORDER BY score DESC LIMIT 5;

// Example 5: Find German laws implementing EU directive
// MATCH (directive:EUDirective {eli_uri: 'http://data.europa.eu/eli/dir/2016/680'})
//       -[:IMPLEMENTED_BY]->(law:GermanLaw)
// RETURN directive.title_en, collect(law.title_de) as implementing_laws;

// ============================================================================
// SCHEMA VALIDATION QUERIES
// ============================================================================

// Count nodes by type
// MATCH (n)
// RETURN labels(n) as NodeType, count(n) as Count
// ORDER BY Count DESC;

// Count relationships by type
// MATCH ()-[r]->()
// RETURN type(r) as RelationshipType, count(r) as Count
// ORDER BY Count DESC;

// Verify constraints
// SHOW CONSTRAINTS;

// Verify indexes
// SHOW INDEXES;

RETURN 'EU GraphRAG schema initialized successfully' as Status;
"""

# Write Neo4j schema file
with open("/home/mbuchhorn/projects/EU_GraphRAG/ontologies/graph-schema.cypher", 'w', encoding='utf-8') as f:
    f.write(schema_cypher)

print("✓ Created Neo4j graph schema")
print("  File: /home/mbuchhorn/projects/EU_GraphRAG/ontologies/graph-schema.cypher")
print("  - Constraints for ELI, ECLI, EuroVoc identifiers")
print("  - Indexes for performance optimization")
print("  - Vector indexes for semantic search")
print("  - Sample data for testing")
