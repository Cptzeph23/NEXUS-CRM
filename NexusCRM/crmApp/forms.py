import re

from django import forms
from .models import Lead, Deal, Pipeline, PipelineStage, Company, Contact
from django.db.models import Q
from django.contrib.auth.models import User
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
    Tag
)


def normalize_phone(phone):
    """
    Normalize a phone number for duplicate comparison.
    Keeps digits only.
    """
    if not phone:
        return ""

    return re.sub(r"\D", "", phone)

def find_duplicate_leads(data, exclude_pk=None):
    """
    Find existing leads that may represent the same prospect.

    Matching priority:
    1. Email
    2. Phone
    3. First name + last name + company
    """

    queryset = Lead.objects.all()

    if exclude_pk:
        queryset = queryset.exclude(pk=exclude_pk)

    email = (data.get("email") or "").strip().lower()
    phone = normalize_phone(data.get("phone"))

    first_name = (data.get("first_name") or "").strip().lower()
    last_name = (data.get("last_name") or "").strip().lower()
    company_name = (data.get("company_name") or "").strip().lower()

    duplicates = Lead.objects.none()

    if email:
        duplicates = queryset.filter(
            email__iexact=email
        )

    if phone:
        for lead in queryset.exclude(phone=""):

            if normalize_phone(lead.phone) == phone:
                duplicates = duplicates | Lead.objects.filter(pk=lead.pk)

    if first_name and last_name and company_name:

        name_company_matches = queryset.filter(
            first_name__iexact=first_name,
            last_name__iexact=last_name,
            company_name__iexact=company_name,
        )

        duplicates = duplicates | name_company_matches

    return duplicates.distinct()

def get_allowed_lead_statuses(current_status):
    """
    Return the statuses that a lead is allowed to transition to.

    A lead may also remain in its current status.
    """

    transitions = {
        Lead.STATUS_NEW: [
            Lead.STATUS_NEW,
            Lead.STATUS_CONTACTED,
            Lead.STATUS_UNQUALIFIED,
        ],

        Lead.STATUS_CONTACTED: [
            Lead.STATUS_CONTACTED,
            Lead.STATUS_QUALIFIED,
            Lead.STATUS_UNQUALIFIED,
        ],

        Lead.STATUS_QUALIFIED: [
            Lead.STATUS_QUALIFIED,
            Lead.STATUS_CONVERTED,
            Lead.STATUS_UNQUALIFIED,
        ],

        Lead.STATUS_UNQUALIFIED: [
            Lead.STATUS_UNQUALIFIED,
            Lead.STATUS_NEW,
        ],

        Lead.STATUS_CONVERTED: [
            Lead.STATUS_CONVERTED,
        ],
    }

    return transitions.get(
        current_status,
        [current_status]
    )


class LeadForm(forms.ModelForm):
    duplicate_leads = None

    class Meta:



        model = Lead

        fields = [
            "first_name",
            "last_name",
            "company_name",
            "email",
            "phone",
            "job_title",
            "source",
            "status",
            "estimated_value",
            "owner",
            "description",
        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last name",
                }
            ),

            "company_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "name@example.com",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone number",
                }
            ),

            "job_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Job title",
                }
            ),

            "source": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "estimated_value": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "owner": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Add additional information about this lead...",
                }
            ),
        }

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "company_name": "Company",
            "job_title": "Job Title",
            "estimated_value": "Estimated Value",
            "owner": "Lead Owner",
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Default to allowing all choices (e.g. when creating a new lead)
        allowed_statuses = [choice[0] for choice in Lead.STATUS_CHOICES]

        # Restrict status choices when editing an existing Lead
        if self.instance and self.instance.pk:

            current_status = self.instance.status

            allowed_statuses = get_allowed_lead_statuses(
                current_status
            )

        self.fields["status"].choices = [
            (value, label)
            for value, label in Lead.STATUS_CHOICES
            if value in allowed_statuses
        ]


    def clean(self):

        cleaned_data = super().clean()

        self.duplicate_leads = find_duplicate_leads(
            cleaned_data,
            exclude_pk=self.instance.pk if self.instance.pk else None
        )

        # ---------------------------------
        # STATUS TRANSITION VALIDATION
        # ---------------------------------

        if self.instance and self.instance.pk:

            current_status = self.instance.status
            new_status = cleaned_data.get("status")

            allowed_statuses = get_allowed_lead_statuses(
                current_status
            )

            if (
                new_status
                and new_status not in allowed_statuses
            ):

                self.add_error(
                    "status",
                    "This lead cannot transition "
                    f"from {self.instance.get_status_display()} "
                    f"to {dict(Lead.STATUS_CHOICES).get(new_status, new_status)}."
                )

        return cleaned_data

       

    def clean_estimated_value(self):
        value = self.cleaned_data.get("estimated_value")

        if value is not None and value < 0:
            raise forms.ValidationError(
                "Estimated value cannot be negative."
            )

        return value

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        if not phone:
            return phone

        allowed_pattern = r"^[0-9+\-\(\)\s\.]+$"

        if not re.match(allowed_pattern, phone):
            raise forms.ValidationError(
                "Enter a valid phone number."
            )

        digits = re.sub(r"\D", "", phone)

        if len(digits) < 7:
            raise forms.ValidationError(
                "Phone number is too short."
            )

        return phone


    

