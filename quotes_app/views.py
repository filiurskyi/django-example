from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from quotes_app.tasks import main_scrape

# Create your views here.
from .models import Author, Quote, Tag


class QuotesListView(ListView):
    model = Quote
    template_name = "quotes_app/index.html"
    success_url = reverse_lazy("index")
    context_object_name = "quotes"
    paginate_by = 6

    ordering = ["-date_created"]


class AuthorsListView(ListView):
    model = Author
    template_name = "quotes_app/all_authors.html"
    success_url = reverse_lazy("authors/")
    context_object_name = "authors"
    paginate_by = 40

    # ordering = ["fullname"]  -- examle of ordering

    def get_queryset(self):
        queryset = super(AuthorsListView, self).get_queryset()
        return queryset.order_by("fullname")


class AuthorDetailView(DetailView):
    model = Author
    template_name = "quotes_app/single_author.html"
    success_url = reverse_lazy("specific_author")
    context_object_name = "author"
    paginate_quotes_by = 6

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        obj_list = (
            Quote.objects.filter(author=self.object).order_by("-date_created").all()
        )
        paginator = Paginator(obj_list, self.paginate_quotes_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


class TagsListView(ListView):
    model = Tag
    template_name = "quotes_app/all_tags.html"
    success_url = reverse_lazy("all_tags")
    context_object_name = "tags"
    paginate_by = 40

    ordering = ["word"]


class QuotesByTagListView(ListView):
    model = Quote
    template_name = "quotes_app/specific_tag.html"
    success_url = reverse_lazy("specific_tag")
    context_object_name = "quotes"
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuotesByTagListView, self).get_context_data(
            object_list=object_list, **kwargs
        )
        obj_list = (
            Quote.objects.filter(tags__word=self.kwargs["tagname"])
            .order_by("-date_created")
            .all()
        )
        paginator = Paginator(obj_list, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


def sync(request):
    main_scrape.delay()

    return redirect("users:dashboard")
