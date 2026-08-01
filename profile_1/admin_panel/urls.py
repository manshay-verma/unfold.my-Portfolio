from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path("",                   views.dashboard,           name="dashboard"),
    path("login/",             views.panel_login,         name="login"),
    path("logout/",            views.panel_logout,        name="logout"),
    path("hero/",              views.hero_edit,           name="hero"),
    path("about/",             views.about_edit,          name="about"),
    path("experience/",        views.experience_list,     name="experience"),
    path("experience/add/",    views.experience_add,      name="experience-add"),
    path("experience/<int:pk>/edit/",   views.experience_edit,   name="experience-edit"),
    path("experience/<int:pk>/delete/", views.experience_delete, name="experience-delete"),
    path("education/",         views.education_list,      name="education"),
    path("education/add/",     views.education_add,       name="education-add"),
    path("education/<int:pk>/edit/",   views.education_edit,   name="education-edit"),
    path("education/<int:pk>/delete/", views.education_delete, name="education-delete"),
    path("projects/",          views.project_list,        name="projects"),
    path("projects/add/",      views.project_add,         name="project-add"),
    path("projects/<int:pk>/edit/",   views.project_edit,   name="project-edit"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project-delete"),
    path("skills/",            views.skill_list,          name="skills"),
    path("skills/add/",        views.skill_add,           name="skill-add"),
    path("skills/<int:pk>/edit/",   views.skill_edit,   name="skill-edit"),
    path("skills/<int:pk>/delete/", views.skill_delete, name="skill-delete"),
    path("certificates/",      views.certification_list,  name="certifications"),
    path("certificates/add/",  views.certification_add,   name="certification-add"),
    path("certificates/<int:pk>/edit/",   views.certification_edit,   name="certification-edit"),
    path("certificates/<int:pk>/delete/", views.certification_delete, name="certification-delete"),
    path("resume/",            views.resume_edit,         name="resume"),
    path("contact/",           views.contact_edit,        name="contact"),
    path("social/",            views.social_list,         name="social"),
    path("social/add/",        views.social_add,          name="social-add"),
    path("social/<int:pk>/edit/",   views.social_edit,   name="social-edit"),
    path("social/<int:pk>/delete/", views.social_delete, name="social-delete"),
    path("seo/",               views.seo_edit,            name="seo"),
]
