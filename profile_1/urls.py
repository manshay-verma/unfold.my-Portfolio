from django.urls import path, include
from rest_framework.routers import DefaultRouter

import profile_1.views as v
from profile_1.admin_panel import views as admin_views

# ──────────────────────────────────────────
# DRF Router (list + CRUD resources)
# ──────────────────────────────────────────
router = DefaultRouter()
router.register(r"experience", v.ExperienceViewSet, basename="experience")
router.register(r"education",  v.EducationViewSet,  basename="education")
router.register(r"skills",     v.SkillViewSet,      basename="skill")
router.register(r"projects",   v.ProjectViewSet,    basename="project")
router.register(r"certifications", v.CertificationViewSet, basename="certification")
router.register(r"social",     v.SocialLinkViewSet, basename="social")

urlpatterns = [

    # ── Public portfolio frontend ──────────────────────────────────────────────
    path("", v.home, name="home"),
    path("portfolio-single/<slug:name>/", v.portfolio_single, name="portfolio_single"),
    path("journal/<slug:slug>/", v.journal_single, name="journal_single"),

    # ── REST API ───────────────────────────────────────────────────────────────
    path("api/",            include(router.urls)),
    path("api/hero/",       v.HeroAPIView.as_view(),    name="api-hero"),
    path("api/about/",      v.AboutAPIView.as_view(),   name="api-about"),
    path("api/resume/",     v.ResumeAPIView.as_view(),  name="api-resume"),
    path("api/contact/",    v.ContactAPIView.as_view(), name="api-contact"),
    path("api/seo/",        v.SEOAPIView.as_view(),     name="api-seo"),
    path("api/portfolio/",  v.PortfolioAPIView.as_view(), name="api-portfolio"),

    # ── Admin Panel ────────────────────────────────────────────────────────────
    path("admin-panel/", include("profile_1.admin_panel.urls")),
]
