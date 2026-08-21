from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import request
from django.http import request
from django.shortcuts import redirect, render

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Company, Contact, Lead, Deal, Activity, Task, Note, Pipeline, PipelineStage, Tag    
from .permissions import (
    can_create,
    can_edit,
    can_delete,
    is_sales,
    is_support,
    is_viewer,
    can_manage_deals,
    can_edit_deal,
    can_delete_deal,
    can_change_deal_stage,
    can_manage_pipelines,
    )
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Sum
from .forms import LeadForm

from django.db import transaction
from .forms import LeadForm, LeadConversionForm

from django.contrib.auth.models import User
from .forms import DealForm
from .models import (
    Lead,
    Deal,
    Pipeline,
    PipelineStage,
    Company,
    Contact,
)

# Create your views here.

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    next_url = request.GET.get("next") or request.POST.get("next")

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
                    "Your account has been disabled. "
                    "Please contact an administrator."
                )

                return render(
                    request,
                    "auth/login.html",
                    {"next": next_url}
                )

            login(request, user)

            if next_url:
                return redirect(next_url)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "auth/login.html",
        {"next": next_url}
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

    if not can_create(request.user):
        raise PermissionDenied

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

    if not can_edit(request.user, company):
        raise PermissionDenied

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

    if not can_delete(request.user, company):
        raise PermissionDenied

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

# ==========================================================
# CONTACT VIEWS
# ==========================================================

@login_required
def contact_list(request):

    contacts = Contact.objects.select_related(
        "company",
        "owner"
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    company_id = request.GET.get(
        "company",
        ""
    ).strip()

    if search:

        contacts = contacts.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
            | Q(company__name__icontains=search)
        )

    if company_id:

        contacts = contacts.filter(
            company_id=company_id
        )

    companies = Company.objects.all()

    paginator = Paginator(
        contacts,
        10
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    context = {
        "contacts": page_obj.object_list,
        "page_obj": page_obj,
        "search": search,
        "selected_company": company_id,
        "companies": companies,
    }

    return render(
        request,
        "crmApp/contacts/contact_list.html",
        context
    )


@login_required
def contact_detail(request, pk):

    contact = get_object_or_404(
        Contact.objects
        .select_related("company", "owner")
        .prefetch_related("deals", "activities", "tasks", "contact_notes"),
        pk=pk
    )

    context = {
        "contact": contact,
        "deals": contact.deals.all(),
        "activities": contact.activities.all()[:10],
        "tasks": contact.tasks.all()[:10],
        "notes": contact.contact_notes.all()[:10],
    }

    return render(
        request,
        "crmApp/contacts/contact_detail.html",
        context
    )


@login_required
def contact_create(request):

    if not can_create(request.user):
        raise PermissionDenied

    company_id = request.GET.get(
        "company"
    )

    initial_company = None

    if company_id:

        initial_company = Company.objects.filter(
            pk=company_id
        ).first()

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        if not first_name:

            messages.error(
                request,
                "First name is required."
            )

            return render(
                request,
                "crmApp/contacts/contact_form.html",
                {
                    "contact": None,
                    "companies": Company.objects.all(),
                    "selected_company": initial_company,
                }
            )

        company_id = request.POST.get(
            "company"
        )

        company = None

        if company_id:

            company = Company.objects.filter(
                pk=company_id
            ).first()

        contact = Contact.objects.create(

            first_name=first_name,

            last_name=last_name,

            company=company,

            job_title=request.POST.get(
                "job_title",
                ""
            ).strip(),

            email=request.POST.get(
                "email",
                ""
            ).strip(),

            phone=request.POST.get(
                "phone",
                ""
            ).strip(),

            mobile=request.POST.get(
                "mobile",
                ""
            ).strip(),

            address=request.POST.get(
                "address",
                ""
            ).strip(),

            city=request.POST.get(
                "city",
                ""
            ).strip(),

            country=request.POST.get(
                "country",
                ""
            ).strip(),

            notes=request.POST.get(
                "notes",
                ""
            ).strip(),

            owner=request.user
        )

        messages.success(
            request,
            f"{contact.full_name} was created successfully."
        )

        return redirect(
            "contact_detail",
            pk=contact.pk
        )

    return render(
        request,
        "crmApp/contacts/contact_form.html",
        {
            "contact": None,
            "companies": Company.objects.all(),
            "selected_company": initial_company,
        }
    )


@login_required
def contact_edit(request, pk):

    contact = get_object_or_404(
        Contact,
        pk=pk
    )

    if not can_edit(request.user, contact):
        raise PermissionDenied

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        if not first_name:

            messages.error(
                request,
                "First name is required."
            )

            return render(
                request,
                "crmApp/contacts/contact_form.html",
                {
                    "contact": contact,
                    "companies": Company.objects.all(),
                }
            )

        company_id = request.POST.get(
            "company"
        )

        company = None

        if company_id:

            company = Company.objects.filter(
                pk=company_id
            ).first()

        contact.first_name = first_name

        contact.last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        contact.company = company

        contact.job_title = request.POST.get(
            "job_title",
            ""
        ).strip()

        contact.email = request.POST.get(
            "email",
            ""
        ).strip()

        contact.phone = request.POST.get(
            "phone",
            ""
        ).strip()

        contact.mobile = request.POST.get(
            "mobile",
            ""
        ).strip()

        contact.address = request.POST.get(
            "address",
            ""
        ).strip()

        contact.city = request.POST.get(
            "city",
            ""
        ).strip()

        contact.country = request.POST.get(
            "country",
            ""
        ).strip()

        contact.notes = request.POST.get(
            "notes",
            ""
        ).strip()

        contact.save()

        messages.success(
            request,
            f"{contact.full_name} was updated successfully."
        )

        return redirect(
            "contact_detail",
            pk=contact.pk
        )

    return render(
        request,
        "crmApp/contacts/contact_form.html",
        {
            "contact": contact,
            "companies": Company.objects.all(),
        }
    )


@login_required
def contact_delete(request, pk):

    contact = get_object_or_404(
        Contact,
        pk=pk
    )


    if not can_delete(request.user, contact):
        raise PermissionDenied

    if request.method == "POST":

        name = contact.full_name

        contact.delete()

        messages.success(
            request,
            f"{name} was deleted successfully."
        )

        return redirect(
            "contact_list"
        )

    return render(
        request,
        "crmApp/contacts/contact_confirm_delete.html",
        {
            "contact": contact
        }
    )

def permission_denied(request, exception=None):

    return render(
        request,
        "403.html",
        status=403
    )

# ==========================================================
# LEAD VIEWS
# ==========================================================

@login_required
def lead_list(request):
    base_leads = Lead.objects.all()
    total_leads = base_leads.count()

    assigned_leads = base_leads.filter(
    owner__isnull=False
    ).count()

    unassigned_leads = base_leads.filter(
    owner__isnull=True
    ).count()
    # Base queryset with query optimizations
    leads = Lead.objects.select_related(
        "owner",
        "converted_company",
        "converted_contact",
    ).prefetch_related(
        "tags"
    )

    # ==========================
    # SEARCH
    # ==========================
    search = request.GET.get("search", "").strip()
    if search:
        leads = leads.filter(
        Q(first_name__icontains=search)
        | Q(last_name__icontains=search)
        | Q(company_name__icontains=search)
        | Q(email__icontains=search)
        | Q(phone__icontains=search)
        | Q(job_title__icontains=search)
        | Q(description__icontains=search)
    )

    # ==========================
    # STATUS FILTER
    # ==========================
    status = request.GET.get("status", "").strip()
    if status:
        leads = leads.filter(status=status)

    # ==========================
    # SOURCE FILTER
    # ==========================
    source = request.GET.get("source", "").strip()
    if source:
        leads = leads.filter(source=source)

    # ==========================
    # OWNER FILTER
    # ==========================
    owner = request.GET.get("owner", "").strip()

    if owner == "unassigned":

        leads = leads.filter(
        owner__isnull=True
    )

    elif owner:

        leads = leads.filter(
        owner_id=owner
    )
    # ==========================
    # ORDERING
    # ==========================
    leads = leads.order_by("-created_at")

    # ==========================
    # PAGINATION
    # ==========================
    paginator = Paginator(leads, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)



    # ==========================
    # METRICS & STATS
    # ==========================
    # Evaluated across the filtered set or global model depending on UI needs
    new_count = Lead.objects.filter(
        status=Lead.STATUS_NEW
    ).count()

    qualified_count = Lead.objects.filter(
        status=Lead.STATUS_QUALIFIED
    ).count()

    pipeline_value = Lead.objects.aggregate(
        total=Sum("estimated_value")
    )["total"] or 0

    # PERMISSION ANNOTATIONS (PRESENTATION METADATA)
    for lead in page_obj.object_list:
        lead.user_can_edit = can_edit(request.user, lead)
        lead.user_can_convert = can_edit(request.user, lead)

    # ==========================
    # CONTEXT
    # ==========================
    context = {
        "leads": page_obj.object_list,
        "page_obj": page_obj,
        "search": search,
        "selected_status": status,
        "selected_source": source,
        "selected_owner": owner,
        "total_leads": total_leads,
        "assigned_leads": assigned_leads,
        "unassigned_leads": unassigned_leads,

        # Metrics
        "new_count": new_count,
        "qualified_count": qualified_count,
        "pipeline_value": pipeline_value,

        # Form Dropdown Choices
        "status_choices": Lead.STATUS_CHOICES,
        "source_choices": Lead.SOURCE_CHOICES,
        "owners": User.objects.filter(
            is_active=True
        ).order_by(
            "first_name",
            "last_name",
            "username"
        ),
        "can_create_lead": can_create(request.user),
    }

    return render(
        request,
        "crmApp/leads/list.html",
        context
    )

@login_required
def lead_create(request):

    if not can_create(request.user):
        raise PermissionDenied

    if request.method == "POST":

        form = LeadForm(request.POST)

        if form.is_valid():

            # ---------------------------------
            # DUPLICATE CHECK
            # ---------------------------------

            if (
                form.duplicate_leads.exists()
                and request.POST.get("confirm_duplicate") != "1"
            ):

                context = {
                    "form": form,
                    "duplicate_leads": form.duplicate_leads,
                    "duplicate_warning": True,
                }

                return render(
                    request,
                    "crmApp/leads/create.html",
                    context
                )

            # ---------------------------------
            # CREATE LEAD
            # ---------------------------------

            lead = form.save(commit=False)

            if is_sales(request.user):
                lead.owner = request.user

            lead.save()

            form.save_m2m()

            messages.success(
                request,
                f"Lead {lead.first_name} {lead.last_name} "
                "was created successfully."
            )

            return redirect("leads")

    else:

        form = LeadForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "crmApp/leads/create.html",
        context
    )


@login_required
def lead_detail(request, pk):

    lead = get_object_or_404(
        Lead.objects.select_related("owner", "converted_company", "converted_contact"),
        pk=pk
    )
    # Attach presentation metadata for permission control
    lead.user_can_edit = can_edit(request.user, lead)
    lead.user_can_convert = can_edit(request.user, lead)
    lead.user_can_delete = can_delete(request.user, lead)

    context = {
        "lead": lead,
    }

    return render(
        request,
        "crmApp/leads/detail.html",
        context
    )

@login_required
def lead_update(request, pk):

    lead = get_object_or_404(
        Lead.objects.select_related("owner", "converted_company", "converted_contact"),
        pk=pk
    )

    if not can_edit(request.user, lead):
        raise PermissionDenied

    if request.method == "POST":

        form = LeadForm(
            request.POST,
            instance=lead
        )

        if form.is_valid():

            lead = form.save()

            messages.success(
                request,
                f"Lead '{lead.first_name} {lead.last_name}' "
                "was updated successfully."
            )

            return redirect(
                "lead_detail",
                pk=lead.pk
            )

    else:

        form = LeadForm(
            instance=lead
        )

    context = {
        "form": form,
        "lead": lead,
    }

    return render(
        request,
        "crmApp/leads/edit.html",
        context
    )

@login_required
def lead_convert(request, pk):

    lead = get_object_or_404(
        Lead.objects.select_related(
            "converted_company",
            "converted_contact"
        ),
        pk=pk
    )


        # ==========================================
        # CONVERSION STATUS VALIDATION
        # ==========================================

    if lead.status == Lead.STATUS_CONVERTED:

        messages.warning(
        request,
        "This lead has already been converted."
        )

        return redirect(
            "lead_detail",
            pk=lead.pk
        )


    if lead.status != Lead.STATUS_QUALIFIED:

        messages.warning(
            request,
            "Only qualified leads can be converted. "
            "Please qualify this lead before converting it."
        )

        return redirect(
            "lead_detail",
            pk=lead.pk
        )

       

    if request.method == "POST":

        form = LeadConversionForm(
            request.POST
        )

        if form.is_valid():

            try:

                with transaction.atomic():

                    company = None
                    contact = None

                    # ==========================
                    # CREATE COMPANY
                    # ==========================

                    if form.cleaned_data["create_company"]:

                        company = Company.objects.create(
                            name=form.cleaned_data["company_name"]
                        )

                    # ==========================
                    # CREATE CONTACT
                    # ==========================

                    if form.cleaned_data["create_contact"]:

                        contact = Contact.objects.create(
                            first_name=form.cleaned_data[
                                "contact_first_name"
                            ],
                            last_name=form.cleaned_data[
                                "contact_last_name"
                            ],
                            email=form.cleaned_data[
                                "email"
                            ],
                            phone=form.cleaned_data[
                                "phone"
                            ],
                            company=company,
                        )

                    # ==========================
                    # UPDATE LEAD
                    # ==========================

                    lead.converted_company = company
                    lead.converted_contact = contact
                    lead.status = Lead.STATUS_CONVERTED

                    lead.save(
                        update_fields=[
                            "converted_company",
                            "converted_contact",
                            "status",
                            "updated_at",
                        ]
                    )

                messages.success(
                    request,
                    f"Lead '{lead.first_name} {lead.last_name}' "
                    "was converted successfully."
                )

                return redirect(
                    "lead_detail",
                    pk=lead.pk
                )

            except Exception:

                messages.error(
                    request,
                    "The lead could not be converted. "
                    "No changes were saved."
                )

    else:

        form = LeadConversionForm(
            initial={
                "company_name": lead.company_name,
                "contact_first_name": lead.first_name,
                "contact_last_name": lead.last_name,
                "email": lead.email,
                "phone": lead.phone,
            }
        )

    return render(
        request,
        "crmApp/leads/convert.html",
        {
            "lead": lead,
            "form": form,
        }
    )

@login_required
def lead_delete(request, pk):

    lead = get_object_or_404(
        Lead,
        pk=pk
    )

    if not can_delete(request.user, lead):
        raise PermissionDenied

    if request.method == "POST":

        lead_name = f"{lead.first_name} {lead.last_name}".strip()

        lead.delete()

        messages.success(
            request,
            f"Lead {lead_name} was deleted successfully."
        )

        return redirect("leads")

    return render(
        request,
        "crmApp/leads/delete.html",
        {
            "lead": lead,
        }
    )

@login_required
def deal_create(request):

    if not can_manage_deals(request.user):
        raise PermissionDenied

    if request.method == "POST":

        form = DealForm(request.POST)

        if form.is_valid():

            deal = form.save(commit=False)

            # Sales users automatically own deals they create.
            if is_sales(request.user):
                deal.owner = request.user

            deal.save()

            form.save_m2m()

            messages.success(
                request,
                f"Deal '{deal.name}' was created successfully."
            )

            return redirect(
                "deal_detail",
                pk=deal.pk
            )

    else:

        form = DealForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "crmApp/deals/create.html",
        context
    )







