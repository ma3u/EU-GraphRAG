# EU GraphRAG - Unified Legal Metadata Model

**Last Updated**: November 11, 2025  
**Version**: 1.0  
**Scope**: Comprehensive metadata schema for German federal laws and EU legislation

---

## 1. Executive Summary

This document defines a unified metadata model that accommodates:

- **German Federal Laws** (~5,000 federal laws, SGB I-XII social codes)
- **EU Legislation** (Regulations, Directives, Decisions from EUR-Lex)
- **Multilingual Concepts** (EuroVoc thesaurus with 24 languages)
- **Temporal Versioning** (Amendment history, supersessions)
- **Cross-jurisdictional Relationships** (Transposition, coordination, implementation)

The model is designed to be:
✅ **Normalized** - Reusable across law types  
✅ **Extensible** - Accommodates future law types (state law, case law)  
✅ **RDF-compatible** - Aligns with ELI, ECLI, EuroVoc standards  
✅ **Graph-native** - Optimized for Neo4j property graphs

---

## 2. Core Metadata Dimensions

### 2.1 Identification Metadata

**Purpose**: Unambiguous, standardized identification of legal documents

```yaml
Identification:
  Primary Identifier:
    - eli_uri: String (Mandatory)
      Format: "eli:{jurisdiction}:{type}:{year}:{number}:{subdivision}"
      Examples:
        - "eli:eu:dir:2016:680"           # EU Directive
        - "eli:de:sgb:6:43:2023-03-01"    # German SGB VI § 43
        - "eli:de:bgb:123"                # German Civil Code § 123
    
    - celex_number: String (EU only)
      Format: "YYPNNNNNN{ABC}"
      Example: "32016L0680" (for 2016/680 directive)
    
    - ecli: String (Case law)
      Format: "ECLI:Country:Court:Year:Number:SuffixAsNeeded"
      Example: "ECLI:DE:BGH:2023:120723U2STR456.22.0"
  
  Secondary Identifiers:
    - bgbl_reference: String (German laws)
      Format: "BGBl {Year} I Nr. {Number}, p. {Page}"
      Example: "BGBl 2023 I Nr. 11, p. 1"
    
    - ojeu_reference: String (EU acts)
      Format: "OJ L/C {Year} {Number} {Page}"
      Example: "OJ L 119, 4.5.2016, p. 1"
    
    - internal_id: String (Database)
      Format: Abbreviation + Roman numeral
      Examples: "SGB-VI", "BGB-PART-1"
    
    - legacy_identifiers: Array[String]
      Historical references for deprecated laws
      Example: ["Reg 1408/71", "AltID-2020"]
```

### 2.2 Temporal Metadata

**Purpose**: Track law lifecycle, amendments, versioning

```yaml
Temporal:
  Effective Dates:
    - date_document: Date (Mandatory)
      "Date the legal document was adopted/enacted"
      Example: 2023-03-01
    
    - first_date_entry_in_force: Date (Mandatory)
      "When the law became legally binding"
      Example: 2023-04-01
    
    - date_no_longer_in_force: Date (Optional)
      "When the law was repealed/superseded"
      Example: 2024-01-01
      Status: Null if currently in force
    
    - last_amended: Date (Mandatory)
      "Date of most recent amendment"
      Example: 2024-10-15
  
  Version Management:
    - version_date: Date
      "Specific version snapshot date"
      Use case: Historical analysis (SGB VI as of 2020-06-30)
    
    - amendment_chain: Relationship chain
      (TemporalVersion)-[:SUPERSEDES*]->(HistoricalVersion)
      Links: Current → Prior version → Earlier version...
    
    - amendment_source: String
      "Reference to amending law"
      Example: "BGBl 2024 I Nr. 15"
    
    - amendment_type: Enum
      Values: ["substantive", "technical", "renumbering", "consolidation"]
  
  Transposition Deadlines (EU Directives only):
    - transposition_deadline: Date (Directive specific)
      Example: 2024-12-31
    
    - transposition_status: Enum
      Values: ["on_time", "delayed", "notified_extension", "not_transposed"]
    
    - transposition_date: Date
      "Date German law(s) were actually updated"
```

### 2.3 Organizational/Institutional Metadata

**Purpose**: Track legislative origin, authority, responsibility

