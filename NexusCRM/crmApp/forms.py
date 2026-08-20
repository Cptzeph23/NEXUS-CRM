import re

from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):

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