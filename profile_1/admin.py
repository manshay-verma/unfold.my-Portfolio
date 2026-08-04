from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import (
    Experience, Education,
    Hero, About, Skill, Project, ProjectImage,
    Certification, Resume, Contact, SocialLink, SEO,
    Journal
)


@admin.register(Experience)
class ExperienceAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("company", "position", "start_date", "end_date", "display_order")
    ordering = ("display_order",)


@admin.register(Education)
class EducationAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("institute", "degree", "start_year", "end_year", "display_order")
    ordering = ("display_order",)


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ("name", "designation")


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "email", "phone", "experience_years", "projects_completed")


@admin.register(Skill)
class SkillAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "category", "percentage", "display_order")
    list_filter = ("category",)
    ordering = ("display_order",)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 2


@admin.register(Project)
class ProjectAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "slug", "featured", "display_order")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]
    ordering = ("display_order",)


@admin.register(Certification)
class CertificationAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "issuer", "issue_date", "display_order")
    ordering = ("display_order",)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "address")


@admin.register(SocialLink)
class SocialLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("platform", "url", "display_order")
    ordering = ("display_order",)


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ("site_title", "keywords")

@admin.register(Journal)
class JournalAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'display_order')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('display_order',)
