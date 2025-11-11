// EU GraphRAG - Comprehensive Neo4j Schema with Metadata
// Date: November 11, 2025
// Version: 2.0 (Updated with unified metadata model)
// Description: Complete schema for German federal laws and EU legislation

// ============================================================================
// CONSTRAINTS (Unique Identifiers & Data Integrity)
// ============================================================================

// Primary identifiers
CREATE CONSTRAINT eli_uri_unique IF NOT EXISTS
FOR (n:LegalDocument) REQUIRE n.eli_uri IS UNIQUE;

CREATE CONSTRAINT celex_number_unique IF NOT EXISTS
FOR (n:EULaw) REQUIRE n.celex_number IS UNIQUE;

CREATE CONSTRAINT ecli_unique IF NOT EXISTS
FOR (d:CourtDecision) REQUIRE d.ecli IS UNIQUE;

CREATE CONSTRAINT eurovoc_concept_id_unique IF NOT EXISTS
FOR (lc:LegalConcept) REQUIRE lc.eurovoc_id IS UNIQUE;

CREATE CONSTRAINT authority_id_unique IF NOT EXISTS
FOR (a:Authority) REQUIRE a.authority_id IS UNIQUE;

// Secondary identifiers
CREATE CONSTRAINT sgb_book_unique IF NOT EXISTS
FOR (b:SocialLawBook) REQUIRE b.book_number IS UNIQUE;

CREATE CONSTRAINT court_identifier IF NOT EXISTS
FOR (c:Court) REQUIRE (c.country_code, c.court_code) IS UNIQUE;

// ============================================================================
// INDEXES (Performance Optimization)
// ============================================================================

// Full-text search
CREATE FULLTEXT INDEX article_search IF NOT EXISTS
FOR (a:Article) ON EACH [a.title_de, a.title_en, a.text_content];

CREATE FULLTEXT INDEX law_search IF NOT EXISTS
FOR (l:LegalDocument) ON EACH [l.title_de, l.title_en, l.short_title];

CREATE FULLTEXT INDEX concept_search IF NOT EXISTS
FOR (c:LegalConcept) ON EACH [c.pref_label_de, c.pref_label_en];

// Temporal searches
CREATE INDEX article_effective_date IF NOT EXISTS
FOR (a:Article) ON (a.first_date_entry_in_force);

CREATE INDEX amendment_date IF NOT EXISTS
FOR (v:TemporalVersion) ON (v.version_date);

CREATE INDEX document_update IF NOT EXISTS
FOR (d:LegalDocument) ON (d.last_update);

// Policy area / classification
CREATE INDEX policy_area IF NOT EXISTS
FOR (d:LegalDocument) ON (d.policy_area);

CREATE INDEX authority_jurisdiction IF NOT EXISTS
FOR (a:Authority) ON (a.jurisdiction_level);

// ============================================================================
// NODE TYPES (Comprehensive Legal Document Model)
// ============================================================================

// Base node: All legal documents
CREATE (doc:LegalDocument {
  // === IDENTIFICATION ===
  eli_uri: STRING NOT NULL UNIQUE,
  internal_id: STRING,
  
  // === TITLES & NAMES ===
  title_de: STRING,
  title_en: STRING,
  title_original: STRING,
  short_title: STRING,
  
  // === TEMPORAL METADATA ===
  date_document: DATE NOT NULL,
  first_date_entry_in_force: DATE NOT NULL,
  date_no_longer_in_force: DATE,
  last_amended: DATE NOT NULL,
  
  // === ORGANIZATIONAL ===
  policy_area: STRING NOT NULL,
  subject_matter_domain: STRING,
  subject_matter_subdomain: STRING,
  
  // === INSTITUTIONAL ===
  legislator_jurisdiction: STRING,
  legislator_body: STRING,
  responsible_authority: STRING,
  
  // === QUALITY & MANAGEMENT ===
  completeness_score: FLOAT,
  data_quality_issues: [STRING],
  validation_status: STRING,
  source_type: STRING,
  version_status: STRING,
  last_update: DATE NOT NULL,
  
  // === CONTENT SCOPE ===
  geographic_scope: STRING,
  sectoral_scope: [STRING],
  beneficiary_categories: [STRING]
});

