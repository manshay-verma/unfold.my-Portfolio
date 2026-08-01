"""
Admin Panel Views — /admin-panel/*
All views require staff login (login_required + is_staff check via decorator).
"""

from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from profile_1.models import (
    Hero, About, Skill, Project, ProjectImage,
    Certification, Resume, Contact, SocialLink, SEO,
    Experience, Education,
)
from .forms import (
    HeroForm, AboutForm, SkillForm, ProjectForm,
    CertificationForm, ResumeForm, ContactForm,
    SocialLinkForm, SEOForm, ExperienceForm, EducationForm,
)


# ──────────────────────────────────────────
# Auth decorator
# ──────────────────────────────────────────

def staff_required(view_func):
    """Redirect to panel login if not a logged-in staff/superuser."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff):
            return redirect("admin_panel:login")
        return view_func(request, *args, **kwargs)
    return wrapper


# ──────────────────────────────────────────
# Auth views
# ──────────────────────────────────────────

def panel_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_panel:dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect("admin_panel:dashboard")
        messages.error(request, "Invalid credentials or insufficient permissions.")
    return render(request, "admin-panel/login.html")


def panel_logout(request):
    logout(request)
    return redirect("admin_panel:login")


# ──────────────────────────────────────────
# Dashboard
# ──────────────────────────────────────────

@staff_required
def dashboard(request):
    ctx = {
        "experience_count":    Experience.objects.count(),
        "education_count":     Education.objects.count(),
        "skills_count":        Skill.objects.count(),
        "projects_count":      Project.objects.count(),
        "certifications_count": Certification.objects.count(),
        "social_count":        SocialLink.objects.count(),
    }
    return render(request, "admin-panel/dashboard.html", ctx)


# ──────────────────────────────────────────
# Hero
# ──────────────────────────────────────────

@staff_required
def hero_edit(request):
    obj = Hero.load()
    if request.method == "POST":
        form = HeroForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Hero section updated.")
            return redirect("admin_panel:hero")
    else:
        form = HeroForm(instance=obj)
    return render(request, "admin-panel/hero.html", {"form": form, "obj": obj})


# ──────────────────────────────────────────
# About
# ──────────────────────────────────────────

@staff_required
def about_edit(request):
    obj = About.load()
    if request.method == "POST":
        form = AboutForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "About section updated.")
            return redirect("admin_panel:about")
    else:
        form = AboutForm(instance=obj)
    return render(request, "admin-panel/about.html", {"form": form, "obj": obj})


# ──────────────────────────────────────────
# Experience
# ──────────────────────────────────────────

@staff_required
def experience_list(request):
    items = Experience.objects.all()
    return render(request, "admin-panel/experience.html", {"items": items})


@staff_required
def experience_add(request):
    if request.method == "POST":
        form = ExperienceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience added.")
            return redirect("admin_panel:experience")
    else:
        form = ExperienceForm()
    return render(request, "admin-panel/experience_form.html", {"form": form, "action": "Add"})


@staff_required
def experience_edit(request, pk):
    obj = get_object_or_404(Experience, pk=pk)
    if request.method == "POST":
        form = ExperienceForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience updated.")
            return redirect("admin_panel:experience")
    else:
        form = ExperienceForm(instance=obj)
    return render(request, "admin-panel/experience_form.html", {"form": form, "action": "Edit"})


@staff_required
def experience_delete(request, pk):
    obj = get_object_or_404(Experience, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Experience deleted.")
    return redirect("admin_panel:experience")


# ──────────────────────────────────────────
# Education
# ──────────────────────────────────────────

@staff_required
def education_list(request):
    items = Education.objects.all()
    return render(request, "admin-panel/education.html", {"items": items})


@staff_required
def education_add(request):
    if request.method == "POST":
        form = EducationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Education added.")
            return redirect("admin_panel:education")
    else:
        form = EducationForm()
    return render(request, "admin-panel/education_form.html", {"form": form, "action": "Add"})


@staff_required
def education_edit(request, pk):
    obj = get_object_or_404(Education, pk=pk)
    if request.method == "POST":
        form = EducationForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Education updated.")
            return redirect("admin_panel:education")
    else:
        form = EducationForm(instance=obj)
    return render(request, "admin-panel/education_form.html", {"form": form, "action": "Edit"})


@staff_required
def education_delete(request, pk):
    obj = get_object_or_404(Education, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Education deleted.")
    return redirect("admin_panel:education")


# ──────────────────────────────────────────
# Projects
# ──────────────────────────────────────────

@staff_required
def project_list(request):
    items = Project.objects.prefetch_related("gallery_images").all()
    return render(request, "admin-panel/projects.html", {"items": items})


@staff_required
def project_add(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project added.")
            return redirect("admin_panel:projects")
    else:
        form = ProjectForm()
    return render(request, "admin-panel/project_form.html", {"form": form, "action": "Add"})


@staff_required
def project_edit(request, pk):
    obj = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated.")
            return redirect("admin_panel:projects")
    else:
        form = ProjectForm(instance=obj)
    return render(request, "admin-panel/project_form.html", {"form": form, "action": "Edit", "obj": obj})


@staff_required
def project_delete(request, pk):
    obj = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Project deleted.")
    return redirect("admin_panel:projects")


# ──────────────────────────────────────────
# Skills
# ──────────────────────────────────────────

@staff_required
def skill_list(request):
    items = Skill.objects.all()
    return render(request, "admin-panel/skills.html", {"items": items})


@staff_required
def skill_add(request):
    if request.method == "POST":
        form = SkillForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill added.")
            return redirect("admin_panel:skills")
    else:
        form = SkillForm()
    return render(request, "admin-panel/skill_form.html", {"form": form, "action": "Add"})


@staff_required
def skill_edit(request, pk):
    obj = get_object_or_404(Skill, pk=pk)
    if request.method == "POST":
        form = SkillForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated.")
            return redirect("admin_panel:skills")
    else:
        form = SkillForm(instance=obj)
    return render(request, "admin-panel/skill_form.html", {"form": form, "action": "Edit"})


@staff_required
def skill_delete(request, pk):
    obj = get_object_or_404(Skill, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Skill deleted.")
    return redirect("admin_panel:skills")


# ──────────────────────────────────────────
# Certifications
# ──────────────────────────────────────────

@staff_required
def certification_list(request):
    items = Certification.objects.all()
    return render(request, "admin-panel/certificates.html", {"items": items})


@staff_required
def certification_add(request):
    if request.method == "POST":
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Certification added.")
            return redirect("admin_panel:certifications")
    else:
        form = CertificationForm()
    return render(request, "admin-panel/certification_form.html", {"form": form, "action": "Add"})


@staff_required
def certification_edit(request, pk):
    obj = get_object_or_404(Certification, pk=pk)
    if request.method == "POST":
        form = CertificationForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Certification updated.")
            return redirect("admin_panel:certifications")
    else:
        form = CertificationForm(instance=obj)
    return render(request, "admin-panel/certification_form.html", {"form": form, "action": "Edit", "obj": obj})


@staff_required
def certification_delete(request, pk):
    obj = get_object_or_404(Certification, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Certification deleted.")
    return redirect("admin_panel:certifications")


# ──────────────────────────────────────────
# Resume
# ──────────────────────────────────────────

@staff_required
def resume_edit(request):
    obj = Resume.load()
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Resume updated.")
            return redirect("admin_panel:resume")
    else:
        form = ResumeForm(instance=obj)
    return render(request, "admin-panel/resume.html", {"form": form, "obj": obj})


# ──────────────────────────────────────────
# Contact
# ──────────────────────────────────────────

@staff_required
def contact_edit(request):
    obj = Contact.load()
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact info updated.")
            return redirect("admin_panel:contact")
    else:
        form = ContactForm(instance=obj)
    return render(request, "admin-panel/contact.html", {"form": form, "obj": obj})


# ──────────────────────────────────────────
# Social Links
# ──────────────────────────────────────────

@staff_required
def social_list(request):
    items = SocialLink.objects.all()
    return render(request, "admin-panel/social.html", {"items": items})


@staff_required
def social_add(request):
    if request.method == "POST":
        form = SocialLinkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Social link added.")
            return redirect("admin_panel:social")
    else:
        form = SocialLinkForm()
    return render(request, "admin-panel/social_form.html", {"form": form, "action": "Add"})


@staff_required
def social_edit(request, pk):
    obj = get_object_or_404(SocialLink, pk=pk)
    if request.method == "POST":
        form = SocialLinkForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Social link updated.")
            return redirect("admin_panel:social")
    else:
        form = SocialLinkForm(instance=obj)
    return render(request, "admin-panel/social_form.html", {"form": form, "action": "Edit"})


@staff_required
def social_delete(request, pk):
    obj = get_object_or_404(SocialLink, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Social link deleted.")
    return redirect("admin_panel:social")


# ──────────────────────────────────────────
# SEO
# ──────────────────────────────────────────

@staff_required
def seo_edit(request):
    obj = SEO.load()
    if request.method == "POST":
        form = SEOForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "SEO settings updated.")
            return redirect("admin_panel:seo")
    else:
        form = SEOForm(instance=obj)
    return render(request, "admin-panel/seo.html", {"form": form, "obj": obj})
