from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Company, Contact

# Create your views here.

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.is_active:
                messages.error(
                    request,
                    "Your account has been disabled. Please contact an administrator."
                )

                return render(
                    request,
                    "auth/login.html"
                )

            login(request, user)

            next_url = request.POST.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "auth/login.html"
    )

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def module_placeholder(request, module_name):
    return render(request, "placeholder.html",
        {
            "module_name": module_name,
        }
    )

@login_required
def logout_view(request):

    if request.method == "POST":

        logout(request)

        return redirect("login")

    return redirect("dashboard")


# ==========================================================
# COMPANY VIEWS
# ==========================================================

@login_required
def company_list(request):

    companies = Company.objects.select_related(
        "owner"
    ).prefetch_related(
        "contacts"
    )

    search = request.GET.get("search", "").strip()
    industry = request.GET.get("industry", "").strip()
    country = request.GET.get("country", "").strip()

    if search:

        companies = companies.filter(
            Q(name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
            | Q(website__icontains=search)
        )

    if industry:
        companies = companies.filter(
            industry=industry
        )

    if country:
        companies = companies.filter(
            country=country
        )

    industries = (
        Company.objects
        .exclude(industry="")
        .values_list("industry", flat=True)
        .distinct()
        .order_by("industry")
    )

    countries = (
        Company.objects
        .exclude(country="")
        .values_list("country", flat=True)
        .distinct()
        .order_by("country")
    )

    paginator = Paginator(companies, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "companies": page_obj.object_list,
        "search": search,
        "selected_industry": industry,
        "selected_country": country,
        "industries": industries,
        "countries": countries,
    }

    return render(
        request,
        "crmApp/companies/company_list.html",
        context
    )


@login_required
def company_detail(request, pk):

    company = get_object_or_404(
        Company.objects
        .select_related("owner")
        .prefetch_related("contacts", "deals", "activities", "tasks", "notes"),
        pk=pk
    )

    context = {
        "company": company,
        "contacts": company.contacts.all(),
        "deals": company.deals.all(),
        "activities": company.activities.all()[:10],
        "tasks": company.tasks.all()[:10],
        "notes": company.notes.all()[:10],
    }

    return render(
        request,
        "crmApp/companies/company_detail.html",
        context
    )


@login_required
def company_create(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()

        if not name:

            messages.error(
                request,
                "Company name is required."
            )

            return render(
                request,
                "crmApp/companies/company_form.html",
                {"company": None}
            )

        company = Company.objects.create(

            name=name,

            industry=request.POST.get(
                "industry", ""
            ).strip(),

            website=request.POST.get(
                "website", ""
            ).strip(),

            email=request.POST.get(
                "email", ""
            ).strip(),

            phone=request.POST.get(
                "phone", ""
            ).strip(),

            address=request.POST.get(
                "address", ""
            ).strip(),

            city=request.POST.get(
                "city", ""
            ).strip(),

            country=request.POST.get(
                "country", ""
            ).strip(),

            description=request.POST.get(
                "description", ""
            ).strip(),

            owner=request.user
        )

        messages.success(
            request,
            f"{company.name} was created successfully."
        )

        return redirect(
            "company_detail",
            pk=company.pk
        )

    return render(
        request,
        "crmApp/companies/company_form.html",
        {"company": None}
    )


@login_required
def company_edit(request, pk):

    company = get_object_or_404(
        Company,
        pk=pk
    )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        if not name:

            messages.error(
                request,
                "Company name is required."
            )

            return render(
                request,
                "crmApp/companies/company_form.html",
                {"company": company}
            )

        company.name = name

        company.industry = request.POST.get(
            "industry",
            ""
        ).strip()

        company.website = request.POST.get(
            "website",
            ""
        ).strip()

        company.email = request.POST.get(
            "email",
            ""
        ).strip()

        company.phone = request.POST.get(
            "phone",
            ""
        ).strip()

        company.address = request.POST.get(
            "address",
            ""
        ).strip()

        company.city = request.POST.get(
            "city",
            ""
        ).strip()

        company.country = request.POST.get(
            "country",
            ""
        ).strip()

        company.description = request.POST.get(
            "description",
            ""
        ).strip()

        company.save()

        messages.success(
            request,
            f"{company.name} was updated successfully."
        )

        return redirect(
            "company_detail",
            pk=company.pk
        )

    return render(
        request,
        "crmApp/companies/company_form.html",
        {"company": company}
    )


@login_required
def company_delete(request, pk):

    company = get_object_or_404(
        Company,
        pk=pk
    )

    if request.method == "POST":

        name = company.name

        company.delete()

        messages.success(
            request,
            f"{name} was deleted successfully."
        )

        return redirect(
            "company_list"
        )

    return render(
        request,
        "crmApp/companies/company_confirm_delete.html",
        {"company": company}
    )