// German federal laws
CREATE (german:GermanLaw:LegalDocument {
  bgbl_reference: STRING,
  bgbl_year: INTEGER,
  bgbl_number: INTEGER,
  bgbl_page: INTEGER,
  sponsoring_ministry: STRING
});

// EU legislation (supertype)
CREATE (eu:EULaw:LegalDocument {
  celex_number: STRING NOT NULL UNIQUE,
  ojeu_reference: STRING,
  ojeu_series: STRING,
  ojeu_year: INTEGER,
  ojeu_number: INTEGER,
  ojeu_page: INTEGER,
  legal_basis_tfeu: STRING,
  legislative_procedure: STRING,
  co_legislators: [STRING]
});

// EU Directives (require transposition)
CREATE (directive:EUDirective:EULaw {
  transposition_deadline: DATE,
  transposition_status: STRING,
  transposition_date: DATE,
  transposition_gap: STRING,
  implementing_member_states: [STRING],
  non_implementing_states: [STRING],
  implementation_status: STRING
});

// EU Regulations (directly applicable)
CREATE (regulation:EURegulation:EULaw {
  member_state_exceptions: [STRING],
  opt_out_states: [STRING]
});

// Social Law Books
CREATE (sgb:SocialLawBook:GermanLaw {
  book_number: STRING NOT NULL UNIQUE,
  book_roman_numeral: STRING,
  official_name: STRING,
  scope_description: STRING,
  authority_id: STRING,
  authority_name: STRING,
  article_count: INTEGER
});

// Individual articles/sections
CREATE (article:Article:LegalDocument {
  // === STRUCTURE ===
  article_number: STRING NOT NULL,
  section_number: STRING,
  paragraph_number: STRING,
  hierarchy_path: STRING,
  sequence_in_document: INTEGER,
  
  // === CONTENT ===
  title_de: STRING,
  title_en: STRING,
  text_content: STRING,
  plain_text_summary: STRING,
  
  // === ARTICLE CLASSIFICATION ===
  article_type: STRING,
  article_category: STRING,
  
  // === COMPLIANCE & ENFORCEMENT ===
  enforcement_mechanism: [STRING],
  applicable_sanctions: [STRING],
  penalty_type: STRING,
  penalty_range: STRING,
  statute_of_limitations: INTEGER,
  
  // === REGULATORY BURDEN ===
  compliance_cost_category: STRING,
  affected_business_processes: [STRING],
  reporting_obligations: [STRING],
  data_retention_period: INTEGER,
  
  // === AMENDMENT SPECIFIC ===
  is_amendment: BOOLEAN,
  amended_article: STRING,
  amendment_source: STRING
});

// Temporal versioning
CREATE (version:TemporalVersion {
  version_date: DATE NOT NULL,
  version_snapshot: STRING,
  amendment_source: STRING,
  amendment_type: STRING,
  amendment_description: STRING,
  change_log: [STRING]
});

// Organizations/Authorities
CREATE (authority:Authority {
  authority_id: STRING NOT NULL UNIQUE,
  authority_name: STRING NOT NULL,
  authority_name_en: STRING,
  authority_short_name: STRING,
  jurisdiction_level: STRING,
  country_code: STRING,
  agency_type: STRING,
  enforcement_scope: [STRING],
  website: STRING
});

// Court entities
CREATE (court:Court:Authority {
  country_code: STRING NOT NULL,
  court_code: STRING NOT NULL,
  court_name: STRING,
  jurisdiction: STRING,
  court_type: STRING,
  competence_areas: [STRING]
});

