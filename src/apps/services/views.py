from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Service, ServiceCategory


class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"
    paginate_by = 9

    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True).select_related("category")
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ServiceCategory.objects.all()
        context["page_title"] = "Услуги - Медицинский Диагностический Центр"
        context["selected_category"] = self.request.GET.get("category")
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "service"
    slug_field = "slug"
    slug_url_kwarg = "service_slug"

    def get_queryset(self):
        return Service.objects.filter(is_active=True).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.object.name} - Медицинский Диагностический Центр"
        return context


# Дополнительный view для поиска услуг
class ServiceSearchView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"
    paginate_by = 9

    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ServiceCategory.objects.all()
        context["page_title"] = "Поиск услуг - Медицинский Диагностический Центр"
        context["search_query"] = self.request.GET.get("q", "")
        return context