```yaml
Institutional:
  Authorship:
    - legislator: Object (Mandatory)
      jurisdiction: String ["EU", "DE", "AT", "FR", ...]
      legislative_body: String
        - EU: "European Parliament", "Council of the EU", "Commission"
        - Germany: "Bundestag", "Bundesrat", "Ministry"
      Example:
        legislator:
          jurisdiction: "DE"
          legislative_body: "Bundestag/Bundesrat"
    
    - adoption_date: Date
      "When legislative body formally adopted"
    
    - sponsoring_ministry: String (German laws)
      Values: "BMJV" (default), "BA", "BMAS", "BMG", "BMF", etc.
  
  Administration & Implementation:
    - responsible_authority: Array[Object]
      authority_id: String (unique code)
      authority_name: String
      jurisdiction_level: Enum ["federal", "state", "municipal", "agency"]
      Examples:
        - {authority_id: "DRV", authority_name: "Deutsche Rentenversicherung"}
        - {authority_id: "BA", authority_name: "Bundesagentur für Arbeit"}
        - {authority_id: "GKV", authority_name: "Gesetzliche Krankenkassen"}
    
    - competent_agency: String
      "Primary agency responsible for implementation"
      Example: "Deutsche Rentenversicherung" for SGB VI
    
    - enforcement_mechanism: Array[String]
      Examples: ["administrative appeal", "court review", "audit", "sanction"]
  
  Coordination (EU Directives):
    - legal_basis_tfeu: String
      "EU Treaty on the Functioning of the EU article"
      Example: "Art. 153 (Social policy)"
    
    - legislative_procedure: Enum
      Values: ["ordinary", "special", "consultation", "consent"]
      "Co-decision procedure used"
    
    - co_legislators: Array[String]
      For ordinary procedure: ["European Parliament", "Council"]
```

### 2.4 Content & Scope Metadata

**Purpose**: Describe what the law covers

```yaml
Content:
  Titles & Names:
    - title_de: String (Mandatory for German laws)
      Example: "Sechstes Buch Sozialgesetzbuch - Rentenversicherung"
    
    - title_en: String (Recommended)
      Example: "Social Code Book VI - Pension Insurance"
    
    - title_original: String
      Official title in language of origin
    
    - short_title: String (Optional)
      Abbreviated name
      Example: "SGB VI", "BGB", "EG-VO 883/2004"
    
    - alternative_titles: Array[String]
      Historical or colloquial names
      Example: ["Rentenversicherungsgesetz", "Invaliden-Versicherungs-Gesetz"]
  
  Subject Matter Classification:
    - subject_matter: Array[Object]
      Hierarchical classification
      Examples:
        - {domain: "Social security", subdomain: "Pension insurance"}
        - {domain: "Labor law", subdomain: "Employment protection"}
    
    - policy_area: String
      Enum: ["social_affairs", "labor", "tax", "commerce", "environment", ...]
    
    - eurovoc_descriptors: Array[Object]
      Links to EuroVoc thesaurus
      - concept_id: String (e.g., "4530")
      - pref_label: Multilingual labels
      - relevance_score: Float [0.0-1.0]
      Example:
        - concept_id: "4530"
          pref_label_de: "Rentenversicherung"
          pref_label_en: "Pension insurance"
          relevance_score: 0.95
  
  Scope & Coverage:
    - geographic_scope: Enum
      Values: ["Germany", "EU27", "EEA", "Global", ...]
    
    - temporal_scope: String
      Describes applicability period
      Example: "From 2024-01-01 onwards"
    
    - sectoral_scope: Array[String]
      Industries/sectors affected
      Examples: ["Healthcare", "Social security", "Labor relations"]
    
    - beneficiary_categories: Array[String]
      Who is affected
      Examples: ["Employees", "Pensioners", "Disabled persons"]
    
    - exception_clauses: Array[String]
      Exemptions and derogations
      Example: ["Small enterprises exempt if <5 employees"]
```

### 2.5 Structural Metadata

**Purpose**: Define internal structure (articles, sections, provisions)