// Court decisions
CREATE (decision:CourtDecision {
  ecli: STRING NOT NULL UNIQUE,
  ecli_country: STRING,
  ecli_court: STRING,
  ecli_year: INTEGER,
  ecli_decision_number: STRING,
  decision_type: STRING,
  decision_date: DATE NOT NULL,
  title: STRING,
  summary: STRING,
  full_text: STRING,
  language: STRING,
  judgment_summary: STRING
});

// EuroVoc concepts
CREATE (concept:LegalConcept:EuroVocConcept {
  // === IDENTIFICATION ===
  eurovoc_id: STRING NOT NULL UNIQUE,
  concept_type: STRING,
  
  // === MULTILINGUAL LABELS (All 24 EU languages) ===
  pref_label_de: STRING,
  pref_label_en: STRING,
  pref_label_fr: STRING,
  pref_label_es: STRING,
  pref_label_it: STRING,
  pref_label_pl: STRING,
  pref_label_pt: STRING,
  pref_label_nl: STRING,
  pref_label_sv: STRING,
  pref_label_da: STRING,
  pref_label_fi: STRING,
  pref_label_cs: STRING,
  pref_label_hu: STRING,
  pref_label_ro: STRING,
  pref_label_sk: STRING,
  pref_label_sl: STRING,
  pref_label_bg: STRING,
  pref_label_hr: STRING,
  pref_label_et: STRING,
  pref_label_el: STRING,
  pref_label_lt: STRING,
  pref_label_lv: STRING,
  pref_label_mt: STRING,
  
  // === ALTERNATIVE LABELS ===
  alt_labels_de: [STRING],
  alt_labels_en: [STRING],
  
  // === CLASSIFICATION ===
  domain_code: STRING,
  domain_label: STRING,
  microthesaurus_code: STRING,
  microthesaurus_label: STRING,
  
  // === DEFINITIONS ===
  scope_note_de: STRING,
  scope_note_en: STRING,
  scope_note_fr: STRING,
  
  // === THESAURUS STRUCTURE ===
  has_narrower: BOOLEAN,
  has_broader: BOOLEAN,
  has_related: BOOLEAN,
  
  // === METADATA ===
  last_modified: DATE,
  status: STRING
});

// Business processes (SGB-specific)
CREATE (process:BusinessProcess {
  process_id: STRING NOT NULL UNIQUE,
  process_name: STRING,
  process_name_en: STRING,
  authority_id: STRING,
  authority_name: STRING,
  
  // === PROCESS METRICS ===
  average_duration_days: INTEGER,
  annual_volume: INTEGER,
  processing_steps: [STRING],
  
  // === COMPLIANCE ===
  required_documentation: [STRING],
  regulatory_basis: [STRING],
  
  // === IT SYSTEMS ===
  it_systems_involved: [STRING],
  system_integrations: [STRING]
});

// ============================================================================
// RELATIONSHIP TYPES (Comprehensive)
// ============================================================================

// Transposition & Implementation
(GermanLaw)-[:IMPLEMENTS {
  transposition_status: STRING,
  articles_mapped: [STRING],
  implementation_complete: BOOLEAN,
  mapping_date: DATE
}]->(EUDirective);

(EUDirective)-[:IMPLEMENTED_BY {
  member_state: STRING,
  implementing_laws: [STRING],
  status: STRING
}]->(GermanLaw);

// Amendment & Version History
(Article)-[:SUPERSEDES {
  superseded_date: DATE,
  amendment_type: STRING,
  change_description: STRING
}]->(Article);

(TemporalVersion)-[:VERSION_OF {
  version_sequence: INTEGER
}]->(Article);

(Amendment)-[:AMENDS {
  amendment_date: DATE,
  amendment_source: STRING
}]->(Article);

// Cross-References
(Article)-[:REFERENCES {
  reference_type: STRING,
  is_normative: BOOLEAN,
  article_pair: STRING
}]->(Article);

