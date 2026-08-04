import os
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField


# ──────────────────────────────────────────
# Existing models (DO NOT RENAME FIELDS)
# ──────────────────────────────────────────

class Experience(models.Model):
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=150, blank=True)

    start_date = models.CharField(max_length=30, default="", blank=True)
    end_date = models.CharField(max_length=30, default="", blank=True)

    description = models.TextField()

    technologies = models.JSONField(default=list, blank=True)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.company


class Education(models.Model):
    institute = models.CharField(max_length=250)
    degree = models.CharField(max_length=250)

    start_year = models.CharField(max_length=10, default="", blank=True)
    end_year = models.CharField(max_length=10, default="", blank=True)

    percentage = models.CharField(max_length=20, blank=True)

    description = models.TextField(blank=True)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.degree


# ──────────────────────────────────────────
# Singleton base mixin
# ──────────────────────────────────────────

class SingletonModel(models.Model):
    """
    Ensures only one row exists (pk=1).
    Subclasses get a classmethod `load()` that
    returns (or creates) the single instance safely.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Singletons cannot be deleted

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ──────────────────────────────────────────
# New CMS Models
# ──────────────────────────────────────────

class Hero(SingletonModel):
    name = models.CharField(max_length=200, default="")
    designation = models.CharField(max_length=200, default="")
    headline = models.CharField(max_length=300, default="")
    description = models.TextField(default="")
    profile_image = models.ImageField(upload_to="hero/", blank=True, null=True)
    background_image = models.ImageField(upload_to="hero/", blank=True, null=True)
    resume = models.FileField(upload_to="resume/", blank=True, null=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return f"Hero – {self.name}"


class About(SingletonModel):
    title = models.CharField(max_length=300, default="")
    description = models.TextField(default="")
    email = models.EmailField(default="")
    phone = models.CharField(max_length=30, default="")
    location = models.CharField(max_length=200, default="")
    experience_years = models.PositiveIntegerField(default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    clients = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return "About"


SKILL_CATEGORY_CHOICES = [
    ("Backend", "Backend"),
    ("Frontend", "Frontend"),
    ("AI", "AI"),
    ("ML", "ML"),
    ("Cloud", "Cloud"),
    ("Database", "Database"),
    ("DevOps", "DevOps"),
]


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=SKILL_CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    percentage = models.PositiveIntegerField(default=0, help_text="0–100")
    icon = models.CharField(max_length=100, blank=True, help_text="Icon class name, e.g. icon-cogs")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    tech_stack = models.JSONField(default=list)
    featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ImageField(upload_to="projects/gallery/")

    def __str__(self):
        return f"Image for {self.project.title}"


class Certification(models.Model):
    title = models.CharField(max_length=300)
    issuer = models.CharField(max_length=200)
    issue_date = models.CharField(max_length=50, default="", blank=True)
    certificate_image = models.ImageField(upload_to="certificates/", blank=True, null=True)
    certificate_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class Resume(SingletonModel):
    title = models.CharField(max_length=200, default="Resume")
    pdf = models.FileField(upload_to="resume/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Resume"

    def save(self, *args, **kwargs):
        # Delete old PDF file when replaced
        try:
            old = Resume.objects.get(pk=1)
            if old.pdf and old.pdf != self.pdf:
                old.pdf.delete(save=False)
        except Resume.DoesNotExist:
            pass
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Contact(SingletonModel):
    email = models.EmailField(default="")
    phone = models.CharField(max_length=30, default="")
    address = models.CharField(max_length=300, default="")
    google_map = models.TextField(blank=True, help_text="Google Maps embed URL or iframe src")

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return "Contact Info"


class SocialLink(models.Model):
    platform = models.CharField(max_length=100)
    url = models.URLField()
    icon = models.CharField(max_length=100, blank=True, help_text="Icon class name, e.g. icon-twitter")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "platform"]

    def __str__(self):
        return self.platform


class SEO(SingletonModel):
    site_title = models.CharField(max_length=200, default="Portfolio")
    meta_description = models.TextField(default="")
    keywords = models.CharField(max_length=500, default="")
    favicon = models.ImageField(upload_to="seo/", blank=True, null=True)
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True)

    class Meta:
        verbose_name = "SEO Settings"
        verbose_name_plural = "SEO Settings"

    def __str__(self):
        return "SEO Settings"
class Journal(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    author = models.CharField(max_length=100, default='Admin')
    read_time = models.CharField(max_length=50, help_text='e.g., 5 mins read')
    publish_date = models.DateField(default=timezone.now, blank=True, null=True, help_text='Publication Date')
    image = models.ImageField(upload_to='journal/', blank=True, null=True)
    excerpt = models.TextField(help_text='Short description for the popup preview')
    content = RichTextField(help_text='Full article content')
    external_urls = models.JSONField(default=list, blank=True, help_text='List of external links e.g. [{"title": "Medium", "url": "https://..."}]')
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Journal"
        verbose_name_plural = "Journals"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