```yaml
Structure:
  Document Hierarchy:
    - level: Enum
      Values: ["document", "book", "chapter", "section", "article", "paragraph", "subparagraph"]
    
    - sequence_number: String
      Organizational structure identifier
      Examples: "I", "II", "§43", "Art. 1(2)", "§1 Abs. 1 S. 2"
    
    - hierarchy_path: String
      Full path from root
      Example: "SGB VI > Book VI > Chapter 5 > § 52"
  
  Parts & Sections:
    - has_parts: Boolean
      Whether document contains distinct books/parts
    
    - part_structure: Array[Object]
      For laws with parts (e.g., SGB I-XII):
      - part_id: String (e.g., "VI")
      - part_title: String (e.g., "Rentenversicherung")
      - part_scope: String
      - article_count: Integer
    
    - annex: Array[String]
      Related documents/appendices
      Example: ["Anlage 1: Klassifizierung", "Anlage 2: Tabellen"]
  
  Granularity:
    - number_of_articles: Integer
      Total substantive provisions
    
    - number_of_sections: Integer (German: "Paragraphen")
      Total §-numbered sections
    
    - number_of_amendments: Integer
      How many times amended
```

### 2.6 Relationship Metadata

**Purpose**: Connect laws across jurisdictions and time

```yaml
Relationships:
  Transposition & Implementation:
    - implements_directive: Array[Object]
      German law implementing EU directive(s)
      - directive_eli: String (e.g., "eli:eu:dir:2014:50")
      - directive_title: String
      - articles_mapped: Array[String]
        Which German law articles implement which directive articles
        Example: [{eu_article: "Art. 2", de_article: "§ 3, § 4"}]
    
    - implemented_by_regulation: Array[Object]
      EU directive implemented by German law(s)
      - regulation_eli: String
      - implementing_laws: Array[String]
      - status: Enum ["fully_implemented", "partially_implemented", "gap_identified"]
    
    - transposition_gap: String (Optional)
      Description of incomplete implementation
      Example: "Art. 5 not transposed; exemption claimed"
  
  Amendment & Supersession:
    - supersedes: String (Foreign key to TemporalVersion)
      Points to previous version
      Relationship direction: newer -> older
    
    - superseded_by: String (Foreign key to TemporalVersion)
      Points to newer version
      Relationship direction: older -> newer
    
    - amending_law: String
      Reference to law that modified this one
      Example: "BGBl 2023 I Nr. 11"
  
  Cross-References:
    - references: Array[Object]
      Links to other laws this law cites
      - target_law: String (ELI)
      - reference_type: Enum ["implements", "requires", "amends", "provides_exception"]
      - article_pairs: Array[{from: String, to: String}]
    
    - referenced_by: Array[String]
      Laws that cite this one
    
    - coordination_with: Array[Object] (EU regulations)
      Related EU/international instruments
      - partner_regulation: String (ELI)
      - coordination_area: String
      - priority_rules: String (Which law takes precedence)
  
  Hierarchical Links:
    - part_of: String (Foreign key)
      Parent code book (e.g., SGB VI is part of "German Social Code")
    
    - repeals: String (Foreign key)
      Previous law that was completely replaced
    
    - amended_by: Array[String]
      List of laws/orders that amended this one
```

### 2.7 Regulatory & Compliance Metadata

**Purpose**: Compliance obligations, enforcement, sanctions

```yaml
Compliance:
  Enforcement:
    - enforcement_authority: String
      "Which agency enforces"
      Example: "Finanzbehörden" (for tax law)
    
    - appeal_mechanism: String
      "How to challenge administrative decisions"
      Example: "Administrative court (VwGO)"
    
    - sanctions: Array[Object]
      Penalties for non-compliance
      - violation_type: String
      - penalty_type: Enum ["fine", "imprisonment", "license_suspension", "administrative_penalty"]
      - penalty_amount_min: Decimal
      - penalty_amount_max: Decimal
      - penalty_unit: Enum ["EUR", "days"]
    
    - statute_of_limitations: Integer
      Years before enforcement time-bars
      Example: 4 (years)
  
  Administrative Burden:
    - compliance_cost_category: Enum
      ["low", "medium", "high"]
      "Estimated compliance effort"
    
    - affected_business_processes: Array[String]
      Which organizational workflows are impacted
      Examples: ["Hiring process", "Payroll", "Tax filing"]
    
    - reporting_obligations: Array[Object]
      Required reports/disclosures
      - report_type: String
      - frequency: String (daily, monthly, annual)
      - recipient: String
      - format: String (electronic, paper, both)
    
    - data_retention: Object
      record_retention_period: Integer (months)
      Example: 36 months for tax records
```

### 2.8 Quality & Metadata Management

**Purpose**: Track data quality, completeness, and source reliability

```yaml
Quality:
  Data Completeness:
    - completeness_score: Float [0.0-1.0]
      "Percentage of metadata fields populated"
      Example: 0.92 (92% complete)
    
    - data_quality_issues: Array[String]
      Known gaps or inconsistencies
      Example: ["Missing English translation", "BGBl reference not yet available"]
    
    - validation_status: Enum
      Values: ["not_validated", "pending", "passed", "failed"]
    
    - validated_by: String
      "Entity/process that validated"
      Example: "BMJV documentation team"
    
    - validation_date: Date
  
  Source Reliability:
    - source_type: Enum
      Values: ["official", "semi-official", "third-party", "user-contributed"]
      Example: "official" for Gesetze im Internet
    
    - authoritative_source: Object
      official_name: String
      url: String
      publisher: String
      Example:
        official_name: "Gesetze im Internet"
        url: "https://www.gesetze-im-internet.de"
        publisher: "Bundesministerium der Justiz"
    
    - version_status: Enum
      Values: ["current", "historical", "superseded", "proposed", "draft"]
  
  Maintenance & Updates:
    - last_update: Date (Mandatory)
      "When metadata was last updated"
    
    - next_review: Date
      "Scheduled review/update date"
    
    - update_frequency: String
      "How often metadata is refreshed"
      Example: "Weekly"
    
    - change_log: Array[Object]
      History of metadata changes
      - change_date: Date
      - changed_by: String (user/system)
      - change_type: String (e.g., "added_translation", "corrected_reference")
      - description: String
```

### 2.9 Multilingual Metadata

**Purpose**: Support all 24 EU languages + German

```yaml
Multilingual:
  Languages Supported:
    - language_codes: Array[String]
      ISO 639-1 codes: ["de", "en", "fr", "es", "it", "pl", ...]
    
    - available_translations: Array[Object]
      Which fields are translated
      - field_name: String
      - available_languages: Array[String]
      - translation_status: Enum ["complete", "partial", "draft", "missing"]
      Example:
        - field_name: "title"
          available_languages: ["de", "en", "fr"]
          translation_status: "complete"
    
    - translation_quality: Object
      machine_translated: Boolean
      professional_translation: Boolean
      certified_translation: Boolean
      translator_credentials: String (Optional)
  
  Language-Specific Properties:
    - title@{language}: String
      Examples: title@de, title@en, title@fr, ...
    
    - description@{language}: String (Optional)
      Multilingual descriptions
    
    - concept_labels: Array[Object] (For EuroVoc concepts)
      Each concept has labels in all supported languages
      - pref_label@de: "Rentenversicherung"
      - pref_label@en: "Pension insurance"
      - alt_label@de: "Altersrente", "Erwerbsminderungsrente"
      - scope_note@{language}: Translations of definition
```

---

## 3. Metadata Model Constraints & Validations

### 3.1 Mandatory Fields by Law Type

```yaml
Mandatory_Fields_All_Laws:
  - eli_uri (must be unique)
  - title_de or title_en
  - date_document
  - first_date_entry_in_force
  - policy_area
  - source_type
  - last_update

Mandatory_Fields_German_Laws:
  - bgbl_reference (for laws, not regulations)
  - responsible_authority (minimum 1)
  - policy_area

Mandatory_Fields_EU_Laws:
  - celex_number (unique)
  - ojeu_reference
  - legal_basis_tfeu (for directives, decisions)
  - legislative_procedure

Mandatory_Fields_EU_Directives:
  - transposition_deadline
  - transposition_status
```

### 3.2 Validation Rules

```cypher
// Example Cypher constraints to enforce metadata quality

// 1. ELI URI format validation
CREATE CONSTRAINT eli_uri_format
  FOR (n:LegalDocument)
  REQUIRE n.eli_uri MATCHES 'eli:[a-z]{2}(:[a-z]+){3}(:[0-9]{4}-[0-9]{2}-[0-9]{2})?'

// 2. Unique identifiers
CREATE CONSTRAINT eli_uri_unique
  FOR (n:LegalDocument) REQUIRE n.eli_uri IS UNIQUE

CREATE CONSTRAINT celex_unique
  FOR (n:EULaw) REQUIRE n.celex_number IS UNIQUE

// 3. Temporal consistency
MATCH (d:LegalDocument)
WHERE d.first_date_entry_in_force < d.date_document
RETURN "VALIDATION ERROR: Entry into force before adoption" as error

// 4. Reference validity
MATCH (doc:LegalDocument)-[:IMPLEMENTS]->(target:LegalDocument)
WHERE target.policy_area NOT IN ['social_affairs', 'labor', ...]
RETURN "WARNING: IMPLEMENTS links to unexpected policy area" as warning
```

### 3.3 Data Quality Rules

```yaml
Quality_Standards:
  Completeness:
    - German laws: Minimum 80% field completion
    - EU laws: Minimum 85% field completion
    - Translations: At least German + English
  
  Accuracy:
    - Date fields: Must be ISO 8601 format
    - Identifiers: Must be validatable against official sources
    - References: Must point to existing documents
  
  Consistency:
    - No contradictory amendment chains
    - Version dates must be chronological
    - SUPERSEDES relationships must form valid DAGs (directed acyclic graphs)
  
  Timeliness:
    - German laws: Update within 7 days of BGBl publication
    - EU laws: Update within 24 hours of official journal
    - EuroVoc: Update within 30 days of new releases
```

---

## 4. Metadata Model in Graph Form (Neo4j)

### 4.1 Node Types

```cypher
// All legal documents inherit from base node
CREATE (doc:LegalDocument {
  eli_uri: STRING UNIQUE,
  title_de: STRING,
  title_en: STRING,
  date_document: DATE,
  first_date_entry_in_force: DATE,
  last_amended: DATE,
  policy_area: STRING,
  source_type: STRING,
  last_update: DATE,
  completeness_score: FLOAT
})

// Specialized nodes for different law types
CREATE (sgb:SocialLawBook:LegalDocument {
  book_number: STRING UNIQUE,
  authority: STRING,
  scope: STRING
})

CREATE (eu_law:EULaw:LegalDocument {
  celex_number: STRING UNIQUE,
  legal_basis_tfeu: STRING,
  legislative_procedure: STRING
})

CREATE (german_law:GermanLaw:LegalDocument {
  bgbl_reference: STRING,
  responsible_authority: STRING
})

CREATE (directive:EUDirective:EULaw {
  transposition_deadline: DATE,
  transposition_status: STRING
})

// Temporal versioning nodes
CREATE (version:TemporalVersion {
  version_date: DATE,
  version_text: STRING,
  amendment_source: STRING
})

// Organizational actors
CREATE (authority:Authority {
  authority_id: STRING UNIQUE,
  authority_name: STRING,
  jurisdiction_level: STRING,
  agency_code: STRING
})

// EuroVoc concepts
CREATE (concept:LegalConcept:EuroVocConcept {
  eurovoc_id: STRING UNIQUE,
  pref_label_de: STRING,
  pref_label_en: STRING,
  domain_code: STRING
})
```

### 4.2 Relationship Types

```cypher
// Hierarchical relationships
(Law)-[:HAS_PART]->(Chapter)
(Chapter)-[:HAS_SECTION]->(Article)
(SGB)-[:PART_OF]->(GermanSocialCode)

// Temporal relationships
(NewVersion)-[:SUPERSEDES]->(OldVersion)
(Amendment)-[:AMENDS]->(Document)

// Transposition relationships
(German Law)-[:IMPLEMENTS]->(EU Directive)
(EU Directive)-[:IMPLEMENTED_BY]->(German Law)

// Cross-references
(Article)-[:REFERENCES]->(Article)
(Law)-[:REFERENCES]->(Law)
(Law)-[:COORDINATES_WITH]->(EU Regulation)

// Classification relationships
(Document)-[:HAS_SUBJECT_MATTER]->(Subject)
(Document)-[:CONCERNS]->(EuroVocConcept)

// Administrative relationships
(Document)-[:ADMINISTERED_BY]->(Authority)
(Document)-[:ENFORCED_BY]->(Authority)

// Amendment chain
(Law)-[:AMENDED_BY]->(AmendingAct)
(Law)-[:REPEALS]->(RepeatedLaw)
```

---

## 5. Metadata Model Examples

### Example 1: German Law (SGB VI § 43)

```json
{
  "eli_uri": "eli:de:sgb:6:43:2023-03-01",
  "internal_id": "SGB-VI-43",
  "titles": {
    "de": "Sechstes Buch Sozialgesetzbuch - Rentenversicherung - Anspruch auf Rente wegen Erwerbsminderung",
    "en": "Social Code Book VI - Statutory Pension Insurance - Entitlement to Disability Pension"
  },
  "identification": {
    "bgbl_reference": "BGBl 2023 I Nr. 11, p. 1",
    "celex_number": null,
    "short_title": "SGB VI § 43"
  },
  "temporal": {
    "date_document": "2023-03-01",
    "first_date_entry_in_force": "2023-04-01",
    "last_amended": "2024-10-15",
    "date_no_longer_in_force": null,
    "version_date": "2023-03-01",
    "amendment_chain": ["BGBl 2024 I Nr. 15", "BGBl 2023 I Nr. 11"],
    "amendment_type": "substantive"
  },
  "institutional": {
    "legislator": {
      "jurisdiction": "DE",
      "legislative_body": "Bundestag/Bundesrat"
    },
    "responsible_authority": {
      "authority_id": "DRV",
      "authority_name": "Deutsche Rentenversicherung",
      "jurisdiction_level": "federal"
    }
  },
  "content": {
    "policy_area": "social_affairs",
    "subject_matter": {
      "domain": "Social security",
      "subdomain": "Pension insurance"
    },
    "eurovoc_descriptors": [
      {
        "concept_id": "4531",
        "pref_label_de": "Erwerbsminderungsrente",
        "pref_label_en": "Disability pension",
        "relevance_score": 0.98
      }
    ],
    "geographic_scope": "Germany",
    "beneficiary_categories": [
      "Employees with reduced earning capacity",
      "Self-employed persons"
    ],
    "exception_clauses": [
      "Exemption for civil servants (separate beamtenversorgung)",
      "Different rules for artists/publishers"
    ]
  },
  "structure": {
    "level": "article",
    "sequence_number": "§ 43",
    "hierarchy_path": "SGB VI > Book VI > Chapter 2 > § 43",
    "article_count": 1
  },
  "relationships": {
    "implements_directive": [],
    "implemented_by_regulation": [],
    "references": [
      {
        "target_law": "eli:de:sgb:6:42",
        "reference_type": "provides_exception",
        "article_pairs": [{"from": "§43 Abs. 1", "to": "§42"}]
      }
    ],
    "coordination_with": [
      {
        "partner_regulation": "eli:eu:reg:2004:883",
        "coordination_area": "Cross-border pension eligibility",
        "priority_rules": "EU Regulation takes precedence for EU citizens"
      }
    ]
  },
  "compliance": {
    "enforcement_authority": "Deutsche Rentenversicherung",
    "appeal_mechanism": "Administrative court (VwGO § 40)",
    "affected_business_processes": [
      "Disability pension application",
      "Medical assessment process"
    ],
    "reporting_obligations": [
      {
        "report_type": "Medical examination report (Gutachten)",
        "frequency": "Per case",
        "recipient": "DRV"
      }
    ]
  },
  "quality": {
    "completeness_score": 0.94,
    "data_quality_issues": [],
    "validation_status": "passed",
    "validated_by": "BMJV documentation team",
    "validation_date": "2024-10-20",
    "source_type": "official",
    "authoritative_source": {
      "official_name": "Gesetze im Internet",
      "url": "https://www.gesetze-im-internet.de/sgb_6",
      "publisher": "Bundesministerium der Justiz"
    },
    "version_status": "current",
    "last_update": "2024-10-20",
    "next_review": "2024-12-31",
    "update_frequency": "Weekly"
  },
  "multilingual": {
    "languages_supported": ["de", "en"],
    "available_translations": [
      {
        "field_name": "title",
        "available_languages": ["de", "en"],
        "translation_status": "complete"
      }
    ],
    "translation_quality": {
      "machine_translated": false,
      "professional_translation": true,
      "certified_translation": false
    }
  }
}
```

### Example 2: EU Directive (2014/50/EU)

```json
{
  "eli_uri": "eli:eu:dir:2014:50",
  "titles": {
    "de": "Richtlinie 2014/50/EU über Rechte der Arbeitnehmer im Falle von Unternehmensübergängen",
    "en": "Directive 2014/50/EU on the rights of workers in an insolvency",
    "fr": "Directive 2014/50/UE relative aux droits des travailleurs en cas de transfert d'entreprise"
  },
  "identification": {
    "eli_uri": "eli:eu:dir:2014:50",
    "celex_number": "32014L0050",
    "ojeu_reference": "OJ L 130, 1.5.2014, p. 1",
    "short_title": "Posted Workers Directive"
  },
  "temporal": {
    "date_document": "2014-04-16",
    "first_date_entry_in_force": "2014-05-01",
    "last_amended": "2018-06-28",
    "transposition_deadline": "2016-04-30",
    "transposition_status": "on_time",
    "transposition_date": "2016-04-15"
  },
  "institutional": {
    "legislator": {
      "jurisdiction": "EU",
      "legislative_body": ["European Parliament", "Council of the EU"]
    },
    "legal_basis_tfeu": "Art. 153 TFEU (Social policy)",
    "legislative_procedure": "ordinary",
    "co_legislators": ["European Parliament", "Council"]
  },
  "content": {
    "title_de": "Richtlinie 2014/50/EU über Rechte der Arbeitnehmer bei Betriebsübergängen",
    "policy_area": "labor",
    "subject_matter": {
      "domain": "Employment & Labor",
      "subdomain": "Worker protection"
    },
    "eurovoc_descriptors": [
      {
        "concept_id": "2005",
        "pref_label_de": "Arbeitsrecht",
        "pref_label_en": "Labor law",
        "relevance_score": 0.95
      },
      {
        "concept_id": "2831",
        "pref_label_de": "Betriebsübergang",
        "pref_label_en": "Takeover of business",
        "relevance_score": 0.92
      }
    ],
    "geographic_scope": "EU27"
  },
  "relationships": {
    "implemented_by_regulation": [
      {
        "member_state": "Germany",
        "implementing_law": "eli:de:agc:2016:aentg",
        "implementing_law_title": "Arbeitnehmer-Entsendegesetz",
        "status": "fully_implemented",
        "articles_mapped": [
          {"eu_article": "Art. 2", "de_law": "§ 3 AEntG"},
          {"eu_article": "Art. 3", "de_law": "§ 4-6 AEntG"}
        ]
      }
    ]
  },
  "quality": {
    "completeness_score": 0.96,
    "source_type": "official",
    "version_status": "current",
    "last_update": "2024-10-20"
  }
}
```

### Example 3: EuroVoc Concept (Pension Insurance)

```json
{
  "concept_id": "4530",
  "eurovoc_concept_type": "concept",
  "preferred_labels": {
    "de": "Rentenversicherung",
    "en": "Pension insurance",
    "fr": "Assurance-pension",
    "es": "Seguro de pensiones",
    "it": "Assicurazione pensionistica",
    "pl": "Ubezpieczenie emerytalne",
    "pt": "Seguro de pensões",
    "nl": "Pensioenversekering",
    "sv": "Pensionsförsäkring",
    "da": "Pensionsforsikring",
    "fi": "Eläkevakuutus",
    "cs": "Důchodové pojištění",
    "hu": "Nyugdíjbiztosítás",
    "ro": "Asigurări de pensii",
    "sk": "Dôchodkové poistenie",
    "sl": "Pokojninsko zavarovanje",
    "bg": "Пенсионно осигуряване",
    "hr": "Mirovinsko osiguranje",
    "et": "Pensionikindlustus",
    "el": "Ασφάλιση συνταξιοδότησης",
    "lt": "Pensijų draudimas",
    "lv": "Pensiju apdraudze",
    "mt": "Assigurazzjoni tal-pensjoni"
  },
  "alternative_labels": {
    "de": ["Altersrente", "Erwerbsminderungsrente", "Hinterbliebenenrente"],
    "en": ["Old-age pension", "Disability pension", "Survivor pension"]
  },
  "scope_note": {
    "de": "Versicherungssystem zur Gewährung von Renten für Altersversorgung, Erwerbsunfähigkeit und Hinterbliebenenversorgung.",
    "en": "Insurance scheme providing income replacement for retirement, disability, and survivor benefits."
  },
  "domain": {
    "domain_id": "28",
    "domain_label": "Soziale Fragen / Social matters"
  },
  "microthesaurus": {
    "microthesaurus_id": "2821",
    "microthesaurus_label": "Social security / Sécurité sociale"
  },
  "narrower_concepts": [
    {
      "concept_id": "4531",
      "label_de": "Erwerbsminderungsrente",
      "label_en": "Disability pension"
    },
    {
      "concept_id": "4532",
      "label_de": "Altersrente",
      "label_en": "Old-age pension"
    }
  ],
  "broader_concept": {
    "concept_id": "2821",
    "label_de": "Soziale Sicherheit",
    "label_en": "Social security"
  },
  "related_concepts": [
    {
      "concept_id": "2895",
      "label_de": "Krankenversicherung",
      "label_en": "Health insurance"
    },
    {
      "concept_id": "446",
      "label_de": "Arbeitslosengeld",
      "label_en": "Unemployment benefit"
    }
  ]
}
```

---

## 6. Implementation Roadmap

### Phase 1: Schema Foundation (✅ Complete)
- Define metadata model (this document)
- Map to ELI, ECLI, EuroVoc standards
- Create Neo4j node/relationship definitions

### Phase 2: Data Ingestion (In Progress)
- Scrape gesetze-im-internet.de (~5,000 laws)
- Query EUR-Lex SPARQL endpoint
- Import EuroVoc thesaurus
- Extract and validate metadata for ~500 sample laws

### Phase 3: Quality Assurance (Planned)
- Validate metadata completeness against constraints
- Cross-check identifiers against official sources
- Link German laws to EU directives via IMPLEMENTS relationships
- Resolve references and create transposition mappings

### Phase 4: Graph Enrichment (Planned)
- Generate embeddings for articles
- Build amendment history chains
- Create concept clusters via Neo4j GDS
- Implement hybrid retrieval (vector + graph traversal)

---

## 7. Tool & API Integration Points

### For Developers

```python
# Example: Access metadata via GraphQL/REST API

GET /api/v1/laws/eli:de:sgb:6:43:2023-03-01
Response:
{
  "eli_uri": "eli:de:sgb:6:43:2023-03-01",
  "title_de": "...",
  "temporal": {...},
  "relationships": {
    "implements": [],
    "supersedes": "eli:de:sgb:6:43:2022-01-01",
    "coordinates_with": ["eli:eu:reg:2004:883"]
  }
}

# Query multiple laws with filters
GET /api/v1/laws?policy_area=social_affairs&author ity=DRV&date_from=2023-01-01

# Get amendment history
GET /api/v1/laws/eli:de:sgb:6:43/history

# Find implementing regulations for EU directive
GET /api/v1/directives/eli:eu:dir:2014:50/implementations
```

---

## 8. Quality Assurance Checklist

- [ ] All mandatory fields populated
- [ ] ELI URIs validated (unique, correct format)
- [ ] Temporal consistency verified (dates chronological)
- [ ] References point to valid documents
- [ ] IMPLEMENTS relationships map to actual transpositions
- [ ] SUPERSEDES chains form valid DAGs
- [ ] Translations completed for title + description
- [ ] EuroVoc concepts linked (relevance_score >= 0.7)
- [ ] Source reliability verified
- [ ] Completeness score >= 80% (German) or 85% (EU)

---

## 9. Conclusion

This unified metadata model provides a comprehensive, standardized framework for representing German federal laws and EU legislation in a knowledge graph. It accommodates:

✅ Multiple law types (statutes, directives, regulations)  
✅ Temporal versioning and amendment chains  
✅ Cross-jurisdictional relationships (transposition, coordination)  
✅ Multilingual content (24 EU languages)  
✅ Quality metadata (completeness, source reliability)  
✅ RDF/semantic web compatibility (ELI, ECLI, EuroVoc standards)

The model is **extensible** for future law types (state law, local regulations, case law) and provides a solid foundation for implementing intelligent GraphRAG retrieval and compliance analytics.

