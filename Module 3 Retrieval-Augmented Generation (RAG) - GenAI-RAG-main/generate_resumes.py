from fpdf import FPDF
import os

# Create directory for resumes
output_dir = "fake_resumes"
os.makedirs(output_dir, exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Curriculum Vitae', 0, 1, 'R')
        self.ln(5)

    def chapter_title(self, name, role):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, name, 0, 1, 'L')
        self.set_font('Arial', 'I', 12)
        self.cell(0, 10, role, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()

    def add_section(self, title, content):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, content)
        self.ln(3)

# --- DATA GENERATION ---
profiles = [
    # --- CLOUD AI ENGINEERS ---
    {
        "name": "Elena R. Vazquez",
        "role": "Principal AI Architect",
        "summary": "Microsoft Certified AI Engineer with 12 years of experience designing scalable machine learning infrastructure. Expert in RAG architectures, Azure OpenAI Service, and fine-tuning LLMs for enterprise applications.",
        "skills": "Python, PyTorch, Azure AI Studio, LangChain, Kubernetes, Docker, Terraform, NLP.",
        "experience": """Principal AI Architect | TechGlobal Solutions (2020-Present)
- Designed and deployed a Retrieval-Augmented Generation (RAG) system for a Fortune 500 bank, reducing document search time by 90%.
- Led a team of 10 ML engineers in migrating on-premise inference workloads to Azure Kubernetes Service (AKS).
- Implemented responsible AI guardrails using Azure Content Safety to prevent PII leakage in chatbot responses.

Senior Data Scientist | DataFlow Inc. (2016-2020)
- Developed computer vision models for manufacturing defect detection, achieving 99.5% accuracy.
- Built automated MLOps pipelines using MLflow and Databricks, reducing model deployment time from weeks to days.""",
        "education": "M.S. Computer Science, Georgia Tech"
    },
    {
        "name": "David Chen",
        "role": "Senior Cloud AI Engineer",
        "summary": "Specialist in AWS SageMaker and Generative AI. Proven track record of optimizing inference costs and building low-latency vector search solutions.",
        "skills": "AWS SageMaker, Bedrock, Pinecone, Python, Docker, FastAPI, CI/CD.",
        "experience": """Senior Cloud AI Engineer | CloudNative Systems (2019-Present)
- Architected a serverless LLM application using AWS Bedrock and Lambda, serving 50k daily active users.
- Optimized vector database costs by 40% through efficient chunking strategies and hybrid search implementation (OpenSearch).
- Collaborated with DevOps teams to implement 'Blue/Green' deployment strategies for ML models.

Machine Learning Engineer | FinTech Corp (2015-2019)
- Built credit risk scoring models using XGBoost deployed on AWS Fargate.
- Automated data ingestion pipelines using AWS Glue and Athena.""",
        "education": "B.S. Electrical Engineering, UC Berkeley"
    },
    {
        "name": "Sarah Jenkins",
        "role": "Lead MLOps Engineer",
        "summary": "DevOps-native AI Engineer focused on the intersection of infrastructure and Machine Learning. Expert in Kubeflow, Argo Workflows, and GPU cluster management.",
        "skills": "Kubernetes, Kubeflow, Python, Go, Terraform, GCP Vertex AI, Prometheus.",
        "experience": """Lead MLOps Engineer | Nexus AI (2021-Present)
- Managed a 500-node GPU cluster on Google Kubernetes Engine (GKE) for training large language models.
- Implemented Argo Workflows to automate retraining pipelines based on data drift detection.
- Reduced model inference latency by 30% using TensorRT optimization and model quantization.

DevOps Engineer | Streamline Tech (2017-2021)
- Built CI/CD pipelines for microservices architecture using Jenkins and Helm.
- Migrated legacy monolithic applications to Docker containers orchestrated by Kubernetes.""",
        "education": "B.S. Computer Science, University of Washington"
    },
    {
        "name": "Michael O. Adebayo",
        "role": "Generative AI Specialist",
        "summary": "Researcher turned Engineer with deep expertise in Transformer architectures and semantic search. Passionate about building 'Chat with your Data' applications.",
        "skills": "LlamaIndex, Haystack, Python, HuggingFace, Neo4j, GraphRAG, React.",
        "experience": """Generative AI Specialist | InnovateHealth (2022-Present)
- Built a secure internal chatbot for doctors to query patient history using GraphRAG and Neo4j.
- Fine-tuned Llama-3 models on medical datasets to improve terminology recognition by 45%.
- Implemented role-based access control (RBAC) within the RAG pipeline to ensure data privacy.

AI Researcher | University of Toronto (2018-2022)
- Published 3 papers on efficient attention mechanisms in Transformers.
- Collaborated with industry partners to apply NLP research to legal document review.""",
        "education": "Ph.D. Computer Science (NLP Focus), University of Toronto"
    },
    {
        "name": "Priya Patel",
        "role": "Data Engineer (AI Focus)",
        "summary": "Data Engineer specializing in building the data foundation for AI. Expert in unstructured data processing, vector embeddings, and real-time streaming.",
        "skills": "Apache Spark, Kafka, Airflow, Weaviate, Python, Scala, Azure Data Factory.",
        "experience": """Senior Data Engineer | OmniRetail (2019-Present)
- Built a real-time embedding pipeline using Kafka and Spark Streaming to update product vector indices instantly.
- Processed 50TB of unstructured customer review data for sentiment analysis training.
- Designed a 'Lakehouse' architecture using Databricks Delta Lake to unify streaming and batch data.

Data Engineer | LogiTrans (2016-2019)
- Developed ETL pipelines using Airflow to ingest supply chain data from 20+ sources.
- Optimized SQL queries on Snowflake, reducing dashboard load times by 60%.""",
        "education": "M.S. Data Analytics, NYU"
    },

    # --- IT / DEVOPS ---
    {
        "name": "James T. Kirkman",
        "role": "Senior Site Reliability Engineer",
        "summary": "Veteran SRE with 15 years of experience ensuring 99.999% availability for high-traffic e-commerce platforms. Expert in incident management and chaos engineering.",
        "skills": "Linux, Bash, Ansible, Datadog, PagerDuty, AWS, Python.",
        "experience": """Senior SRE | ShopScale (2018-Present)
- Led the 'Black Friday' war room, maintaining 100% uptime during traffic spikes of 100k requests/second.
- Implemented Chaos Monkey testing in production to identify and fix single points of failure.
- Automating incident response runbooks using StackStorm, reducing MTTR by 40%.

Systems Administrator | NetServe (2010-2018)
- Managed 500+ bare-metal Linux servers across 3 data centers.
- Migrated physical infrastructure to a hybrid cloud environment using VMWare and AWS.""",
        "education": "B.S. Information Technology, Purdue University"
    },
    {
        "name": "Linda Wu",
        "role": "Cloud Security Architect",
        "summary": "Security-first architect specializing in Zero Trust environments. Certified CISSP and AWS Security Specialty.",
        "skills": "IAM, VPC Service Controls, Sentinel, Terraform, Python, Compliance (SOC2, HIPAA).",
        "experience": """Lead Cloud Security Architect | FinSafe (2019-Present)
- Designed a Zero Trust network architecture for a digital bank, utilizing micro-segmentation and mTLS.
- Implemented automated compliance scanning using CSPM tools (Wiz), achieving SOC2 Type II certification.
- Conducted threat modeling workshops for all new microservices deployments.

Security Engineer | HealthTech IO (2015-2019)
- Hardened Kubernetes clusters according to CIS benchmarks.
- Managed secrets lifecycle using HashiCorp Vault.""",
        "education": "M.S. Cybersecurity, Johns Hopkins"
    },
    {
        "name": "Robert Sterling",
        "role": "Enterprise Solutions Architect",
        "summary": "Strategic architect with experience in legacy modernization and cloud migration. TOGAF certified.",
        "skills": "TOGAF, Enterprise Architecture, Azure, .NET, Java, API Management (Apigee).",
        "experience": """Enterprise Architect | Global Mfg Corp (2017-Present)
- Led the migration of a 20-year-old ERP system from on-premise mainframe to Azure Cloud.
- Established an API Center of Excellence (CoE) to standardize interface definitions across business units.
- Reduced IT operational costs by $2M/year through application rationalization.

Solution Architect | SoftConsult (2012-2017)
- Designed a microservices-based supply chain platform for a major logistics client.
- Led the technical pre-sales team for enterprise cloud transformations.""",
        "education": "MBA, Technology Management, Wharton"
    },
    {
        "name": "Kevin Flynn",
        "role": "Senior Network Engineer",
        "summary": "Network specialist with deep expertise in SD-WAN, BGP, and hybrid cloud networking.",
        "skills": "Cisco (CCIE), Juniper, BGP, OSPF, Python (Netmiko), AWS Direct Connect.",
        "experience": """Senior Network Engineer | ConnectGlobal (2016-Present)
- Architected a global SD-WAN solution connecting 50 branch offices to AWS regions.
- Troubleshooted complex BGP routing loops during a major ISP outage, restoring service in under 15 minutes.
- Automating network device configuration backups using Ansible and Python.

Network Admin | Regional ISP (2011-2016)
- Managed core routing infrastructure for a user base of 50,000 broadband customers.
- Implemented IPv6 migration strategy.""",
        "education": "B.S. Telecommunications, RIT"
    },
    {
        "name": "Angela Moss",
        "role": "DevSecOps Lead",
        "summary": "Bridging the gap between development, security, and operations. Expert in shifting security left in the CI/CD pipeline.",
        "skills": "GitLab CI, SonarQube, Snyk, Docker, Kubernetes, Bash, Python.",
        "experience": """DevSecOps Lead | SecureSoft (2020-Present)
- Integrated SAST and DAST scanning into the GitLab CI pipeline, blocking critical vulnerabilities from reaching production.
- Standardized container base images across the organization to ensure patch compliance.
- Reduced container build times by 50% through caching strategies and multi-stage builds.

Build Engineer | GameDev Studios (2015-2020)
- Managed build farms for AAA game titles, ensuring nightly builds were delivered to QA by 8 AM.
- Scripted automated deployment tools for game server fleets.""",
        "education": "B.S. Computer Science, UCLA"
    },

    # --- FINANCE ---
    {
        "name": "Marcus Thorne",
        "role": "Senior Portfolio Manager",
        "summary": "CFA Charterholder with 15 years of experience in quantitative asset management and risk hedging. Expert in derivatives and algorithmic trading strategies.",
        "skills": "Portfolio Management, Derivatives, Bloomberg Terminal, Python (pandas), SQL, Risk Analysis.",
        "experience": """Senior Portfolio Manager | Vanguard Horizon (2018-Present)
- Manage a $5B Multi-Asset Global Fund, consistently outperforming the benchmark by 150bps annually.
- Developed a proprietary Python-based risk model to hedge against currency fluctuations in emerging markets.
- Led the integration of ESG (Environmental, Social, Governance) criteria into the investment selection process.

Quantitative Analyst | Prime Capital (2010-2018)
- Built mean-reversion algorithmic trading strategies for G10 currencies.
- Backtested volatility arbitrage strategies using historical options data.""",
        "education": "M.S. Financial Engineering, Columbia University"
    },
    {
        "name": "Jessica Pearson",
        "role": "Investment Banking Associate",
        "summary": "Results-driven banker specializing in M&A within the Technology, Media, and Telecom (TMT) sector. Expert in financial modeling and valuation.",
        "skills": "Financial Modeling (LBO, DCF), M&A, Due Diligence, PowerPoint, Excel Macros.",
        "experience": """Associate, TMT Group | Goldman Sachs (2021-Present)
- Key member of the deal team for the $10B acquisition of a major cloud software provider.
- Built complex LBO models to advise private equity clients on potential take-private transactions.
- Managed the due diligence data room and coordinated with legal and tax advisors.

Analyst | JP Morgan (2018-2021)
- Prepared pitch books and management presentations for IPO roadshows.
- Conducted comparable company analysis (Comps) for valuation of pre-IPO tech startups.""",
        "education": "MBA, Finance, Chicago Booth"
    },
    {
        "name": "William R. Foster",
        "role": "Chief Risk Officer (CRO)",
        "summary": "Executive leader with a strong background in credit risk, operational risk, and regulatory compliance (Basel III).",
        "skills": "Enterprise Risk Management, Credit Risk, Basel III, CCAR, SQL, Tableau.",
        "experience": """Chief Risk Officer | Regional Bank Corp (2019-Present)
- Overhauled the enterprise risk framework, implementing a new credit scoring model that reduced default rates by 12%.
- Led the bank through successful CCAR stress testing submissions to the Federal Reserve.
- Established a Cyber Risk committee to address emerging technology threats.

VP of Credit Risk | Citi (2012-2019)
- Managed a credit portfolio of $2B in commercial real estate loans.
- Developed automated early-warning systems for deteriorating credit quality.""",
        "education": "B.S. Economics, London School of Economics"
    },
    {
        "name": "Satoshi N. (Fake)",
        "role": "Crypto Asset Analyst",
        "summary": "Deep expertise in DeFi protocols, tokenomics, and blockchain analytics. Bridging the gap between traditional finance (TradFi) and Web3.",
        "skills": "Solidity (Reading), Dune Analytics, Python, Smart Contract Auditing, Tokenomics.",
        "experience": """Senior Crypto Analyst | BlockFund Capital (2020-Present)
- Conduct fundamental analysis on Layer 1 and Layer 2 blockchain protocols to guide investment decisions.
- Built automated dashboards on Dune Analytics to track TVL (Total Value Locked) and wallet retention.
- Audited token vesting schedules for seed-stage investments to ensure long-term alignment.

Equity Research Associate | Morgan Stanley (2017-2020)
- Covered the Fintech payments sector, analyzing companies like PayPal, Block, and Visa.
- Published research reports on the impact of digital wallets on traditional banking.""",
        "education": "B.S. Finance, UPenn Wharton"
    },
    {
        "name": "Charles Montgomery",
        "role": "Private Wealth Manager",
        "summary": "Trusted advisor to Ultra-High-Net-Worth (UHNW) individuals. Specializes in estate planning, tax optimization, and alternative investments.",
        "skills": "Wealth Management, Estate Planning, Tax Strategy, Relationship Management, Salesforce.",
        "experience": """Managing Director | UBS Private Wealth (2015-Present)
- Manage $1.2B in AUM for 50 UHNW families.
- Structured complex trust vehicles to minimize estate taxes for multi-generational wealth transfer.
- Provided access to exclusive private equity and hedge fund co-investment opportunities.

Financial Advisor | Merrill Lynch (2005-2015)
- Built a book of business from scratch to $200M AUM within 5 years.
- Specialized in retirement income planning for corporate executives.""",
        "education": "MBA, Harvard Business School"
    },

    # --- ACCOUNTANTS ---
    {
        "name": "Jennifer Wu",
        "role": "Senior Forensic Accountant",
        "summary": "CPA and CFE (Certified Fraud Examiner) with a keen eye for detail. Specializes in uncovering financial discrepancies and supporting litigation.",
        "skills": "Forensic Accounting, Fraud Examination, SQL, IDEA Data Analysis, Litigation Support.",
        "experience": """Senior Manager, Forensics | Deloitte (2018-Present)
- Led an investigation into a $50M procurement fraud scheme at a manufacturing client, resulting in successful prosecution.
- Analyzed terabytes of structured financial data to trace illicit fund flows through shell companies.
- Prepare expert witness reports for federal court cases regarding damages calculations.

Senior Auditor | EY (2013-2018)
- Conducted external audits for Fortune 500 clients in the retail sector.
- Identified material weaknesses in internal controls over financial reporting (ICFR).""",
        "education": "Master of Accounting, University of Texas at Austin"
    },
    {
        "name": "Ben Wyatt (Realistic)",
        "role": "Municipal Comptroller",
        "summary": "Government accounting specialist with a focus on budget optimization and fund accounting. Passionate about fiscal responsibility.",
        "skills": "Fund Accounting, GASB Standards, Budgeting, Excel, SAP ERP.",
        "experience": """City Comptroller | City of Pawnee (2017-Present)
- Balanced the city budget for 5 consecutive years, eliminating a historical deficit of $10M.
- Implemented a new ERP system for payroll and procurement, improving transparency.
- Managed the issuance of $50M in municipal bonds for infrastructure projects.

State Auditor | State Dept of Revenue (2012-2017)
- Audited local municipalities for compliance with state grant requirements.
- Recovered $2M in misallocated funds through detailed ledger analysis.""",
        "education": "B.S. Accounting, Indiana University"
    },
    {
        "name": "Skyler White (Realistic)",
        "role": "Small Business Controller",
        "summary": "Hands-on controller for diverse small businesses. Expert in cash flow management, QuickBooks, and tax compliance.",
        "skills": "QuickBooks Online, Xero, Payroll Management, Tax Preparation, Cash Flow Forecasting.",
        "experience": """Controller | A1A Enterprises (2015-Present)
- Manage all financial aspects for a portfolio of small businesses including retail and service sectors.
- Oversaw a 200% revenue growth phase, securing line-of-credit financing to support expansion.
- Implemented strict cash handling controls to reduce shrinkage and theft.

Bookkeeper | Freelance (2010-2015)
- Provided bookkeeping services for 15+ local clients.
- Cleaned up 3 years of disorganized financial records for a new client facing an IRS audit.""",
        "education": "A.S. Accounting, local Community College"
    },
    {
        "name": "Oscar Martinez (Realistic)",
        "role": "Tax Manager",
        "summary": "Deeply technical tax specialist focused on corporate tax compliance and strategy. Known for finding efficiency in the tax code.",
        "skills": "Corporate Tax, ASC 740, Tax Provision, OneSource, Excel.",
        "experience": """Tax Manager | Dunder Paper Corp (2016-Present)
- Manage the consolidated federal and state tax filings for a multi-state manufacturing company.
- Successfully defended the company during a state sales tax audit, reducing proposed assessments by 80%.
- Implemented automated tax provision software to streamline the quarter-end close process.

Tax Associate | PwC (2012-2016)
- Prepared tax returns for large partnerships and S-corps.
- Researched complex tax implications of international transfer pricing.""",
        "education": "B.S. Accounting, University of Scranton"
    },
    {
        "name": "Arthur P. Anderson",
        "role": "Internal Audit Director",
        "summary": "CIA (Certified Internal Auditor) focused on operational efficiency and risk mitigation. Experience in SOX compliance.",
        "skills": "Internal Audit, SOX Compliance, COSO Framework, Risk Assessment, Visio.",
        "experience": """Director of Internal Audit | Global Logistics (2019-Present)
- Report directly to the Audit Committee of the Board of Directors.
- Developed a risk-based annual audit plan covering operations in 10 countries.
- Identified $5M in cost savings through operational audits of the supply chain procurement process.

Audit Manager | KMPG (2014-2019)
- Managed SOX 404 compliance testing for newly public clients.
- Led training sessions on internal controls for client finance teams.""",
        "education": "B.S. Finance & Accounting, Ohio State University"
    }
]

# --- GENERATE PDFS ---
print("Generating 20 Resumes...")
for p in profiles:
    pdf = PDF()
    pdf.add_page()
    
    # Title
    pdf.chapter_title(p['name'], p['role'])
    
    # Summary
    pdf.add_section("Summary", p['summary'])
    
    # Skills
    pdf.add_section("Technical Skills", p['skills'])
    
    # Experience
    pdf.add_section("Professional Experience", p['experience'])
    
    # Education
    pdf.add_section("Education", p['education'])
    
    # Save
    filename = f"{output_dir}/{p['name'].replace(' ', '_').replace('.', '')}_CV.pdf"
    pdf.output(filename)
    print(f"Created: {filename}")

print(f"\nDone! Check the '{output_dir}' folder.")