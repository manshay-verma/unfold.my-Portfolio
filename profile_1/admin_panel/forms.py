from django import forms
from django.db import models
from profile_1.models import (
    Hero, About, Skill, Project, ProjectImage,
    Certification, Resume, Contact, SocialLink, SEO,
    Experience, Education, Journal
)


def _auto_display_order(form_obj, model_class):
    """Auto-fills display_order with max(display_order) + 1 for new objects."""
    if not form_obj.instance.pk and "display_order" in form_obj.fields:
        if not form_obj.initial.get("display_order"):
            max_order = model_class.objects.aggregate(max_val=models.Max("display_order"))["max_val"]
            form_obj.fields["display_order"].initial = (max_order or 0) + 1


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = [
            "title", "slug", "author", "read_time", "publish_date",
            "image", "excerpt", "content", "external_urls", "display_order",
        ]
        widgets = {
            "publish_date": forms.DateInput(attrs={"type": "date"}),
            "excerpt": forms.Textarea(attrs={"rows": 3}),
            "external_urls": forms.Textarea(attrs={"rows": 2, "placeholder": '[{"title": "Medium", "url": "https://medium.com/..."}]'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _auto_display_order(self, Journal)


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = [
            "name", "designation", "headline", "description",
            "profile_image", "background_image", "resume",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = [
            "title", "description", "email", "phone", "location",
            "experience_years", "projects_completed", "clients",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "category", "percentage", "icon", "display_order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _auto_display_order(self, Skill)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title", "slug", "short_description", "description",
            "cover_image", "github_url", "live_url",
            "tech_stack", "featured", "display_order",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "tech_stack": forms.Textarea(attrs={"rows": 2, "placeholder": '["Python","Django"]'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _auto_display_order(self, Project)


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = [
            "title", "issuer", "issue_date",
            "certificate_image", "certificate_url", "display_order",
        ]
        widgets = {
            "issue_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _auto_display_order(self, Certification)


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["title", "pdf"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["email", "phone", "address", "google_map"]
        widgets = {
            "google_map": forms.Textarea(attrs={"rows": 3}),
        }


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ["platform", "url", "icon", "display_order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _auto_display_order(self, SocialLink)


class SEOForm(forms.ModelForm):
    class Meta:
        model = SEO
        fields = ["site_title", "meta_description", "keywords", "favicon", "og_image"]
        widgets = {
            "meta_description": forms.Textarea(attrs={"rows": 3}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            "company", "position", "location",
            "start_date", "end_date", "description",
            "technologies", "display_order",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "technologies": forms.Textarea(attrs={"rows": 2, "placeholder": '["Python","Django"]'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _auto_display_order(self, Experience)


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            "institute", "degree",
            "start_year", "end_year",
            "percentage", "description", "display_order",
        ]
        widgets = {
            "start_year": forms.DateInput(attrs={"type": "date"}),
            "end_year": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _auto_display_order(self, Education)
