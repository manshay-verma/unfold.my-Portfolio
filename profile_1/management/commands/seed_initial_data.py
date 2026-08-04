"""
Management command: seed_initial_data
Seeds the DB with the hardcoded content that previously lived in base.html.
Run once: python manage.py seed_initial_data
Safe to re-run — uses get_or_create / update_or_create patterns.
"""

from django.core.management.base import BaseCommand
from profile_1.models import (
    Hero, About, Experience, Education,
    Skill, Project, Contact, SEO, SocialLink,
)


class Command(BaseCommand):
    help = "Seeds the database with the initial hardcoded portfolio content."

    def handle(self, *args, **kwargs):
        self._seed_hero()
        self._seed_about()
        self._seed_experience()
        self._seed_education()
        self._seed_skills()
        self._seed_projects()
        self._seed_contact()
        self._seed_seo()
        self._seed_social()
        self.stdout.write(self.style.SUCCESS("OK  Initial data seeded successfully."))

    # ── Hero ────────────────────────────────────────────────────────────
    def _seed_hero(self):
        hero = Hero.load()
        if not hero.name:
            hero.name = "Manshay"
            hero.designation = "Software Engineer"
            hero.headline = "I'm Manshay Verma, a Software Engineer who loves building complete and scalable solutions."
            hero.description = "My experience covers Backend Development, Machine Learning, and DevOps."
            hero.save()
            self.stdout.write("  Hero seeded.")

    # ── About ───────────────────────────────────────────────────────────
    def _seed_about(self):
        about = About.load()
        if not about.title:
            about.title = "I'm a Software Engineer who loves building complete and scalable solutions."
            about.description = (
                "My experience covers Backend Development, Machine Learning, and DevOps, "
                "which allows me to work on everything from APIs and automation systems "
                "to cloud infrastructure and intelligent applications.\n\n"
                "I'm always curious to learn new technologies, improve my skills, and build "
                "projects that create real impact through software, cloud, and AI."
            )
            about.email = "manshayverma01@gmail.com"
            about.phone = ""
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
                "start_date": "May 2025",
                "end_date": "Present",
                "description": (
                    "Building scalable backend applications and automation systems using modern "
                    "development practices. Working on API development, cloud-based workflows, "
                    "data processing, and deployment pipelines while contributing to reliable and "
                    "high-performance software solutions. Also involved in DevOps practices, "
                    "infrastructure management, and system optimization for production environments."
                ),
                "technologies": ["Python", "Django", "FastAPI", "AWS", "Docker", "PostgreSQL"],
                "display_order": 0,
            },
            {
                "company": "Active Now Technologies",
                "position": "Python Developer",
                "location": "Remote",
                "start_date": "January 2024",
                "end_date": "February 2025",
                "description": (
                    "Worked on backend development, data automation, and web application features "
                    "for data-driven projects. Contributed to API development, workflow automation, "
                    "containerized deployments, and data processing pipelines while collaborating "
                    "on cloud and DevOps-related tasks."
                ),
                "technologies": ["Python", "Flask", "Docker", "MongoDB", "Selenium"],
                "display_order": 1,
            },
        ]
        for e in entries:
            obj, created = Experience.objects.get_or_create(
                company=e["company"], position=e["position"],
                defaults=e,
            )
            if created:
                self.stdout.write(f"  Experience: {e['company']} seeded.")

    # ── Education ───────────────────────────────────────────────────────
    def _seed_education(self):
        entries = [
            {
                "institute": "Devi Ahilya Vishwavidyalaya, Indore",
                "degree": "Master of Technology in Computer Science",
                "start_year": "June 2023",
                "end_year": "May 2025",
                "description": (
                    "Specialized in software engineering, machine learning, distributed systems, "
                    "and cloud computing. Worked on AI-powered applications, scalable backend "
                    "systems, and research focused on data processing and intelligent solutions."
                ),
                "display_order": 0,
            },
            {
                "institute": "Sri Aurobindo Institute of Technology, Indore",
                "degree": "Bachelor of Technology in Computer Science",
                "start_year": "July 2019",
                "end_year": "May 2023",
                "description": (
                    "Built a strong foundation in programming, software development, system design, "
                    "and problem-solving while exploring backend engineering, cloud technologies, "
                    "and real-world application development."
                ),
                "display_order": 1,
            },
        ]
        for e in entries:
            obj, created = Education.objects.get_or_create(
                institute=e["institute"], degree=e["degree"],
                defaults=e,
            )
            if created:
                self.stdout.write(f"  Education: {e['degree']} seeded.")

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
                "title": "Vi Telecom Analytics",
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
                "title": "Harman Studio Cloud",
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
                "title": "Smart Activity Tracker",
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
            title = p.pop("title")
            _, created = Project.objects.update_or_create(
                title=title,
                defaults=p,
            )
            if created:
                self.stdout.write(f"  Project: {title} seeded.")
            else:
                self.stdout.write(f"  Project: {title} updated.")

    # ── Contact ─────────────────────────────────────────────────────────
    def _seed_contact(self):
        contact = Contact.load()
        if not contact.email:
            contact.email = "manshayverma01@gmail.com"
            contact.phone = ""
            contact.address = "Indore, Madhya Pradesh, India"
            contact.save()
            self.stdout.write("  Contact seeded.")

    # ── SEO ─────────────────────────────────────────────────────────────
    def _seed_seo(self):
        seo = SEO.load()
        if not seo.site_title or seo.site_title == "Portfolio":
            seo.site_title = "Manshay Verma — Software Engineer"
            seo.meta_description = (
                "Portfolio of Manshay Verma, a Software Engineer specializing in "
                "Backend Development, Machine Learning, and Cloud/DevOps."
            )
            seo.keywords = "Manshay Verma, Software Engineer, Python, Django, Machine Learning, DevOps, Portfolio"
            seo.save()
            self.stdout.write("  SEO seeded.")

    # ── Social ──────────────────────────────────────────────────────────
    def _seed_social(self):
        socials = [
            ("GitHub",   "https://github.com/manshay-verma",   "icon-github",   0),
            ("LinkedIn", "https://linkedin.com/in/manshay-verma", "icon-linkedin", 1),
        ]
        for platform, url, icon, order in socials:
            _, created = SocialLink.objects.get_or_create(
                platform=platform,
                defaults={"url": url, "icon": icon, "display_order": order},
            )
            if created:
                self.stdout.write(f"  Social: {platform} seeded.")