(LegalDocument)-[:REFERENCES {
  reference_type: STRING,
  citation_count: INTEGER
}]->(LegalDocument);

// Hierarchical Structure
(SocialLawBook)-[:CONTAINS_CHAPTER]->(Chapter);
(Chapter)-[:CONTAINS_SECTION]->(Section);
(Section)-[:CONTAINS_ARTICLE]->(Article);

(Article)-[:PART_OF]->(SocialLawBook);

// Coordination & Harmonization
(SocialLawBook)-[:COORDINATES_WITH {
  coordination_area: STRING,
  priority_rules: STRING,
  articles_affected: [STRING]
}]->(EURegulation);

(LegalDocument)-[:IMPLEMENTS_PRINCIPLE {
  principle_id: STRING,
  principle_name: STRING
}]->(LegalConcept);

// Administrative Relationships
(LegalDocument)-[:ADMINISTERED_BY {
  primary_responsibility: BOOLEAN,
  jurisdiction_level: STRING
}]->(Authority);

(LegalDocument)-[:ENFORCED_BY]->(Authority);

(Process)-[:BASED_ON]->(Article);

(Article)-[:IMPACTS {
  impact_type: STRING,
  affected_population: INTEGER,
  change_probability: STRING
}]->(Process);

// Court Decision Links
(CourtDecision)-[:DECIDED_BY]->(Court);

(CourtDecision)-[:INTERPRETS]->(Article);

(CourtDecision)-[:CITES {
  citation_count: INTEGER
}]->(Article);

// Concept & Classification
(Article)-[:CONCERNS {
  relevance_score: FLOAT,
  certainty: FLOAT
}]->(LegalConcept);

(LegalDocument)-[:HAS_SUBJECT_MATTER]->(Subject);

(LegalDocument)-[:CLASSIFIED_AS {
  classification_scheme: STRING,
  classification_code: STRING
}]->(Classification);

// EuroVoc Thesaurus Structure
(LegalConcept)-[:NARROWER_CONCEPT]->(LegalConcept);

(LegalConcept)-[:BROADER_CONCEPT]->(LegalConcept);

(LegalConcept)-[:RELATED_CONCEPT]->(LegalConcept);

// Multilingual Content
(LegalDocument)-[:HAS_TRANSLATION {
  target_language: STRING,
  translation_status: STRING,
  machine_translated: BOOLEAN,
  certified: BOOLEAN
}]->(TranslatedContent);

// ============================================================================
// INDEXES FOR RELATIONSHIPS
// ============================================================================

CREATE INDEX implements_relationship IF NOT EXISTS
FOR ()-[r:IMPLEMENTS]-() ON (r.transposition_status);

CREATE INDEX references_relationship IF NOT EXISTS
FOR ()-[r:REFERENCES]-() ON (r.reference_type);

CREATE INDEX supersedes_relationship IF NOT EXISTS
FOR ()-[r:SUPERSEDES]-() ON (r.amendment_type);

// ============================================================================
// SAMPLE DATA (Exemplary Entities for Testing)
// ============================================================================

// 1. EU Regulation on Social Security Coordination
CREATE (eureg:EURegulation:EULaw {
  eli_uri: "eli:eu:reg:2004:883",
  celex_number: "32004R0883",
  title_de: "Verordnung (EG) Nr. 883/2004 des Europäischen Parlaments und des Rates vom 29. April 2004 über die Koordinierung der Systeme der sozialen Sicherheit",
  title_en: "Regulation (EC) No 883/2004 of the European Parliament and of the Council on the coordination of social security systems",
  date_document: date("2004-04-29"),
  first_date_entry_in_force: date("2010-05-01"),
  ojeu_reference: "OJ L 166, 30.4.2004, p. 1",
  policy_area: "social_affairs",
  completeness_score: 0.95,
  validation_status: "passed",
  source_type: "official",
  version_status: "current",
  last_update: date("2024-10-20")
});

