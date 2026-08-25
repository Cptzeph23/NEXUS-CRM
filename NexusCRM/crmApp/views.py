from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core import paginator
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
    can_manage_activities,
    can_delete_activity,
    can_edit_activity,
    can_view_activity,
    can_manage_tasks,
    can_delete_task,
    can_edit_task,
    can_view_task,
    
    )
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Sum
from .forms import LeadForm, TaskForm

from django.db import transaction
from .forms import LeadForm, LeadConversionForm

from django.contrib.auth.models import User
from .forms import DealForm, ActivityForm
from .models import (
    Lead,
    Deal,
    Pipeline,
    PipelineStage,
    Company,
    Contact,
    Activity,
    Task,
    Note,
    Tag,
)

from django.utils import timezone

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
        "activities": lead.activities.all(),
        "can_create_activity": can_manage_activities(
            request.user
        ),
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

@login_required
def deal_list(request):

    deals = Deal.objects.select_related(
        "company",
        "contact",
        "pipeline",
        "stage",
        "owner",
    ).prefetch_related(
        "tags"
    )

    # ==========================================================
    # SEARCH
    # ==========================================================

    search = request.GET.get("search", "").strip()

    if search:
        deals = deals.filter(
            Q(name__icontains=search)
            | Q(company__name__icontains=search)
            | Q(contact__first_name__icontains=search)
            | Q(contact__last_name__icontains=search)
        )

    # ==========================================================
    # FILTERS
    # ==========================================================

    pipeline_id = request.GET.get("pipeline", "").strip()
    stage_id = request.GET.get("stage", "").strip()
    owner_id = request.GET.get("owner", "").strip()

    if pipeline_id:
        deals = deals.filter(
            pipeline_id=pipeline_id
        )

    if stage_id:
        deals = deals.filter(
            stage_id=stage_id
        )

    if owner_id:
        deals = deals.filter(
            owner_id=owner_id
        )

    # ==========================================================
    # STATISTICS
    # ==========================================================

    total_deals = deals.count()

    open_deals = deals.filter(
        stage__is_closed=False
    ).count()

    won_deals = deals.filter(
        stage__is_won=True
    ).count()

    lost_deals = deals.filter(
        stage__is_closed=True,
        stage__is_won=False
    ).count()

    pipeline_value = deals.filter(
        stage__is_closed=False
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    weighted_pipeline_value = sum(
        (
            deal.amount *
            deal.stage.probability /
            100
        )
        for deal in deals.filter(
            stage__is_closed=False
        ).select_related("stage")
    )

    paginator = Paginator(deals, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "deals": deals,

        "total_deals": total_deals,
        "open_deals": open_deals,
        "won_deals": won_deals,
        "lost_deals": lost_deals,
        "pipeline_value": pipeline_value,
        "weighted_pipeline_value": weighted_pipeline_value,

        "pipelines": Pipeline.objects.filter(
            is_active=True
        ).order_by("name"),

        "stages": PipelineStage.objects.select_related(
            "pipeline"
        ).order_by(
            "pipeline",
            "order"
        ),

        "owners": User.objects.filter(
            is_active=True
        ).order_by(
            "first_name",
            "last_name",
            "username"
        ),

        "selected_pipeline": pipeline_id,
        "selected_stage": stage_id,
        "selected_owner": owner_id,
        "search": search,

        "can_create_deal": can_manage_deals(request.user),
    }

    return render(
        request,
        "crmApp/deals/list.html",
        context
    )

@login_required
def activity_create(request):

    if not can_manage_activities(request.user):
        raise PermissionDenied

    if request.method == "POST":

        form = ActivityForm(request.POST)

        if form.is_valid():

            activity = form.save(commit=False)

            activity.created_by = request.user

            activity.save()

            messages.success(
                request,
                f"Activity '{activity.subject}' was logged successfully."
            )

            return redirect("activities")

    else:

        form = ActivityForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "crmApp/activities/create.html",
        context
    )


