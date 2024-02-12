from django.urls import path

from . import views

app_name = "quotes_app"

urlpatterns = [
    path("", views.QuotesListView.as_view(), name="index"),
    path("authors/<pk>", views.AuthorDetailView.as_view(), name="specific_author"),
    path("authors/", views.AuthorsListView.as_view(), name="all_authors"),
    path("tags/", views.TagsListView.as_view(), name="all_tags"),
    path(
        "tags/<str:tagname>", views.QuotesByTagListView.as_view(), name="specific_tag"
    ),
    path("sync_quotes/", views.sync, name="sync_quotes"),
]