// 2. German SGB VI (Pension Insurance)
CREATE (sgbvi:SocialLawBook:GermanLaw {
  eli_uri: "eli:de:sgb:6",
  internal_id: "SGB-VI",
  book_number: "VI",
  book_roman_numeral: "VI",
  title_de: "Sechstes Buch Sozialgesetzbuch - Gesetzliche Rentenversicherung",
  title_en: "Social Code Book VI - Statutory Pension Insurance",
  official_name: "SGB VI",
  date_document: date("1992-12-18"),
  first_date_entry_in_force: date("1992-01-01"),
  bgbl_reference: "BGBl 1992 I Nr. 2, p. 2257",
  policy_area: "social_affairs",
  authority_name: "Deutsche Rentenversicherung",
  article_count: 300,
  completeness_score: 0.93,
  validation_status: "passed",
  source_type: "official",
  version_status: "current",
  last_update: date("2024-10-20")
});

// 3. SGB VI § 43 (Disability Pension)
CREATE (art43:Article:LegalDocument {
  eli_uri: "eli:de:sgb:6:43:2023-03-01",
  internal_id: "SGB-VI-43",
  article_number: "43",
  title_de: "Anspruch auf Rente wegen Erwerbsminderung",
  title_en: "Entitlement to Disability Pension",
  date_document: date("2023-03-01"),
  first_date_entry_in_force: date("2023-04-01"),
  policy_area: "social_affairs",
  article_type: "eligibility",
  compliance_cost_category: "medium",
  affected_business_processes: ["Disability pension application", "Medical assessment"],
  enforcement_mechanism: ["administrative_appeal", "court_review"],
  penalty_type: "administrative_fine",
  statute_of_limitations: 4,
  completeness_score: 0.92,
  validation_status: "passed",
  source_type: "official",
  version_status: "current",
  last_update: date("2024-10-20")
});

// 4. EuroVoc Concept: Pension Insurance
CREATE (concept4530:LegalConcept:EuroVocConcept {
  eurovoc_id: "4530",
  concept_type: "concept",
  pref_label_de: "Rentenversicherung",
  pref_label_en: "Pension insurance",
  pref_label_fr: "Assurance-pension",
  pref_label_es: "Seguro de pensiones",
  pref_label_it: "Assicurazione pensionistica",
  pref_label_pl: "Ubezpieczenie emerytalne",
  alt_labels_de: ["Altersrente", "Erwerbsminderungsrente"],
  alt_labels_en: ["Old-age pension", "Disability pension"],
  domain_code: "28",
  domain_label: "Soziale Fragen / Social matters",
  microthesaurus_code: "2821",
  microthesaurus_label: "Soziale Sicherheit / Social security",
  scope_note_de: "Versicherungssystem zur Gewährung von Renten für Altersversorgung, Erwerbsunfähigkeit und Hinterbliebenenversorgung.",
  scope_note_en: "Insurance scheme providing income replacement for retirement, disability, and survivor benefits.",
  has_narrower: true,
  has_broader: true,
  has_related: true,
  last_modified: date("2024-09-15"),
  status: "active"
});

// 5. Court: Bundesgerichtshof (BGH)
CREATE (bgh:Court:Authority {
  authority_id: "BGH",
  authority_name: "Bundesgerichtshof",
  country_code: "DE",
  court_code: "BGH",
  jurisdiction: "federal",
  court_type: "supreme",
  competence_areas: ["Civil law", "Criminal law", "Commercial law"]
});

// 6. Sample Court Decision
CREATE (decision:CourtDecision {
  ecli: "ECLI:DE:BGH:2023:120723U2STR456.22.0",
  decision_type: "Urteil",
  decision_date: date("2023-07-12"),
  title: "BGH Urteil vom 12.07.2023 - 2 StR 456/22",
  summary: "Decision on criminal procedure law and pension entitlements",
  language: "deu"
});

