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
            # Backend
            ("Python",     "Backend", 92, "icon-cogs",      0),
            ("Django",     "Backend", 90, "icon-cogs",      1),
            ("FastAPI",    "Backend", 85, "icon-cogs",      2),
            ("Flask",      "Backend", 82, "icon-cogs",      3),
            ("DRF",        "Backend", 88, "icon-cogs",      4),
            ("REST APIs",  "Backend", 90, "icon-cogs",      5),
            # Cloud / DevOps
            ("AWS",            "Cloud", 78, "icon-cloud",  10),
            ("Docker",         "DevOps", 85, "icon-cloud", 11),
            ("Kubernetes",     "DevOps", 70, "icon-cloud", 12),
            ("GitHub Actions", "DevOps", 80, "icon-cloud", 13),
            ("Linux",          "DevOps", 85, "icon-cloud", 14),
            # AI / ML
            ("TensorFlow",  "ML", 75, "icon-lightbulb-o", 20),
            ("PyTorch",     "ML", 72, "icon-lightbulb-o", 21),
            ("Scikit-learn","ML", 80, "icon-lightbulb-o", 22),
            ("CNNs",        "AI", 70, "icon-lightbulb-o", 23),
            ("Pandas",      "ML", 88, "icon-lightbulb-o", 24),
            # Database
            ("PostgreSQL", "Database", 85, "icon-database", 30),
            ("MongoDB",    "Database", 80, "icon-database", 31),
            ("Redis",      "Database", 72, "icon-database", 32),
            ("MySQL",      "Database", 82, "icon-database", 33),
        ]
        for name, cat, pct, icon, order in skills:
            _, created = Skill.objects.get_or_create(
                name=name, category=cat,
                defaults={"percentage": pct, "icon": icon, "display_order": order},
            )
            if created:
                self.stdout.write(f"  Skill: {name} seeded.")

    # ── Projects ────────────────────────────────────────────────────────
    def _seed_projects(self):
        projects = [
            {
                "title": "Vi Telecom Analytics",
                "short_description": "Enterprise Backend, Data Engineering",
                "description": "Enterprise analytics system for Vi Telecom with scalable data pipelines and backend APIs.",
                "tech_stack": ["Python", "Django", "PostgreSQL", "PySpark", "AWS"],
                "featured": True,
                "display_order": 0,
            },
            {
                "title": "Harman Studio Cloud",
                "short_description": "Cloud Infrastructure, SaaS Backend",
                "description": "Cloud-native SaaS backend platform for Harman Studio with multi-tenant architecture.",
                "tech_stack": ["Python", "FastAPI", "AWS", "Docker", "Kubernetes"],
                "featured": True,
                "display_order": 1,
            },
            {
                "title": "BMP Book",
                "short_description": "Mobile App, Real-Time Platform",
                "description": "Real-time booking platform with mobile app backend and live availability tracking.",
                "tech_stack": ["Django", "WebSockets", "PostgreSQL", "Redis"],
                "featured": False,
                "display_order": 2,
            },
            {
                "title": "Smart Activity Tracker",
                "short_description": "AI, Desktop App, Computer Vision",
                "description": "AI-powered desktop application using computer vision to track and analyze user activity.",
                "tech_stack": ["Python", "TensorFlow", "OpenCV", "PyQt5"],
                "featured": False,
                "display_order": 3,
            },
            {
                "title": "Text Analysis System",
                "short_description": "Automation, NLP, Data Processing",
                "description": "Web scraping and NLP-based text analysis system for automated data extraction and insights.",
                "tech_stack": ["Python", "Scrapy", "NLTK", "spaCy", "Elasticsearch"],
                "featured": False,
                "display_order": 4,
            },
            {
                "title": "MUSLEEASE E-Commerce",
                "short_description": "Full-Stack, MERN E-Commerce",
                "description": "Full-stack e-commerce platform built with MERN stack featuring cart, payments, and admin panel.",
                "tech_stack": ["React", "Node.js", "MongoDB", "Express", "Stripe"],
                "featured": False,
                "display_order": 5,
            },
        ]
        for p in projects:
            _, created = Project.objects.get_or_create(
                title=p["title"],
                defaults=p,
            )
            if created:
                self.stdout.write(f"  Project: {p['title']} seeded.")

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
