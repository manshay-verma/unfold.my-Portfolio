from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Experience, Education,
    Hero, About, Skill, Project,
    Certification, Resume, Contact, SocialLink, SEO, Journal
)
from .serializers import (
    ExperienceSerializer, EducationSerializer,
    HeroSerializer, AboutSerializer, SkillSerializer, ProjectSerializer,
    CertificationSerializer, ResumeSerializer, ContactSerializer,
    SocialLinkSerializer, SEOSerializer, JournalSerializer
)


# ──────────────────────────────────────────
# Permission helper
# ──────────────────────────────────────────

SAFE_METHODS_ONLY = permissions.IsAuthenticatedOrReadOnly


# ──────────────────────────────────────────
# Existing ViewSets (keep unchanged behavior)
# ──────────────────────────────────────────

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [SAFE_METHODS_ONLY]


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [SAFE_METHODS_ONLY]


# ──────────────────────────────────────────
# New list/CRUD ViewSets
# ──────────────────────────────────────────

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [SAFE_METHODS_ONLY]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related("gallery_images").all()
    serializer_class = ProjectSerializer
    permission_classes = [SAFE_METHODS_ONLY]


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [SAFE_METHODS_ONLY]


class SocialLinkViewSet(viewsets.ModelViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    permission_classes = [SAFE_METHODS_ONLY]


# ──────────────────────────────────────────
# Singleton APIViews (GET + PATCH only)
# ──────────────────────────────────────────

class SingletonAPIView(APIView):
    """Generic base for singleton GET/PATCH endpoints."""
    model = None
    serializer_class = None

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get(self, request):
        obj = self.model.load()
        serializer = self.serializer_class(obj, context={"request": request})
        return Response(serializer.data)

    def patch(self, request):
        obj = self.model.load()
        serializer = self.serializer_class(
            obj, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class HeroAPIView(SingletonAPIView):
    model = Hero
    serializer_class = HeroSerializer


class AboutAPIView(SingletonAPIView):
    model = About
    serializer_class = AboutSerializer


class ResumeAPIView(SingletonAPIView):
    model = Resume
    serializer_class = ResumeSerializer


class ContactAPIView(SingletonAPIView):
    model = Contact
    serializer_class = ContactSerializer


class SEOAPIView(SingletonAPIView):
    model = SEO
    serializer_class = SEOSerializer


# ──────────────────────────────────────────
# Aggregate portfolio endpoint
# ──────────────────────────────────────────

class PortfolioAPIView(APIView):
    """
    GET /api/portfolio/
    Returns every CMS section in one response.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ctx = {"request": request}
        data = {
            "hero": HeroSerializer(Hero.load(), context=ctx).data,
            "about": AboutSerializer(About.load(), context=ctx).data,
            "experience": ExperienceSerializer(
                Experience.objects.all(), many=True, context=ctx
            ).data,
            "education": EducationSerializer(
                Education.objects.all(), many=True, context=ctx
            ).data,
            "skills": SkillSerializer(
                Skill.objects.all(), many=True, context=ctx
            ).data,
            "projects": ProjectSerializer(
                Project.objects.prefetch_related("gallery_images").all(),
                many=True, context=ctx,
            ).data,
            "certifications": CertificationSerializer(
                Certification.objects.all(), many=True, context=ctx
            ).data,
            "resume": ResumeSerializer(Resume.load(), context=ctx).data,
            "contact": ContactSerializer(Contact.load(), context=ctx).data,
            "social": SocialLinkSerializer(
                SocialLink.objects.all(), many=True, context=ctx
            ).data,
            "seo": SEOSerializer(SEO.load(), context=ctx).data,
            "journals": JournalSerializer(
                Journal.objects.all(), many=True, context=ctx
            ).data,
        }
        return Response(data)


# ──────────────────────────────────────────
# Template views
# ──────────────────────────────────────────

def home(request):
    return render(request, 'portfolio/base.html')


from django.shortcuts import get_object_or_404

def portfolio_single(request, name):
    project = get_object_or_404(Project, slug=name)
    return render(request, 'portfolio/portfolio-single.html', {'project': project})

def journal_single(request, slug):
    journal = get_object_or_404(Journal, slug=slug)
    return render(request, 'portfolio/journal-single.html', {'journal': journal})