// 7. Authority: Deutsche Rentenversicherung
CREATE (drv:Authority {
  authority_id: "DRV",
  authority_name: "Deutsche Rentenversicherung",
  authority_short_name: "DRV",
  jurisdiction_level: "federal",
  country_code: "DE",
  agency_type: "social_insurance_agency",
  enforcement_scope: ["Pension insurance", "Rehabilitation", "Occupational health"]
});

// 8. Business Process: Disability Pension Application
CREATE (process:BusinessProcess {
  process_id: "DRV-P-001",
  process_name: "Antrag auf Erwerbsminderungsrente",
  process_name_en: "Application for Disability Pension",
  authority_id: "DRV",
  authority_name: "Deutsche Rentenversicherung",
  average_duration_days: 90,
  annual_volume: 45000,
  processing_steps: [
    "Application receipt",
    "Insurance history review",
    "Medical examination",
    "Income assessment",
    "Pension decision notification"
  ]
});

// 9. Temporal Version (Previous version of SGB VI § 43)
CREATE (oldversion:TemporalVersion {
  version_date: date("2022-01-01"),
  amendment_type: "substantive",
  amendment_description: "Reduced waiting period from 5 to 3 years"
});

// ============================================================================
// RELATIONSHIPS FOR SAMPLE DATA
// ============================================================================

// SGB VI § 43 part of SGB VI
CREATE (art43)-[:PART_OF]->(sgbvi);

// Article 43 concerns pension insurance concept
CREATE (art43)-[:CONCERNS {relevance_score: 0.98}]->(concept4530);

// SGB VI coordinates with EU Regulation 883/2004
CREATE (sgbvi)-[:COORDINATES_WITH {
  coordination_area: "Cross-border pension rights",
  articles_affected: ["Art. 6", "Art. 52"]
}]->(eureg);

// Article 43 impacts disability pension process
CREATE (art43)-[:IMPACTS {
  impact_type: "eligibility_criteria",
  affected_population: 320000,
  change_probability: "medium"
}]->(process);

// Process based on Article 43
CREATE (process)-[:BASED_ON]->(art43);

// Court decision interprets Article 43
CREATE (decision)-[:INTERPRETS]->(art43);

// Court operated by BGH
CREATE (decision)-[:DECIDED_BY]->(bgh);

// SGB VI administered by DRV
CREATE (sgbvi)-[:ADMINISTERED_BY {primary_responsibility: true}]->(drv);

// Previous version relationship
CREATE (art43)-[:SUPERSEDES {
  superseded_date: date("2023-03-01"),
  amendment_type: "substantive"
}]->(oldversion);

// ============================================================================
// VALIDATION QUERIES (Example)
// ============================================================================

// Count nodes by type
MATCH (n)
RETURN labels(n) as NodeType, count(n) as Count
ORDER BY Count DESC;

// Find all amendments to SGB VI § 43
MATCH path = (current:Article {article_number: "43"})
       -[:SUPERSEDES*]->(historical)
RETURN current.title_de, [v IN nodes(path) | v.version_date] as amendment_history;

// Find implementing German laws for EU regulations
MATCH (directive:EUDirective {policy_area: "social_affairs"})
       -[:IMPLEMENTED_BY]->(german:GermanLaw)
RETURN directive.title_de, collect(german.title_de) as implementing_laws;

// Find all articles concerning pension insurance
MATCH (article:Article)-[:CONCERNS {relevance_score: score}]->(concept:LegalConcept {eurovoc_id: "4530"})
WHERE score >= 0.7
RETURN article.title_de, article.eli_uri, score
ORDER BY score DESC;

// ============================================================================
// RETURN CONFIRMATION
// ============================================================================

RETURN 'EU GraphRAG comprehensive metadata schema initialized successfully' as Status;
