from django.contrib import admin
from .models import (
    Experience, Education,
    Hero, About, Skill, Project, ProjectImage,
    Certification, Resume, Contact, SocialLink, SEO,
)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("company", "position", "start_date", "end_date", "display_order")
    ordering = ("display_order",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("institute", "degree", "start_year", "end_year", "display_order")
    ordering = ("display_order",)


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ("name", "designation")


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "email", "phone", "experience_years", "projects_completed")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "percentage", "display_order")
    list_filter = ("category",)
    ordering = ("display_order",)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 2


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "featured", "display_order")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]
    ordering = ("display_order",)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "issue_date", "display_order")
    ordering = ("display_order",)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "address")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "display_order")
    ordering = ("display_order",)


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ("site_title", "keywords")