@login_required
def activity_list(request):

    activities = Activity.objects.select_related(
        "company",
        "contact",
        "lead",
        "deal",
        "assigned_to",
        "created_by",
    )

    # ==========================================================
    # SEARCH
    # ==========================================================

    search = request.GET.get("search", "").strip()

    if search:
        activities = activities.filter(
            Q(subject__icontains=search)
            | Q(description__icontains=search)
            | Q(company__name__icontains=search)
            | Q(contact__first_name__icontains=search)
            | Q(contact__last_name__icontains=search)
            | Q(lead__first_name__icontains=search)
            | Q(lead__last_name__icontains=search)
            | Q(deal__name__icontains=search)
        )

    # ==========================================================
    # FILTERS
    # ==========================================================

    activity_type = request.GET.get(
        "activity_type",
        ""
    ).strip()

    assigned_to = request.GET.get(
        "assigned_to",
        ""
    ).strip()

    if activity_type:
        activities = activities.filter(
            activity_type=activity_type
        )

    if assigned_to:
        activities = activities.filter(
            assigned_to_id=assigned_to
        )
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()

    if date_from:
        activities = activities.filter(
            activity_date__date__gte=date_from
        )

    if date_to:
        activities = activities.filter(
            activity_date__date__lte=date_to
        )

    # ==========================================================
    # STATISTICS
    # ==========================================================

    total_activities = activities.count()

    calls = activities.filter(
        activity_type=Activity.TYPE_CALL
    ).count()

    emails = activities.filter(
        activity_type=Activity.TYPE_EMAIL
    ).count()

    meetings = activities.filter(
        activity_type=Activity.TYPE_MEETING
    ).count()

    upcoming_activities = activities.filter(
        activity_date__gte=timezone.now()
    ).count()
    sms = activities.filter(
        activity_type=Activity.TYPE_SMS
    ).count()
    other = activities.filter(
        activity_type=Activity.TYPE_OTHER
    ).count()


    paginator = Paginator(activities, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)



    # ==========================================================
    # CONTEXT
    # ==========================================================

    context = {
        "page_obj": page_obj,
        "activities": page_obj.object_list,
        "total_activities": total_activities,
        "calls": calls,
        "emails": emails,
        "meetings": meetings,
        "upcoming_activities": upcoming_activities,
        "sms": sms,
        "other": other,
        "activity_types": Activity.TYPE_CHOICES,

        "users": User.objects.filter(
            is_active=True
        ).order_by(
            "first_name",
            "last_name",
            "username"
        ),

        "selected_activity_type": activity_type,
        "selected_assigned_to": assigned_to,
        "search": search,

        "can_create_activity": can_manage_activities(
            request.user
        ),
    }

    return render(
        request,
        "crmApp/activities/list.html",
        context
    )


@login_required
def activity_detail(request, pk):

    activity = get_object_or_404(
        Activity.objects.select_related(
            "company",
            "contact",
            "lead",
            "deal",
            "assigned_to",
            "created_by",
        ),
        pk=pk,
    )

    context = {
        "activity": activity,

        "can_edit": can_edit_activity(
            request.user,
            activity
        ),

        "can_delete": can_delete_activity(
            request.user,
            activity
        ),
    }

    return render(request, "crmApp/activities/detail.html", context)

@login_required
def activity_edit(request, pk):

    activity = get_object_or_404(
        Activity.objects.select_related(
            "company",
            "contact",
            "lead",
            "deal",
            "assigned_to",
            "created_by",
        ),
        pk=pk,
    )

    if not can_edit_activity(
        request.user,
        activity
    ):
        raise PermissionDenied

    if request.method == "POST":

        form = ActivityForm(
            request.POST,
            instance=activity
        )

        if form.is_valid():

            updated_activity = form.save()

            messages.success(
                request,
                f"Activity '{updated_activity.subject}' "
                "was updated successfully."
            )

            return redirect(
                "activity_detail",
                pk=updated_activity.pk
            )

    else:

        form = ActivityForm(
            instance=activity
        )

    context = {
        "form": form,
        "activity": activity,
    }

    return render(
        request,
        "crmApp/activities/edit.html",
        context
    )


@login_required
def activity_delete(request, pk):

    activity = get_object_or_404(
        Activity,
        pk=pk
    )

    if not can_delete_activity(
        request.user,
        activity
    ):
        raise PermissionDenied

    if request.method == "POST":

        subject = activity.subject

        activity.delete()

        messages.success(
            request,
            f"Activity '{subject}' was deleted successfully."
        )

        return redirect("activities")

    return render(
        request,
        "crmApp/activities/delete.html",
        {
            "activity": activity,
        }
    )



@login_required
def deal_detail(request, pk):

    deal = get_object_or_404(
        Deal.objects.select_related(
            "company",
            "contact",
            "pipeline",
            "stage",
            "owner",
        ).prefetch_related(
            "tags",
            "activities",
        ),
        pk=pk,
    )

    context = {
        "deal": deal,
        "activities": deal.activities.all(),
        "can_edit": can_edit_deal(
            request.user,
            deal
        ),

        "can_delete": can_delete_deal(
            request.user,
            deal
        ),
        "can_change_stage": can_change_deal_stage(
            request.user,
            deal
        ),
        "can_create_activity": can_manage_activities(
            request.user
        ),
    }


    return render(
        request,
        "crmApp/deals/detail.html",
        context
    )