class LeadConversionForm(forms.Form):

    create_company = forms.BooleanField(
        required=False,
        initial=True,
        label="Create Company"
    )

    create_contact = forms.BooleanField(
        required=False,
        initial=True,
        label="Create Contact"
    )

    company_name = forms.CharField(
        max_length=200,
        required=False
    )

    contact_first_name = forms.CharField(
        max_length=100,
        required=False
    )

    contact_last_name = forms.CharField(
        max_length=100,
        required=False
    )

    email = forms.EmailField(
        required=False
    )

    phone = forms.CharField(
        max_length=30,
        required=False
    )
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            if name in [
                "create_company",
                "create_contact",
            ]:

                field.widget.attrs["class"] = "form-check-input"

            else:

                field.widget.attrs["class"] = "form-control"

def clean(self):

    cleaned_data = super().clean()

    create_company = cleaned_data.get("create_company")
    create_contact = cleaned_data.get("create_contact")

    company_name = cleaned_data.get("company_name")
    first_name = cleaned_data.get("contact_first_name")

    if not create_company and not create_contact:
        raise forms.ValidationError(
            "Select at least one conversion option."
        )

    if create_company and not company_name:
        self.add_error(
            "company_name",
            "Company name is required when creating a company."
        )

    if create_contact and not first_name:
        self.add_error(
            "contact_first_name",
            "First name is required when creating a contact."
        )

    return cleaned_data       


class DealForm(forms.ModelForm):

    class Meta:

        model = Deal

        fields = [
            "name",
            "company",
            "contact",
            "pipeline",
            "stage",
            "amount",
            "expected_close_date",
            "owner",
            "description",
            "tags",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Deal name",
                }
            ),

            "company": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "contact": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "pipeline": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "stage": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "expected_close_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "owner": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Add additional information about this deal...",
                }
            ),

            "tags": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                }
            ),
        }

        labels = {
            "name": "Deal Name",
            "company": "Company",
            "contact": "Contact",
            "pipeline": "Pipeline",
            "stage": "Stage",
            "amount": "Deal Amount",
            "expected_close_date": "Expected Close Date",
            "owner": "Deal Owner",
            "description": "Description",
            "tags": "Tags",
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # --------------------------------------------------
        # DEFAULT QUERYSETS
        # --------------------------------------------------

        self.fields["company"].queryset = (
            Company.objects.order_by("name")
        )

        self.fields["contact"].queryset = (
            Contact.objects.select_related("company")
            .order_by("first_name", "last_name")
        )

        self.fields["pipeline"].queryset = (
            Pipeline.objects.filter(
                is_active=True
            ).order_by("name")
        )

        self.fields["owner"].queryset = (
            User.objects.filter(
                is_active=True
            ).order_by(
                "first_name",
                "last_name",
                "username"
            )
        )

        # --------------------------------------------------
        # STAGE QUERYSET
        # --------------------------------------------------

        pipeline_id = None

        # Existing deal
        if self.instance and self.instance.pk:
            pipeline_id = self.instance.pipeline_id

        # Submitted pipeline during create/edit
        if self.is_bound:
            submitted_pipeline = self.data.get(
                self.add_prefix("pipeline")
            )

            if submitted_pipeline:
                try:
                    pipeline_id = int(submitted_pipeline)
                except (TypeError, ValueError):
                    pass

        if pipeline_id:
            self.fields["stage"].queryset = (
                PipelineStage.objects.filter(
                    pipeline_id=pipeline_id
                ).order_by("order")
            )
        else:
            self.fields["stage"].queryset = (
                PipelineStage.objects.none()
            )

    def clean(self):

        cleaned_data = super().clean()

        pipeline = cleaned_data.get("pipeline")
        stage = cleaned_data.get("stage")

        if pipeline and stage:

            if stage.pipeline_id != pipeline.id:

                self.add_error(
                    "stage",
                    "The selected stage does not belong to "
                    "the selected pipeline."
                )

        return cleaned_data

class ActivityForm(forms.ModelForm):

    class Meta:

        model = Activity

        fields = [
            "subject",
            "activity_type",
            "description",
            "company",
            "contact",
            "lead",
            "deal",
            "assigned_to",
            "activity_date",
        ]

        widgets = {

            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Activity subject",
                }
            ),

            "activity_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Add activity details...",
                }
            ),

            "company": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "contact": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "lead": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "deal": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "activity_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
        }

        labels = {
            "subject": "Subject",
            "activity_type": "Activity Type",
            "description": "Description",
            "company": "Company",
            "contact": "Contact",
            "lead": "Lead",
            "deal": "Deal",
            "assigned_to": "Assigned To",
            "activity_date": "Activity Date",
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["company"].queryset = (
            Company.objects.order_by("name")
        )

        self.fields["contact"].queryset = (
            Contact.objects.select_related(
                "company"
            ).order_by(
                "first_name",
                "last_name"
            )
        )

        self.fields["lead"].queryset = (
            Lead.objects.order_by(
                "first_name",
                "last_name"
            )
        )

        self.fields["deal"].queryset = (
            Deal.objects.order_by("name")
        )

        self.fields["assigned_to"].queryset = (
            User.objects.filter(
                is_active=True
            ).order_by(
                "first_name",
                "last_name",
                "username"
            )
        )

        # --------------------------------------------------
        # OPTIONAL RELATIONSHIPS
        # --------------------------------------------------

        self.fields["company"].required = False
        self.fields["contact"].required = False
        self.fields["lead"].required = False
        self.fields["deal"].required = False
        self.fields["assigned_to"].required = False


class TaskForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            "title",
            "description",
            "company",
            "contact",
            "lead",
            "deal",
            "assigned_to",
            "due_date",
            "priority",
            "status",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Task title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Add task details...",
                }
            ),

            "company": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "contact": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "lead": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "deal": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "due_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

        labels = {
            "title": "Task Title",
            "description": "Description",
            "company": "Company",
            "contact": "Contact",
            "lead": "Lead",
            "deal": "Deal",
            "assigned_to": "Assigned To",
            "due_date": "Due Date",
            "priority": "Priority",
            "status": "Status",
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # --------------------------------------------------
        # RELATED CRM RECORDS
        # --------------------------------------------------

        self.fields["company"].queryset = (
            Company.objects.order_by("name")
        )

        self.fields["contact"].queryset = (
            Contact.objects.select_related(
                "company"
            ).order_by(
                "first_name",
                "last_name"
            )
        )

        self.fields["lead"].queryset = (
            Lead.objects.order_by(
                "first_name",
                "last_name"
            )
        )

        self.fields["deal"].queryset = (
            Deal.objects.order_by("name")
        )

        self.fields["assigned_to"].queryset = (
            User.objects.filter(
                is_active=True
            ).order_by(
                "first_name",
                "last_name",
                "username"
            )
        )

        # --------------------------------------------------
        # OPTIONAL RELATIONSHIPS
        # --------------------------------------------------

        self.fields["company"].required = False
        self.fields["contact"].required = False
        self.fields["lead"].required = False
        self.fields["deal"].required = False
        self.fields["assigned_to"].required = False
        self.fields["due_date"].required = False



# ==========================================================
# NOTE FORM
# ==========================================================

class NoteForm(forms.ModelForm):

    class Meta:

        model = Note

        fields = [
            "title",
            "content",
            "company",
            "contact",
            "lead",
            "deal",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Note title",
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 7,
                    "placeholder": "Write your note...",
                }
            ),

            "company": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "contact": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "lead": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "deal": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

        labels = {
            "title": "Note Title",
            "content": "Content",
            "company": "Company",
            "contact": "Contact",
            "lead": "Lead",
            "deal": "Deal",
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # --------------------------------------------------
        # RELATED CRM RECORDS
        # --------------------------------------------------

        self.fields["company"].queryset = (
            Company.objects.order_by("name")
        )

        self.fields["contact"].queryset = (
            Contact.objects.select_related(
                "company"
            ).order_by(
                "first_name",
                "last_name"
            )
        )

        self.fields["lead"].queryset = (
            Lead.objects.order_by(
                "first_name",
                "last_name"
            )
        )

        self.fields["deal"].queryset = (
            Deal.objects.order_by("name")
        )

        # --------------------------------------------------
        # OPTIONAL RELATIONSHIPS
        # --------------------------------------------------

        self.fields["title"].required = False
        self.fields["company"].required = False
        self.fields["contact"].required = False
        self.fields["lead"].required = False
        self.fields["deal"].required = False