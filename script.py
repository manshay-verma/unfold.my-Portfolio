import re

file_path = r'E:\ML_AND_AI\Python\Django\Portfolio\profile_1\management\commands\seed_initial_data.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_projects = '''        projects = [
            {
                "title": "Vi Telecom Analytics",
                "short_description": "Enterprise Backend, Data Engineering",
                "description": \"\"\"<p>Built a large-scale telecom analytics and backend automation system using FastAPI, Pandas, Shell Scripting, and Linux-based server environments. Automated enterprise workflows for data ingestion, transformation, formula-based calculations, network analytics, and reporting pipelines while improving operational efficiency and reducing manual processing time.</p>
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
</ul>\"\"\",
                "tech_stack": ["Python", "Django", "PostgreSQL", "PySpark", "AWS"],
                "featured": True,
                "display_order": 0,
            },
            {
                "title": "Harman Studio Cloud",
                "short_description": "Cloud Infrastructure, SaaS Backend",
                "description": \"\"\"<p>Architected and developed a multi-tenant SaaS cloud infrastructure for professional audio studios using FastAPI, GraphQL, and AWS services. Built scalable backend systems to handle complex studio management workflows.</p>
<h4 class="mb-3" style="color:#fff;font-size:16px;letter-spacing:1px;text-transform:uppercase; margin-top: 20px;">Key Highlights</h4>
<ul class="highlight-list mb-4">
  <li>Multi-tenant SaaS architecture</li>
  <li>AWS Lambda Serverless</li>
  <li>FastAPI & GraphQL APIs</li>
  <li>Terraform (IaC)</li>
</ul>\"\"\",
                "tech_stack": ["Python", "FastAPI", "AWS", "Docker", "Kubernetes"],
                "featured": True,
                "display_order": 1,
            },
            {
                "title": "BMP Book",
                "short_description": "Mobile App, Real-Time Platform",
                "description": \"\"\"<p>Developed a scalable full-stack booking platform connecting users with verified pandits through real-time communication systems, geolocation services, and cloud-based infrastructure using React Native, Django REST Framework, Redis, and AWS integrations.</p>
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
</ul>\"\"\",
                "tech_stack": ["Django", "WebSockets", "PostgreSQL", "Redis"],
                "featured": False,
                "display_order": 2,
            },
            {
                "title": "Smart Activity Tracker",
                "short_description": "AI, Desktop App, Computer Vision",
                "description": \"\"\"<p>Developed a desktop monitoring and activity analysis application using Qt and OpenCV for capturing and processing detailed information from active desktop windows.</p>
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
</ul>\"\"\",
                "tech_stack": ["Python", "TensorFlow", "OpenCV", "PyQt5"],
                "featured": False,
                "display_order": 3,
            },
            {
                "title": "Text Analysis System",
                "short_description": "Automation, NLP, Data Processing",
                "description": \"\"\"<p>Built a Python-based automation system for extracting article data from URLs and performing advanced text-analysis workflows. The system implements robust extraction pipelines using BeautifulSoup and Requests.</p>
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
</ul>\"\"\",
                "tech_stack": ["Python", "Scrapy", "NLTK", "spaCy", "Elasticsearch"],
                "featured": False,
                "display_order": 4,
            },
            {
                "title": "MUSLEEASE E-Commerce",
                "short_description": "Full-Stack, MERN E-Commerce",
                "description": \"\"\"<p>Built a comprehensive MERN-stack e-commerce platform for gym and lifestyle products. The platform features a scalable backend and highly responsive shopping workflows designed for a premium user experience.</p>
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
</ul>\"\"\",
                "tech_stack": ["React", "Node.js", "MongoDB", "Express", "Stripe"],
                "featured": False,
                "display_order": 5,
            },
        ]'''

content = re.sub(r'        projects = \[.*?        \]', new_projects, content, flags=re.DOTALL)
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Replaced projects!')
