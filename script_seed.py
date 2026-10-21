import re

file_path = r'E:\ML_AND_AI\Python\Django\Portfolio\profile_1\management\commands\seed_initial_data.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_skills_func = '''    def _seed_skills(self):
        skills = [
            # Backend
            ("Python",     "Backend", 92, "icon-cogs",      0, "Extensive experience building scalable backend services and data pipelines."),
            ("Django",     "Backend", 90, "icon-cogs",      1, "Expert in building robust web applications and REST APIs using Django framework."),
            ("FastAPI",    "Backend", 85, "icon-cogs",      2, "Proficient in developing high-performance async APIs for modern web services."),
            ("Flask",      "Backend", 82, "icon-cogs",      3, "Experience building lightweight microservices and prototyping web apps."),
            ("DRF",        "Backend", 88, "icon-cogs",      4, "Strong background in designing and implementing RESTful APIs with Django REST Framework."),
            ("REST APIs",  "Backend", 90, "icon-cogs",      5, "Deep understanding of API design principles, authentication, and integration."),
            # Cloud / DevOps
            ("AWS",            "Cloud", 78, "icon-cloud",  10, "Experience deploying and managing applications using EC2, S3, RDS, and Lambda."),
            ("Docker",         "DevOps", 85, "icon-cloud", 11, "Skilled in containerizing applications for consistent deployment across environments."),
            ("Kubernetes",     "DevOps", 70, "icon-cloud", 12, "Familiar with orchestrating containerized applications in production clusters."),
            ("GitHub Actions", "DevOps", 80, "icon-cloud", 13, "Automating CI/CD pipelines for testing and deployment workflows."),
            ("Linux",          "DevOps", 85, "icon-cloud", 14, "Strong command-line skills and experience managing Linux-based servers."),
            # AI / ML
            ("TensorFlow",  "ML", 75, "icon-lightbulb-o", 20, "Experience building and training deep learning models for various tasks."),
            ("PyTorch",     "ML", 72, "icon-lightbulb-o", 21, "Proficient in developing neural networks and custom architectures."),
            ("Scikit-learn","ML", 80, "icon-lightbulb-o", 22, "Implementing traditional machine learning algorithms and data preprocessing."),
            ("CNNs",        "AI", 70, "icon-lightbulb-o", 23, "Designing convolutional neural networks for computer vision applications."),
            ("Pandas",      "ML", 88, "icon-lightbulb-o", 24, "Expert in data manipulation, cleaning, and analysis using Pandas DataFrames."),
            # Database
            ("PostgreSQL", "Database", 85, "icon-database", 30, "Designing relational schemas and optimizing complex SQL queries."),
            ("MongoDB",    "Database", 80, "icon-database", 31, "Working with NoSQL databases for flexible and scalable data storage."),
            ("Redis",      "Database", 72, "icon-database", 32, "Implementing caching layers and message brokers for improved performance."),
            ("MySQL",      "Database", 82, "icon-database", 33, "Experience managing relational databases and ensuring data integrity."),
        ]
        for name, cat, pct, icon, order, desc in skills:
            _, created = Skill.objects.update_or_create(
                name=name, category=cat,
                defaults={"percentage": pct, "icon": icon, "display_order": order, "description": desc},
            )
            if created:
                self.stdout.write(f"  Skill: {name} seeded.")
            else:
                self.stdout.write(f"  Skill: {name} updated.")'''

content = re.sub(r'    def _seed_skills\(self\):.*?    # -- Projects --', new_skills_func + '\n\n    # -- Projects --', content, flags=re.DOTALL)
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Replaced skills!')