@login_required
def deal_edit(request, pk):

    deal = get_object_or_404(
        Deal.objects.select_related(
            "company",
            "contact",
            "pipeline",
            "stage",
            "owner",
        ).prefetch_related("tags"),
        pk=pk,
    )

    if not can_edit_deal(request.user, deal):
        raise PermissionDenied

    if request.method == "POST":

        form = DealForm(
            request.POST,
            instance=deal
        )

        if form.is_valid():

            updated_deal = form.save(commit=False)

            # Sales users retain ownership of their own deals.
            # They must not be able to reassign ownership.
            if is_sales(request.user):
                updated_deal.owner = request.user

            updated_deal.save()

            form.save_m2m()

            messages.success(
                request,
                f"Deal '{updated_deal.name}' was updated successfully."
            )

            return redirect(
                "deal_detail",
                pk=updated_deal.pk
            )

    else:

        form = DealForm(
            instance=deal
        )

    context = {
        "form": form,
        "deal": deal,
    }

    return render(
        request,
        "crmApp/deals/edit.html",
        context
    )

@login_required
def deal_delete(request, pk):

    deal = get_object_or_404(
        Deal.objects.select_related(
            "company",
            "contact",
            "pipeline",
            "stage",
            "owner",
        ),
        pk=pk,
    )

    if not can_delete_deal(request.user, deal):
        raise PermissionDenied

    deal_name = deal.name

    if request.method == "POST":

        deal.delete()

        messages.success(
            request,
            f"Deal '{deal_name}' was deleted successfully."
        )

        return redirect("deals")

    context = {
        "deal": deal,
    }

    return render(
        request,
        "crmApp/deals/delete.html",
        context
    )

@login_required
def task_create(request):

    if not can_manage_tasks(request.user):
        raise PermissionDenied

    # ------------------------------------------------------
    # CONTEXTUAL RELATIONSHIPS
    # ------------------------------------------------------

    company_id = request.GET.get("company")
    contact_id = request.GET.get("contact")
    lead_id = request.GET.get("lead")
    deal_id = request.GET.get("deal")

    initial = {}

    if company_id:
        initial["company"] = company_id

    if contact_id:
        initial["contact"] = contact_id

    if lead_id:
        initial["lead"] = lead_id

    if deal_id:
        initial["deal"] = deal_id

    # ------------------------------------------------------
    # FORM
    # ------------------------------------------------------

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.created_by = request.user

            task.save()

            messages.success(
                request,
                f"Task '{task.title}' was created successfully."
            )

            return redirect(
                "task_detail",
                pk=task.pk
            )

    else:

        form = TaskForm(
            initial=initial
        )

    context = {
        "form": form,
    }

    return render(
        request,
        "crmApp/tasks/create.html",
        context
    )

@login_required
def task_list(request):

    tasks = Task.objects.select_related(
        "company",
        "contact",
        "lead",
        "deal",
        "assigned_to",
        "created_by",
    )

    # ======================================================
    # SEARCH
    # ======================================================

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        tasks = tasks.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(company__name__icontains=search)
            | Q(contact__first_name__icontains=search)
            | Q(contact__last_name__icontains=search)
            | Q(lead__first_name__icontains=search)
            | Q(lead__last_name__icontains=search)
            | Q(deal__name__icontains=search)
        )

    # ======================================================
    # FILTERS
    # ======================================================

    status = request.GET.get(
        "status",
        ""
    ).strip()

    priority = request.GET.get(
        "priority",
        ""
    ).strip()

    assigned_to = request.GET.get(
        "assigned_to",
        ""
    ).strip()

    if status:
        tasks = tasks.filter(
            status=status
        )

    if priority:
        tasks = tasks.filter(
            priority=priority
        )

    if assigned_to:
        tasks = tasks.filter(
            assigned_to_id=assigned_to
        )

    # ======================================================
    # DATE FILTERS
    # ======================================================

    date_from = request.GET.get(
        "date_from",
        ""
    ).strip()

    date_to = request.GET.get(
        "date_to",
        ""
    ).strip()

    if date_from:
        tasks = tasks.filter(
            due_date__date__gte=date_from
        )

    if date_to:
        tasks = tasks.filter(
            due_date__date__lte=date_to
        )

    # ======================================================
    # STATISTICS
    # ======================================================

    total_tasks = tasks.count()

    pending_tasks = tasks.filter(
        status=Task.STATUS_PENDING
    ).count()

    in_progress_tasks = tasks.filter(
        status=Task.STATUS_IN_PROGRESS
    ).count()

    completed_tasks = tasks.filter(
        status=Task.STATUS_COMPLETED
    ).count()

    overdue_tasks = tasks.filter(
        due_date__lt=timezone.now()
    ).exclude(
        status__in=[
            Task.STATUS_COMPLETED,
            Task.STATUS_CANCELLED,
        ]
    ).count()

    # ======================================================
    # PAGINATION
    # ======================================================

    paginator = Paginator(
        tasks,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    # ======================================================
    # CONTEXT
    # ======================================================

    context = {
        "page_obj": page_obj,
        "tasks": page_obj.object_list,

        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completed_tasks": completed_tasks,
        "overdue_tasks": overdue_tasks,

        "users": User.objects.filter(
            is_active=True
        ).order_by(
            "first_name",
            "last_name",
            "username"
        ),

        "status_choices": Task.STATUS_CHOICES,
        "priority_choices": Task.PRIORITY_CHOICES,

        "selected_status": status,
        "selected_priority": priority,
        "selected_assigned_to": assigned_to,

        "date_from": date_from,
        "date_to": date_to,
        "search": search,

        "can_create_task": can_manage_tasks(
            request.user
        ),
    }

    return render(
        request,
        "crmApp/tasks/list.html",
        context
    )

@login_required
def task_detail(request, pk):

    task = get_object_or_404(
        Task.objects.select_related(
            "company",
            "contact",
            "lead",
            "deal",
            "assigned_to",
            "created_by",
        ),
        pk=pk,
    )

    if not can_view_task(
        request.user,
        task
    ):
        raise PermissionDenied

    context = {
        "task": task,

        "can_edit": can_edit_task(
            request.user,
            task
        ),

        "can_delete": can_delete_task(
            request.user,
            task
        ),
    }

    return render(
        request,
        "crmApp/tasks/detail.html",
        context
    )


@login_required
def task_edit(request, pk):

    task = get_object_or_404(
        Task.objects.select_related(
            "company",
            "contact",
            "lead",
            "deal",
            "assigned_to",
            "created_by",
        ),
        pk=pk,
    )

    if not can_edit_task(
        request.user,
        task
    ):
        raise PermissionDenied

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():

            updated_task = form.save()

            messages.success(
                request,
                f"Task '{updated_task.title}' "
                "was updated successfully."
            )

            return redirect(
                "task_detail",
                pk=updated_task.pk
            )

    else:

        form = TaskForm(
            instance=task
        )

    context = {
        "form": form,
        "task": task,
    }

    return render(
        request,
        "crmApp/tasks/edit.html",
        context
    )


@login_required
def task_delete(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    if not can_delete_task(
        request.user,
        task
    ):
        raise PermissionDenied

    if request.method == "POST":

        title = task.title

        task.delete()

        messages.success(
            request,
            f"Task '{title}' was deleted successfully."
        )

        return redirect(
            "tasks"
        )

    return render(
        request,
        "crmApp/tasks/delete.html",
        {
            "task": task,
        }
    )

@login_required
def note_create(request):

    if not can_manage_notes(request.user):
        raise PermissionDenied

    # ------------------------------------------------------
    # CONTEXTUAL RELATIONSHIPS
    # ------------------------------------------------------

    company_id = request.GET.get("company")
    contact_id = request.GET.get("contact")
    lead_id = request.GET.get("lead")
    deal_id = request.GET.get("deal")

    initial = {}

    if company_id:
        initial["company"] = company_id

    if contact_id:
        initial["contact"] = contact_id

    if lead_id:
        initial["lead"] = lead_id

    if deal_id:
        initial["deal"] = deal_id

    # ------------------------------------------------------
    # FORM
    # ------------------------------------------------------

    if request.method == "POST":

        form = NoteForm(request.POST)

        if form.is_valid():

            note = form.save(commit=False)

            note.created_by = request.user

            note.save()

            messages.success(
                request,
                "Note was created successfully."
            )

            return redirect(
                "note_detail",
                pk=note.pk
            )

    else:

        form = NoteForm(
            initial=initial
        )

    context = {
        "form": form,
    }

    return render(
        request,
        "crmApp/notes/create.html",
        context
    )

@login_required
def note_list(request):

    notes = Note.objects.select_related(
        "company",
        "contact",
        "lead",
        "deal",
        "created_by",
    )

    # ======================================================
    # SEARCH
    # ======================================================

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        notes = notes.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(company__name__icontains=search)
            | Q(contact__first_name__icontains=search)
            | Q(contact__last_name__icontains=search)
            | Q(lead__first_name__icontains=search)
            | Q(lead__last_name__icontains=search)
            | Q(deal__name__icontains=search)
        )

    # ======================================================
    # PAGINATION
    # ======================================================

    paginator = Paginator(
        notes,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    context = {
        "page_obj": page_obj,
        "notes": page_obj.object_list,
        "search": search,

        "can_create_note": can_manage_notes(
            request.user
        ),
    }

    return render(
        request,
        "crmApp/notes/list.html",
        context
    )
