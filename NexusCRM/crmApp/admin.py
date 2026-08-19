from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

from .models import (
    Activity,
    Company,
    Contact,
    Deal,
    Lead,
    Note,
    Pipeline,
    PipelineStage,
    Profile,
    Tag,
    Task,
)

class ProfileInline(admin.StackedInline):

    model = Profile

    extra = 0

    fields = (
        "role",
        "phone",
        "job_title",
        "avatar",
    )

class CustomUserAdmin(UserAdmin):

    inlines = (
        ProfileInline,
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "industry",
        "email",
        "phone",
        "city",
        "country",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "city",
    )

    list_filter = (
        "industry",
        "country",
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "company",
        "job_title",
        "email",
        "phone",
        "status",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "company__name",
    )

    list_filter = (
        "status",
        "company",
        "country",
    )
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "last_name",
        "company_name",
        "email",
        "status",
        "source",
        "estimated_value",
        "owner",
        "created_at",
    )

    list_filter = (
        "status",
        "source",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "company_name",
        "email",
        "phone",
    )


class PipelineStageInline(admin.TabularInline):
    model = PipelineStage
    extra = 1
    ordering = ("order",)


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    inlines = [
        PipelineStageInline,
    ]


@admin.register(PipelineStage)
class PipelineStageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "pipeline",
        "probability",
        "order",
        "is_closed",
        "is_won",
    )

    list_filter = (
        "pipeline",
        "is_closed",
        "is_won",
    )

    ordering = (
        "pipeline",
        "order",
    )


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "company",
        "contact",
        "pipeline",
        "stage",
        "amount",
        "expected_close_date",
        "owner",
    )

    list_filter = (
        "pipeline",
        "stage",
        "expected_close_date",
    )

    search_fields = (
        "name",
        "company__name",
        "contact__first_name",
        "contact__last_name",
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "activity_type",
        "activity_date",
        "assigned_to",
        "created_by",
    )

    list_filter = (
        "activity_type",
        "activity_date",
    )

    search_fields = (
        "subject",
        "description",
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "assigned_to",
        "due_date",
        "priority",
        "status",
        "created_by",
    )

    list_filter = (
        "status",
        "priority",
        "due_date",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "created_by",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )