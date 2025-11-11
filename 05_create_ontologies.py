
# Create ontology specification files
import os

# Create comprehensive ontology YAML files with EU and German legal ontologies
ontology_files = {}

# 1. ELI Ontology Specification
ontology_files['eli-core.yaml'] = """# ELI (European Legislation Identifier) Core Ontology
# Based on: http://data.europa.eu/eli/ontology

version: "1.0"
namespace: "http://data.europa.eu/eli/ontology#"
prefix: "eli"

description: |
  The ELI ontology provides a common data model for exchanging legislation metadata 
  on the web. It supports the FRBR model (Work, Expression, Manifestation, Item).

classes:
  - name: LegalResource
    description: Abstract base class for all legal resources
    properties:
      - title: string (multilingual)
      - date_document: date
      - type_document: string
      - is_about: LegalConcept[]
      
  - name: Work
    parent: LegalResource
    description: Abstract legal act (language-independent)
    properties:
      - eli_uri: IRI (unique identifier)
      - date_document: date
      - passed_by: Organization
      - publisher: Organization
      - in_force: boolean
      - first_date_entry_in_force: date
      - date_no_longer_in_force: date
    example: "eli:dir:2016:680"
      
  - name: Expression
    parent: LegalResource
    description: Language version of a Work
    properties:
      - eli_uri: IRI
      - language: ISO_639_1_code
      - date_publication: date
      - title: string
      - id_local: string
      - realizes: Work (mandatory)
    example: "eli:dir:2016:680:oj"
      
  - name: Manifestation
    parent: LegalResource
    description: Format version (HTML, PDF, XML)
    properties:
      - eli_uri: IRI
      - format: MIME_type
      - embodies: Expression (mandatory)
    example: "eli:dir:2016:680:oj:deu:html"
      
  - name: Item
    parent: LegalResource
    description: Physical/digital instance
    properties:
      - access_url: URL
      - exemplifies: Manifestation (mandatory)

relationships:
  - name: realizes
    domain: Expression
    range: Work
    description: Expression realizes a Work
    
  - name: embodies
    domain: Manifestation
    range: Expression
    description: Manifestation embodies an Expression
    
  - name: exemplifies
    domain: Item
    range: Manifestation
    description: Item exemplifies a Manifestation
    
  - name: cites
    domain: LegalResource
    range: LegalResource
    description: Legal resource cites another
    
  - name: amends
    domain: LegalResource
    range: LegalResource
    description: Legal resource amends another
    
  - name: repeals
    domain: LegalResource
    range: LegalResource
    description: Legal resource repeals another
    
  - name: based_on
    domain: LegalResource
    range: LegalResource
    description: Legal resource is based on another (e.g., national law implements EU directive)
    
  - name: transposes
    domain: Work
    range: Work
    description: National legislation transposes EU directive

# ELI URI Structure
uri_template: |
  {jurisdiction}/{type}/{year}/{natural_number}[/{point_in_time}][/{version}][/{language}][/{format}]
  
  Examples:
  - eli:eu:dir:2016:680 (EU Directive 2016/680)
  - eli:de:bgb:§:123 (German Civil Code § 123)
  - eli:de:sgb:6:43:2023-03-01 (SGB VI § 43, version from 2023-03-01)
"""

# 2. ECLI Ontology
ontology_files['ecli-core.yaml'] = """# ECLI (European Case Law Identifier) Ontology
# Based on: Council Conclusions on ECLI (2011)

version: "1.0"
namespace: "http://data.europa.eu/ecli/ontology#"
prefix: "ecli"

description: |
  ECLI provides uniform identifiers for court decisions across Europe.
  Format: ECLI:{country}:{court}:{year}:{ordinal_number}

classes:
  - name: CourtDecision
    description: Judicial decision from any court
    properties:
      - ecli: string (unique identifier)
      - title: string
      - decision_date: date
      - decision_type: enum [judgment, order, conclusion, opinion]
      - language: ISO_639_1_code
      - creator: Court (mandatory)
      - subject: LegalConcept[]
      - references: LegalResource[]
      - is_about: LegalMatter
    example: "ECLI:DE:BGH:2023:120723U2STR456.22.0"
    
  - name: Court
    description: Judicial organization
    properties:
      - name: string
      - court_code: string
      - country_code: ISO_3166_1_alpha_2
      - jurisdiction: enum [federal, state, regional, local]
      - court_type: enum [supreme, constitutional, administrative, civil, criminal, social, tax]
    example: 
      name: "Bundesgerichtshof"
      court_code: "BGH"
      country_code: "DE"
      
  - name: LegalMatter
    description: Subject matter of case
    properties:
      - matter_id: string
      - description: string
      - legal_area: EuroVoc_descriptor

relationships:
  - name: decided_by
    domain: CourtDecision
    range: Court
    
  - name: cites_legislation
    domain: CourtDecision
    range: LegalResource
    properties:
      - article_number: string
      - citation_context: string
      
  - name: cites_case
    domain: CourtDecision
    range: CourtDecision
    description: Case law citation
    
  - name: overturns
    domain: CourtDecision
    range: CourtDecision
    description: Higher court overturns lower court decision
    
  - name: confirms
    domain: CourtDecision
    range: CourtDecision
    description: Higher court confirms lower court decision

# ECLI Identifier Structure
ecli_template: |
  ECLI:{country_code}:{court_code}:{year}:{ordinal_number}
  
  Country codes: ISO 3166-1 alpha-2 (DE, FR, NL, etc.)
  Court codes: Defined by each Member State
  Year: 4 digits
  Ordinal number: Up to 25 alphanumeric characters (dots allowed)
  
  Examples:
  - ECLI:DE:BGH:2023:120723U2STR456.22.0 (German Federal Court of Justice)
  - ECLI:DE:BVerfG:2023:rk20231201.1bvr000123 (German Constitutional Court)
  - ECLI:NL:HR:2009:384425 (Dutch Supreme Court)

# Metadata (Dublin Core)
required_metadata:
  - identifier: ECLI
  - type: decision_type
  - date: decision_date
  - creator: court
  - language: primary_language

optional_metadata:
  - title: case_name
  - subject: eurovoc_descriptors
  - references: cited_legislation
  - description: summary
  - coverage: territorial_scope
"""

# 3. EuroVoc Thesaurus
ontology_files['eurovoc-core.yaml'] = """# EuroVoc Multilingual Thesaurus
# Based on: EU Publications Office controlled vocabulary

version: "4.9"
namespace: "http://eurovoc.europa.eu/"
prefix: "eurovoc"

description: |
  EuroVoc is a multilingual, multidisciplinary thesaurus covering EU activities.
  Contains ~7,000 concepts in 24 EU languages organized into 21 domains.

domains:
  - code: "04"
    label_en: "politics"
    label_de: "Politik"
    microthesauri: ["0406", "0411", "0416", "0421", "0426", "0431", "0436"]
    
  - code: "12"
    label_en: "law"
    label_de: "Recht"
    microthesauri: ["1206", "1211", "1216", "1221", "1226", "1231", "1236"]
    subdomains:
      - code: "1206"
        label_en: "labour law"
        label_de: "Arbeitsrecht"
      - code: "1211"
        label_en: "civil law"
        label_de: "Zivilrecht"
      - code: "1216"
        label_en: "criminal law"
        label_de: "Strafrecht"
      - code: "1221"
        label_en: "justice"
        label_de: "Justiz"
      - code: "1226"
        label_en: "organisation of the legal system"
        label_de: "Gerichtsorganisation"
      - code: "1231"
        label_en: "international law"
        label_de: "Internationales Recht"
      - code: "1236"
        label_en: "EU law"
        label_de: "EU-Recht"
        
  - code: "28"
    label_en: "social questions"
    label_de: "Soziale Fragen"
    microthesauri: ["2806", "2811", "2816", "2821", "2826", "2831", "2836", "2841", "2846"]

classes:
  - name: Concept
    description: EuroVoc descriptor (controlled term)
    properties:
      - concept_id: string (eurovoc_id)
      - pref_label: string (multilingual, 24 languages)
      - alt_label: string[] (synonyms, multilingual)
      - definition: string (multilingual)
      - scope_note: string (usage guidance)
      - domain: Domain
      - microthesaurus: MicroThesaurus
    example:
      concept_id: "3141"
      pref_label_en: "employment contract"
      pref_label_de: "Arbeitsvertrag"
      pref_label_fr: "contrat de travail"
      alt_label_de: ["Dienstvertrag", "Anstellungsvertrag"]
      
  - name: Domain
    description: Top-level thematic area
    properties:
      - code: string (2 digits)
      - label: string (multilingual)
      
  - name: MicroThesaurus
    description: Fine-grained subcategory within a domain
    properties:
      - code: string (4 digits)
      - label: string (multilingual)
      - belongs_to: Domain

relationships:
  - name: broader_than
    description: Hierarchical relationship (parent concept)
    domain: Concept
    range: Concept
    example: "social_security broader_than pension_insurance"
    
  - name: narrower_than
    description: Hierarchical relationship (child concept)
    domain: Concept
    range: Concept
    inverse_of: broader_than
    
  - name: related_to
    description: Associative relationship (non-hierarchical)
    domain: Concept
    range: Concept
    example: "employment_contract related_to labor_law"
    
  - name: in_domain
    domain: Concept
    range: Domain
    
  - name: in_microthesaurus
    domain: Concept
    range: MicroThesaurus

# Common Legal Concepts (Examples)
sample_concepts:
  - id: "3141"
    pref_label_en: "employment contract"
    pref_label_de: "Arbeitsvertrag"
    domain: "12" # law
    microthesaurus: "1206" # labour law
    
  - id: "4530"
    pref_label_en: "pension insurance"
    pref_label_de: "Rentenversicherung"
    domain: "28" # social questions
    microthesaurus: "2826" # social insurance
    
  - id: "446"
    pref_label_en: "unemployment benefit"
    pref_label_de: "Arbeitslosengeld"
    domain: "28"
    microthesaurus: "2821" # employment
    
  - id: "1439"
    pref_label_en: "EU directive"
    pref_label_de: "EU-Richtlinie"
    domain: "12"
    microthesaurus: "1236" # EU law
"""

# 4. SGB-Specific Ontology Extension
ontology_files['sgb-extension.yaml'] = """# SGB (Sozialgesetzbuch) Domain Ontology
# German Social Code extension for EU GraphRAG

version: "1.0"
namespace: "http://data.europa.eu/eli/de/sgb#"
prefix: "sgb"

description: |
  Domain-specific ontology for German social law (SGB Books I-XII).
  Extends ELI ontology with social benefit concepts and administrative processes.

sgb_books:
  - book: "I"
    title_de: "Allgemeiner Teil"
    title_en: "General Part"
    scope: "Common provisions for all social law books"
    eli_base: "eli:de:sgb:1"
    
  - book: "II"
    title_de: "Grundsicherung für Arbeitsuchende"
    title_en: "Basic provision for jobseekers"
    scope: "Unemployment benefit II (Hartz IV / Bürgergeld)"
    eli_base: "eli:de:sgb:2"
    authority: "Bundesagentur für Arbeit (BA)"
    
  - book: "III"
    title_de: "Arbeitsförderung"
    title_en: "Employment promotion"
    scope: "Unemployment insurance, job placement"
    eli_base: "eli:de:sgb:3"
    authority: "Bundesagentur für Arbeit (BA)"
    
  - book: "IV"
    title_de: "Gemeinsame Vorschriften für die Sozialversicherung"
    title_en: "Common provisions for social insurance"
    scope: "Contributions, organization, procedures"
    eli_base: "eli:de:sgb:4"
    
  - book: "V"
    title_de: "Gesetzliche Krankenversicherung"
    title_en: "Statutory health insurance"
    scope: "Health care benefits"
    eli_base: "eli:de:sgb:5"
    authority: "Gesetzliche Krankenkassen (GKV)"
    
  - book: "VI"
    title_de: "Gesetzliche Rentenversicherung"
    title_en: "Statutory pension insurance"
    scope: "Old age, disability, survivors pensions"
    eli_base: "eli:de:sgb:6"
    authority: "Deutsche Rentenversicherung (DRV)"
    
  - book: "VII"
    title_de: "Gesetzliche Unfallversicherung"
    title_en: "Statutory accident insurance"
    scope: "Workplace injuries, occupational diseases"
    eli_base: "eli:de:sgb:7"
    
  - book: "VIII"
    title_de: "Kinder- und Jugendhilfe"
    title_en: "Child and youth welfare"
    scope: "Family support, child protection"
    eli_base: "eli:de:sgb:8"
    
  - book: "IX"
    title_de: "Rehabilitation und Teilhabe von Menschen mit Behinderungen"
    title_en: "Rehabilitation and participation of persons with disabilities"
    scope: "Disability benefits, inclusion"
    eli_base: "eli:de:sgb:9"
    
  - book: "X"
    title_de: "Sozialverwaltungsverfahren und Sozialdatenschutz"
    title_en: "Social administrative procedures and data protection"
    scope: "Procedures, appeals, data privacy"
    eli_base: "eli:de:sgb:10"
    
  - book: "XI"
    title_de: "Soziale Pflegeversicherung"
    title_en: "Social long-term care insurance"
    scope: "Nursing care benefits"
    eli_base: "eli:de:sgb:11"
    
  - book: "XII"
    title_de: "Sozialhilfe"
    title_en: "Social assistance"
    scope: "Welfare benefits for those not covered by insurance"
    eli_base: "eli:de:sgb:12"

classes:
  - name: SocialLawBook
    parent: eli:Work
    description: One of the 12 SGB books
    properties:
      - book_number: string
      - title: string (multilingual)
      - authority: Organization
      - effective_date: date
      - latest_amendment: date
      
  - name: BenefitType
    description: Type of social benefit
    properties:
      - benefit_id: string
      - label: string (multilingual)
      - sgb_book: SocialLawBook
      - eligibility_criteria: Article[]
      - legal_basis: Article[]
    examples:
      - "Arbeitslosengeld I" (Unemployment benefit I, SGB III)
      - "Bürgergeld" (Citizen's allowance, SGB II)
      - "Erwerbsminderungsrente" (Disability pension, SGB VI)
      - "Pflegegeld" (Care allowance, SGB XI)
      
  - name: BusinessProcess
    description: Administrative procedure for benefit processing
    properties:
      - process_id: string
      - name: string (multilingual)
      - authority: Organization
      - avg_duration_days: integer
      - annual_volume: integer
      - process_steps: ProcessStep[]
      - legal_basis: Article[]
    example:
      process_id: "DRV-P-001"
      name: "Antrag auf Erwerbsminderungsrente"
      authority: "Deutsche Rentenversicherung"
      avg_duration_days: 90
      annual_volume: 45000
      
  - name: ProcessStep
    description: Individual step in administrative process
    properties:
      - step_number: integer
      - description: string
      - responsible_unit: string
      - it_system: ITSystem
      
  - name: ITSystem
    description: IT system supporting social benefit administration
    properties:
      - system_id: string
      - name: string
      - vendor: string
      - used_by: Organization[]

relationships:
  - name: regulates
    domain: SocialLawBook
    range: BenefitType
    
  - name: based_on
    domain: BusinessProcess
    range: Article
    description: Process implements legal provision
    
  - name: impacts
    domain: Article
    range: BusinessProcess
    properties:
      - impact_type: enum [eligibility, calculation, procedure]
      - affected_population: integer
      - change_probability: enum [low, medium, high]
    description: Legal change affects administrative process
    
  - name: coordinates_with
    domain: SocialLawBook
    range: eli:Work (EU Regulation)
    description: SGB coordinates with EU social security regulations
    example: "SGB VI coordinates_with EU Reg 883/2004 (social security coordination)"
    
  - name: references_sgb
    domain: Article
    range: Article
    properties:
      - reference_type: enum [applies, extends, restricts, supplements]
    description: Cross-references between SGB books

# EU Coordination
eu_regulations_integrated:
  - eli: "eli:eu:reg:2004:883"
    title: "Coordination of social security systems"
    german_implementation: ["SGB IV", "SGB VI"]
    
  - eli: "eli:eu:reg:2009:987"
    title: "Implementing Regulation 883/2004"
    german_implementation: ["SGB IV"]
    
  - eli: "eli:eu:dir:2014:50"
    title: "Posted Workers Directive"
    german_implementation: ["SGB IV", "AEntG"]

# Common SGB Article Types
article_patterns:
  - type: "eligibility"
    description: "Defines who is entitled to benefits"
    example: "SGB VI § 43 - Anspruch auf Rente wegen Erwerbsminderung"
    
  - type: "calculation"
    description: "Formula for benefit amount calculation"
    example: "SGB VI § 63 - Höhe der Rente"
    
  - type: "procedure"
    description: "Administrative procedures and deadlines"
    example: "SGB X § 24 - Antragstellung"
    
  - type: "appeals"
    description: "Legal remedies and appeals process"
    example: "SGB X § 78 - Widerspruchsverfahren"
"""

# Write all ontology files
os.makedirs("/home/mbuchhorn/projects/EU_GraphRAG/ontologies", exist_ok=True)

for filename, content in ontology_files.items():
    filepath = f"/home/mbuchhorn/projects/EU_GraphRAG/ontologies/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created {filename}")

print(f"\n✓ Created {len(ontology_files)} ontology specification files")
print("  Location: /home/mbuchhorn/projects/EU_GraphRAG/ontologies/")
