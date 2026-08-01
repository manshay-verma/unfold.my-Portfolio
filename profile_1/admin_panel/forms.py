from django import forms
from profile_1.models import (
    Hero, About, Skill, Project, ProjectImage,
    Certification, Resume, Contact, SocialLink, SEO,
    Experience, Education,
)


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


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = [
            "title", "issuer", "issue_date",
            "certificate_image", "certificate_url", "display_order",
        ]


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
            "description": forms.Textarea(attrs={"rows": 4}),
            "technologies": forms.Textarea(attrs={"rows": 2, "placeholder": '["Python","Django"]'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            "institute", "degree",
            "start_year", "end_year",
            "percentage", "description", "display_order",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
