from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, ListView, UpdateView,
                                  View)
from quotes_app.models import Author, Quote, Tag  # noqa

from .forms import (AddAuthorForm, AddQuoteForm, AddTagForm, LoginForm,
                    RegisterForm, ResetForm)


def register(request):
    """
    The register function is responsible for handling the registration of new users.
    It first checks if the user is already authenticated, and if so redirects them to the index page.
    If not, it then checks whether or not a POST request has been made (i.e., whether or not a form has been submitted).
    If so, it creates an instance of RegisterForm with that data and validates it; if valid, saves the form's data as a new User object in our database and redirects to login page; otherwise renders register template with invalid form instance passed as context. If no POST request was made (i.e.,
    
    :param request: Get the request object
    :return: The rendered register
    :doc-author: Trelent
    """
    if request.user.is_authenticated:
        return redirect(to="quotes_app:index")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="users:login")
        else:
            return render(request, "users/register.html", context={"form": form})

    return render(request, "users/register.html", context={"form": RegisterForm()})


def sign_in(request):
    """
    The sign_in function is a view that allows users to sign in.
        If the user is already signed in, they are redirected to the index page.
        If the request method is POST, then we authenticate and log them in if their username and password match.
        Otherwise, we redirect them back to login with an error message.
    
    :param request: Pass the request object to the view
    :return: A redirect to the index page if the user is already authenticated
    :doc-author: Trelent
    """
    if request.user.is_authenticated:
        return redirect(to="quotes_app:index")
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user is None:
            messages.error(request, "Username or password didn't match")
            return redirect(to="users:login")
        login(request, user)
        return redirect(to="users:dashboard")
    return render(request, "users/login.html", context={"form": LoginForm()})


class EmailOnlyPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users:login')



# @login_required
@method_decorator(login_required, name="dispatch")
class DashboardView(ListView):
    model = Quote
    template_name = "users/dashboard.html"
    success_url = reverse_lazy("dashboard")
    context_object_name = "quotes"
    paginate_by = 2

    # ordering = ["date_created"]

    def get_queryset(self):
        """
        The get_queryset function is used to filter the queryset of objects that are displayed in the view.
        In this case, we're filtering it so that only objects created by the current user are shown.
        
        :param self: Represent the instance of the class
        :return: A queryset of all the objects created by a user
        :doc-author: Trelent
        """
        queryset = super(DashboardView, self).get_queryset()
        return queryset.filter(created_by=self.request.user).order_by("date_created")

    def get_context_data(self, **kwargs):
        """
        The get_context_data function is a method that Django calls when rendering the template.
        It allows you to add additional context variables to the template, which are then available in 
        the rendered HTML. In this case, we're adding three variables: quotes, authors and tags.
        
        :param self: Represent the instance of the class
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A dictionary of data that is used to render the template
        :doc-author: Trelent
        """
        context = super(DashboardView, self).get_context_data(**kwargs)
        quotes = Quote.objects.filter(created_by=self.request.user).order_by(
            "-date_created"
        )
        authors = Author.objects.filter(created_by=self.request.user).order_by(
            "-date_created"
        )
        tags = Tag.objects.filter(created_by=self.request.user).order_by(
            "-date_created"
        )
        paginator_quotes = Paginator(quotes, 4)
        # paginator_authors = Paginator(authors, 4)
        context["quotes"] = paginator_quotes
        context["authors"] = authors
        context["tags"] = tags
        return context


@method_decorator(login_required, name="dispatch")
class SignOutView(View):
    def get(self, request):
        logout(request)
        return redirect("quotes_app:index")


@method_decorator(login_required, name="dispatch")
class QuoteCreateView(CreateView):
    model = Quote
    form_class = AddQuoteForm
    template_name = "users/add_quote.html"
    success_url = reverse_lazy("users:dashboard")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class AuthorCreateView(CreateView):
    model = Author
    form_class = AddAuthorForm
    template_name = "users/add_author.html"
    success_url = reverse_lazy("users:dashboard")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class TagCreateView(CreateView):
    model = Tag
    form_class = AddTagForm
    template_name = "users/add_tag.html"
    success_url = reverse_lazy("users:dashboard")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class QuoteUpdateView(UpdateView):
    model = Quote
    form_class = AddQuoteForm
    template_name = "users/add_quote.html"
    success_url = reverse_lazy("users:dashboard")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("You are not allowed to edit this Quote.")
        return obj


@method_decorator(login_required, name="dispatch")
class QuoteDeleteView(DeleteView):
    model = Quote
    template_name = "users/delete_confirm_quote.html"
    success_url = reverse_lazy("users:dashboard")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("You are not allowed to delete this Quote.")
        return obj


@method_decorator(login_required, name="dispatch")
class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AddAuthorForm
    template_name = "users/add_author.html"
    success_url = reverse_lazy("users:dashboard")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("You are not allowed to edit this Author.")
        return obj


@method_decorator(login_required, name="dispatch")
class AuthorDeleteView(DeleteView):
    model = Author
    template_name = "users/delete_confirm_author.html"
    success_url = reverse_lazy("users:dashboard")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("You are not allowed to delete this Author.")
        return obj


@method_decorator(login_required, name="dispatch")
class TagUpdateView(UpdateView):
    model = Tag
    template_name = "users/add_tag.html"
    success_url = reverse_lazy("users:dashboard")
    form_class = AddTagForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("You are not allowed to edit this Author.")
        return obj


@method_decorator(login_required, name="dispatch")
class TagDeleteView(DeleteView):
    model = Tag
    template_name = "users/delete_confirm_tag.html"
    success_url = reverse_lazy("users:dashboard")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("You are not allowed to delete this Author.")
        return obj
