"""
Management command: seed_initial_data
Seeds the DB with all current portfolio content.
Run once or whenever DB is reset: python manage.py seed_initial_data
Safe to re-run — updates existing records or creates them cleanly.
"""

from django.core.management.base import BaseCommand
from profile_1.models import (
    Hero, About, Experience, Education,
    Skill, Project, Certification, Contact, SEO, SocialLink, Journal
)


class Command(BaseCommand):
    help = "Seeds the database with all portfolio content."

    def handle(self, *args, **kwargs):
        self._seed_hero()
        self._seed_about()
        self._seed_experience()
        self._seed_education()
        self._seed_skills()
        self._seed_projects()
        self._seed_certifications()
        self._seed_contact()
        self._seed_seo()
        self._seed_social()
        self._seed_journals()
        self.stdout.write(self.style.SUCCESS("OK  Initial data seeded successfully."))

    # ── Hero ────────────────────────────────────────────────────────────
    def _seed_hero(self):
        hero = Hero.load()
        hero.name = "Manshay"
        hero.designation = "Software Engineer"
        hero.headline = "I’m Manshay Verma, a Software Engineer based in India."
        hero.description = "Specializing in FastAPI, Django REST Framework, LangGraph, CrewAI, RAG pipelines, and AWS cloud infrastructure."
        hero.save()
        self.stdout.write("  Hero seeded.")

    # ── About ───────────────────────────────────────────────────────────
    def _seed_about(self):
        about = About.load()
        about.title = "I’m a Software Engineer who loves building complete and scalable solutions."
        about.description = (
            "My experience covers Backend Development, Machine Learning, and DevOps, "
            "which allows me to work on everything from APIs and automation systems "
            "to cloud infrastructure and intelligent applications.\n\n"
            "I’m always curious to learn new technologies, improve my skills, and build "
            "projects that create real impact through software, cloud, and AI."
        )
        about.email = "manshayverma01@gmail.com"
        about.phone = "+91 62649 96677"
        about.location = "Indore, India"
        about.experience_years = 2
        about.projects_completed = 6
        about.clients = 3
        about.save()
        self.stdout.write("  About seeded.")

    # ── Experience ──────────────────────────────────────────────────────
    def _seed_experience(self):
        entries = [
            {
                "company": "CubexO Software Solutions",
                "position": "Software Engineer",
                "location": "Indore, India",
                "start_date": "2025-05-15",
                "end_date": "2026-05-31",
                "description": (
                    "Built scalable backend applications and automation systems for enterprise products "
                    "across telecom, SaaS, and audio platform domains. Developed RESTful APIs, automated data "
                    "processing workflows, designed multi-tenant cloud solutions, and optimized backend performance "
                    "using FastAPI, Django REST Framework, GraphQL, AWS, and modern DevOps practices."
                ),
                "technologies": ["Python", "Django", "FastAPI", "AWS", "Docker", "PostgreSQL", "MongoAtlas", "Jira", "Github", "Bitbucket"],
                "display_order": 1,
            },
            {
                "company": "Muscle Ease",
                "position": "Full Stack Engineer",
                "location": "Remote - Freelance",
                "start_date": "2022-02-01",
                "end_date": "2022-09-29",
                "description": (
                    "Independently designed, developed, and deployed a full-stack fitness web application using the MERN stack "
                    "(MongoDB, Express.js, React, and Node.js). Built responsive frontend interfaces, developed RESTful APIs, "
                    "and designed the database architecture. Implemented secure user authentication along with PayPal payment gateway integration."
                ),
                "technologies": ["MongoDB", "Express.js", "React", "Node.js", "JavaScript", "REST API", "PayPal", "JWT", "Authentication"],
                "display_order": 2,
            },
        ]
        for e in entries:
            company = e["company"]
            position = e["position"]
            Education.objects.filter(institute=company, degree=position).delete()
            Experience.objects.update_or_create(
                company=company, position=position,
                defaults=e,
            )
            self.stdout.write(f"  Experience: {company} seeded.")

    # ── Education ───────────────────────────────────────────────────────
    def _seed_education(self):
        entries = [
            {
                "institute": "Devi Ahilya Vishwavidyalaya, Indore",
                "degree": "Master of Technology in Computer Science",
                "start_year": "2023-06-01",
                "end_year": "2025-04-30",
                "description": (
                    "Specialized in software engineering, machine learning, distributed systems, "
                    "and cloud computing. Worked on AI-powered applications and scalable backend systems."
                ),
                "specializations": [
                    "Advanced Algorithms", "Machine Learning & AI", "Distributed Systems",
                    "Cyber Security", "Artificial Intelligence (Python)", "Web Development (Django, Flask)"
                ],
                "display_order": 0,
            },
            {
                "institute": "Sri Aurobindo Institute of Technology, Indore",
                "degree": "Bachelor of Technology in Computer Science",
                "start_year": "2019-03-01",
                "end_year": "2023-05-31",
                "description": (
                    "Built a strong foundation in programming, software development, system design, "
                    "and problem-solving while exploring backend engineering and cloud technologies."
                ),
                "specializations": [
                    "Data Structures & Algorithms", "Operating Systems",
                    "Data Analytics & Cloud Computing", "AWS Infrastructure"
                ],
                "display_order": 1,
            },
        ]
        for e in entries:
            institute = e["institute"]
            degree = e["degree"]
            Education.objects.update_or_create(
                institute=institute, degree=degree,
                defaults=e,
            )
            self.stdout.write(f"  Education: {degree} seeded.")

    # ── Skills ──────────────────────────────────────────────────────────
    def _seed_skills(self):
        skills = [
            {
                "name": "Python & Backend Engineering",
                "category": "Backend",
                "description": "Django, DRF, FastAPI, Flask, GraphQL, Microservices Architecture, RESTful APIs, Celery.",
                "percentage": 92,
                "icon": "fa-brands fa-python",
                "display_order": 1,
            },
            {
                "name": "Agentic AI & LLM Systems",
                "category": "AI",
                "description": "LangGraph, LangChain, CrewAI, RAG Pipelines, Multi-Agent Workflows, Context Recall & Semantic Chunking.",
                "percentage": 88,
                "icon": "fa-solid fa-brain",
                "display_order": 2,
            },
            {
                "name": "Machine Learning & Analytics",
                "category": "ML",
                "description": "TensorFlow, PyTorch, Pandas, NumPy, Plotly Dash, Streamlit, Predictive Analytics.",
                "percentage": 85,
                "icon": "fa-solid fa-chart-line",
                "display_order": 3,
            },
            {
                "name": "Cloud Infrastructure (AWS)",
                "category": "Cloud",
                "description": "AWS (EC2, S3, Lambda, RDS, Aurora, DynamoDB, VPC, IAM, Route 53, CloudFormation, ELB, Auto Scaling, CloudWatch, CloudFront, Athena).",
                "percentage": 85,
                "icon": "fa-brands fa-aws",
                "display_order": 4,
            },
            {
                "name": "Databases & Vector Search",
                "category": "Database",
                "description": "PostgreSQL, SQLite, MongoDB Atlas, MySQL, ChromaDB, Weaviate, Redis.",
                "percentage": 90,
                "icon": "fa-solid fa-database",
                "display_order": 5,
            },
            {
                "name": "DevOps, CI/CD & Automation",
                "category": "DevOps",
                "description": "Docker, Docker Compose, Linux Server Management, Shell Scripting, CI/CD Pipelines, Sumo Logic, Jira, Confluence.",
                "percentage": 82,
                "icon": "fa-brands fa-docker",
                "display_order": 6,
            },
            {
                "name": "Programming & CS Fundamentals",
                "category": "Backend",
                "description": "Python, C++, Data Structures & Algorithms, Object-Oriented Design, Distributed Systems.",
                "percentage": 90,
                "icon": "fa-solid fa-code",
                "display_order": 7,
            },
        ]
        
        Skill.objects.all().delete()
        for sk in skills:
            Skill.objects.create(**sk)
            self.stdout.write(f"  Skill: {sk['name']} seeded.")

    # ── Projects ────────────────────────────────────────────────────────
    def _seed_projects(self):
        projects = [
            {
                "title": "Autonomous Multi-Agent Research Assistant (LangGraph + RAG)",
                "slug": "autonomous-multi-agent-research-assistant-langgraph-rag",
                "short_description": "LangGraph, LangChain, FastAPI, RAG, ChromaDB, Docker",
                "description": """<p>Architected a LangGraph-based multi-agent system (Supervisor, Researcher, Summarizer, Fact-Checker) that autonomously plans, retrieves, and verifies research information into a cited report, cutting manual research time by ~70% in testing.</p>
<h4 class="mb-3" style="color: #fff; font-size: 16px; letter-spacing: 1px; text-transform: uppercase; margin-top: 20px;">Key Highlights</h4>
<ul class="highlight-list">
  <li>LangGraph Multi-Agent Architecture</li>
  <li>RAG pipeline with ChromaDB and chunked embeddings (~40% hallucination reduction)</li>
  <li>Async FastAPI backend with SSE streaming (50+ concurrent sessions)</li>
  <li>PostgreSQL + Redis session state & agent memory</li>
  <li>Docker Compose deployment on AWS EC2</li>
</ul>""",
                "tech_stack": ["LangGraph", "LangChain", "FastAPI", "PostgreSQL", "Redis", "ChromaDB", "Docker"],
                "featured": True,
                "display_order": 0,
            },
            {
                "title": "Vi Telecom Analytics",
                "slug": "vi-telecom-analytics",
                "short_description": "Enterprise Backend, Data Engineering",
                "description": """<p>Built a large-scale telecom analytics and backend automation system using FastAPI, Pandas, Shell Scripting, and Linux-based server environments. Automated enterprise workflows for data ingestion, transformation, formula-based calculations, network analytics, and reporting pipelines while improving operational efficiency and reducing manual processing time.</p>
<h4 class="mb-3" style="color: #fff; font-size: 16px; letter-spacing: 1px; text-transform: uppercase; margin-top: 20px;">Key Highlights</h4>
<ul class="highlight-list">
  <li>FastAPI backend services</li>
  <li>Telecom analytics workflows</li>
  <li>Large-scale data ingestion</li>
  <li>Linux server automation</li>
  <li>Shell scripting</li>
  <li>Remote server management</li>
  <li>CRUD utilities</li>
  <li>GitLab CI/CD workflows</li>
  <li>Production deployment handling</li>
  <li>PostgreSQL & SQLite optimization</li>
</ul>""",
                "tech_stack": ["Python", "Django", "PostgreSQL", "PySpark", "AWS"],
                "featured": True,
                "display_order": 0,
            },
            {
                "title": "Customer Support Multi-Agent System (CrewAI)",
                "slug": "customer-support-multi-agent-system-crewai",
                "short_description": "CrewAI, FastAPI, Celery, PostgreSQL, Redis, Docker",
                "description": """<p>Built a CrewAI-based customer support automation system with 3 specialized agents (Billing, Technical, Refund), achieving an 85% auto-resolution rate on a 500-ticket synthetic dataset.</p>
<h4 class="mb-3" style="color:#fff;font-size:16px;letter-spacing:1px;text-transform:uppercase; margin-top: 20px;">Key Highlights</h4>
<ul class="highlight-list mb-4">
  <li>CrewAI multi-agent support workflows</li>
  <li>Async ticket processing pipeline with Celery & Redis (45% handling time reduction)</li>
  <li>Context-aware escalation logic cutting resolution time by 30%</li>
</ul>""",
                "tech_stack": ["CrewAI", "FastAPI", "Celery", "PostgreSQL", "Redis", "Docker"],
                "featured": True,
                "display_order": 1,
            },
            {
                "title": "Harman Studio Cloud",
                "slug": "harman-studio-cloud",
                "short_description": "Cloud Infrastructure, SaaS Backend",
                "description": """<p>Architected and developed a multi-tenant SaaS cloud infrastructure for professional audio studios using FastAPI, GraphQL, and AWS services. Built scalable backend systems to handle complex studio management workflows.</p>
<h4 class="mb-3" style="color:#fff;font-size:16px;letter-spacing:1px;text-transform:uppercase; margin-top: 20px;">Key Highlights</h4>
<ul class="highlight-list mb-4">
  <li>Multi-tenant SaaS architecture</li>
  <li>AWS Lambda Serverless</li>
  <li>FastAPI & GraphQL APIs</li>
  <li>Terraform (IaC)</li>
</ul>""",
                "tech_stack": ["Python", "FastAPI", "AWS", "Docker", "Kubernetes"],
                "featured": True,
                "display_order": 1,
            },
            {
                "title": "BMP Book",
                "slug": "bmp-book",
                "short_description": "Mobile App, Real-Time Platform",
                "description": """<p>Developed a scalable full-stack booking platform connecting users with verified pandits through real-time communication systems, geolocation services, and cloud-based infrastructure using React Native, Django REST Framework, Redis, and AWS integrations.</p>
<h4 class="mb-3" style="color:#fff;font-size:16px;letter-spacing:1px;text-transform:uppercase; margin-top: 20px;">Key Features</h4>
<ul class="highlight-list">
  <li>React Native mobile app</li>
  <li>DRF backend APIs</li>
  <li>AWS SNS & SQS integrations</li>
  <li>Redis caching</li>
  <li>Geolocation & maps</li>
  <li>Real-time notifications</li>
  <li>Booking workflows</li>
  <li>Elasticsearch search systems</li>
</ul>""",
                "tech_stack": ["Django", "WebSockets", "PostgreSQL", "Redis"],
                "featured": False,
                "display_order": 2,
            },
            {
                "title": "Personal Knowledge Base Agent (RAG + Long-Term Memory)",
                "slug": "personal-knowledge-base-agent-rag-long-term-memory",
                "short_description": "LangChain, Weaviate, FastAPI, PostgreSQL",
                "description": """<p>Built a personal RAG chatbot with long-term memory, storing summarized past conversations as embeddings, improving multi-session context recall by 50%.</p>
<h4 class="mb-3" style="color:#fff;font-size:16px;letter-spacing:1px;text-transform:uppercase; margin-top: 20px;">Key Features</h4>
<ul class="highlight-list">
  <li>Multi-format document ingestion (PDF/DOCX/MD) with semantic chunking</li>
  <li>Weaviate Vector DB & PostgreSQL embeddings storage</li>
</ul>""",
                "tech_stack": ["LangChain", "Weaviate", "FastAPI", "PostgreSQL"],
                "featured": False,
                "display_order": 2,
            },
            {
                "title": "Multi-Agent Travel/Itinerary Planner (CrewAI)",
                "slug": "multi-agent-travelitinerary-planner-crewai",
                "short_description": "CrewAI, FastAPI, Google Maps API, OpenWeatherMap API",
                "description": """<p>Developed a CrewAI-based multi-agent trip planner (Planner, Budget, Logistics agents) that iteratively refines itineraries, keeping 95% of generated plans within user budget constraints.</p>
<h4 class="mb-3" style="color:#fff;font-size:16px;letter-spacing:1px;text-transform:uppercase; margin-top: 20px;">Key Features</h4>
<ul class="highlight-list">
  <li>Google Maps Distance Matrix & OpenWeatherMap API integrations</li>
  <li>Multi-agent iterative itinerary optimization</li>
</ul>""",
                "tech_stack": ["CrewAI", "FastAPI", "PostgreSQL", "Google Maps API", "OpenWeatherMap"],
                "featured": False,
                "display_order": 3,
            },
            {
                "title": "Smart Activity Tracker",
                "slug": "smart-activity-tracker",
                "short_description": "AI, Desktop App, Computer Vision",
                "description": """<p>Developed a desktop monitoring and activity analysis application using Qt and OpenCV for capturing and processing detailed information from active desktop windows.</p>
<h4 class="mb-3" style="color:#fff;font-size:16px;letter-spacing:1px;text-transform:uppercase; margin-top: 20px;">Key Features</h4>
<ul class="highlight-list">
  <li>Active window tracking</li>
  <li>Dynamic screen analysis</li>
  <li>OpenCV image processing</li>
  <li>OCR integration</li>
  <li>Edge recognition</li>
  <li>Local secure processing</li>
  <li>Responsive PyQt5 UI</li>
  <li>Workflow analysis</li>
</ul>""",
                "tech_stack": ["Python", "TensorFlow", "OpenCV", "PyQt5"],
                "featured": False,
                "display_order": 3,
            },
            {
                "title": "Text Analysis System",
                "slug": "text-analysis-system",
                "short_description": "Automation, NLP, Data Processing",
                "description": """<p>Built a Python-based automation system for extracting article data from URLs and performing advanced text-analysis workflows. The system implements robust extraction pipelines using BeautifulSoup and Requests.</p>
<h4 class="mb-3" style="color:#fff;font-size:16px;letter-spacing:1px;text-transform:uppercase; margin-top: 20px;">Key Features</h4>
<ul class="highlight-list">
  <li>Automated article extraction</li>
  <li>Readability analysis</li>
  <li>Sentiment analysis</li>
  <li>Excel automation</li>
  <li>Broken URL management</li>
  <li>Natural Language Processing</li>
  <li>Structured data output</li>
  <li>Error handling & logging</li>
</ul>""",
                "tech_stack": ["Python", "Scrapy", "NLTK", "spaCy", "Elasticsearch"],
                "featured": False,
                "display_order": 4,
            },
            {
                "title": "MUSLEEASE E-Commerce",
                "slug": "musleease-e-commerce",
                "short_description": "Full-Stack, MERN E-Commerce",
                "description": """<p>Built a comprehensive MERN-stack e-commerce platform for gym and lifestyle products. The platform features a scalable backend and highly responsive shopping workflows designed for a premium user experience.</p>
<h4 class="mb-3" style="color:#fff;font-size:16px;letter-spacing:1px;text-transform:uppercase; margin-top: 20px;">Key Features</h4>
<ul class="highlight-list">
  <li>Authentication system</li>
  <li>Cart & checkout workflows</li>
  <li>Payment integration</li>
  <li>Product reviews</li>
  <li>Admin dashboard</li>
  <li>Password recovery</li>
  <li>Cloudinary image storage</li>
  <li>Email notification systems</li>
</ul>""",
                "tech_stack": ["React", "Node.js", "MongoDB", "Express", "Stripe"],
                "featured": False,
                "display_order": 5,
            },
        ]

        for p in projects:
            slug = p["slug"]
            Project.objects.update_or_create(slug=slug, defaults=p)
            self.stdout.write(f"  Project: {slug} seeded.")

    # ── Certifications ──────────────────────────────────────────────────
    def _seed_certifications(self):
        certs = [
            {
                "title": "Ultimate AWS Certified Solutions Architect Associate",
                "issuer": "Udemy (Stephane Maarek)",
                "issue_date": "2023-05-10",
                "display_order": 0,
            },
            {
                "title": "The Complete Python Developer",
                "issuer": "Udemy (Andrei Neagoie)",
                "issue_date": "2023-11-20",
                "display_order": 1,
            },
            {
                "title": "Complete A.I. & Machine Learning, Data Science Bootcamp",
                "issuer": "Udemy (Andrei Neagoie, Daniel Bourke)",
                "issue_date": "2024-01-15",
                "display_order": 2,
            },
        ]
        for c in certs:
            title = c["title"]
            Certification.objects.update_or_create(title=title, defaults=c)
            self.stdout.write(f"  Certification: {title} seeded.")

    # ── Contact ─────────────────────────────────────────────────────────
    def _seed_contact(self):
        contact = Contact.load()
        contact.email = "manshayverma01@gmail.com"
        contact.phone = "+91 62649 96677"
        contact.address = "Indore, India"
        contact.save()
        self.stdout.write("  Contact seeded.")

    # ── SEO ─────────────────────────────────────────────────────────────
    def _seed_seo(self):
        seo = SEO.load()
        seo.site_title = "Manshay Verma — Backend & AI/ML Engineer"
        seo.meta_description = "Portfolio of Manshay Verma, Backend & AI/ML Engineer specializing in FastAPI, Django REST Framework, LangGraph, CrewAI, RAG, and AWS."
        seo.keywords = "Manshay Verma, Backend Engineer, AI Engineer, FastAPI, Django, LangGraph, CrewAI, RAG, AWS, Portfolio"
        seo.save()
        self.stdout.write("  SEO seeded.")

    # ── Social Links ────────────────────────────────────────────────────
    def _seed_social(self):
        links = [
            {
                "platform": "GitHub",
                "url": "https://github.com/manshay-verma",
                "icon": "icon-github",
                "display_order": 0,
            },
            {
                "platform": "LinkedIn",
                "url": "https://linkedin.com/in/manshay-verma01",
                "icon": "icon-linkedin",
                "display_order": 1,
            },
        ]
        for l in links:
            platform = l["platform"]
            SocialLink.objects.update_or_create(platform=platform, defaults=l)
            self.stdout.write(f"  SocialLink: {platform} seeded.")

    # ── Journals ────────────────────────────────────────────────────────
    def _seed_journals(self):
        journals = [
            {
                "title": "My Journey in Software Engineering",
                "slug": "my-journey-in-software-engineering",
                "author": "Manshay Verma",
                "read_time": "5 mins read",
                "publish_date": "2026-08-03",
                "excerpt": "A brief overview of how I started my journey in tech and what I learned along the way.",
                "content": "<p>I started my journey back in college, exploring various programming languages and software engineering fundamentals. Over the years, I developed a strong passion for scalable backend architectures, cloud computing, and AI-driven automation systems.</p><p>Building real-world projects and solving complex engineering challenges has taught me the importance of writing clean, maintainable, and reliable software.</p>",
                "external_urls": [],
                "display_order": 0,
            },
            {
                "title": "The Future of Web Development",
                "slug": "the-future-of-web-development",
                "author": "Manshay Verma",
                "read_time": "4 mins read",
                "publish_date": "2026-08-03",
                "excerpt": "Thoughts on where web development is heading with the rise of AI and modern cloud systems.",
                "content": "<p>The web is constantly evolving. With AI-assisted coding tools, vector search databases, and serverless cloud infrastructure, developers are becoming more productive than ever.</p><p>Integrating intelligent agentic workflows and modern web APIs is transforming how web applications interact with users and process data.</p>",
                "external_urls": [],
                "display_order": 1,
            },
            {
                "title": "Understanding Django Architecture",
                "slug": "understanding-django-architecture",
                "author": "Manshay Verma",
                "read_time": "8 mins read",
                "publish_date": "2026-08-03",
                "excerpt": "An in-depth look at Django's MVT architecture and why it scales so well for enterprise applications.",
                "content": "<p>Django uses Model-View-Template architecture, which is slightly different from the traditional MVC pattern. It handles database ORM, administrative interfaces, and security out-of-the-box, making it ideal for rapid enterprise development.</p>",
                "external_urls": [],
                "display_order": 2,
            },
        ]
        for j in journals:
            slug = j["slug"]
            Journal.objects.update_or_create(slug=slug, defaults=j)
            self.stdout.write(f"  Journal: {slug} seeded.")

