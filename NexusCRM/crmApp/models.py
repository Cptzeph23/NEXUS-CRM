from decimal import Decimal

from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from .models import AuditLog
class Profile(models.Model):

    ROLE_ADMIN = "admin"
    ROLE_MANAGER = "manager"
    ROLE_SALES = "sales"
    ROLE_SUPPORT = "support"
    ROLE_VIEWER = "viewer"

    ROLE_CHOICES = [
        (ROLE_ADMIN, "Administrator"),
        (ROLE_MANAGER, "Manager"),
        (ROLE_SALES, "Sales Representative"),
        (ROLE_SUPPORT, "Support"),
        (ROLE_VIEWER, "Viewer"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default=ROLE_VIEWER
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    job_title = models.CharField(
        max_length=100,
        blank=True
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} Profile"

    @property
    def role_display(self):
        return self.get_role_display()


# ==========================================================
# COMPANY
# ==========================================================

class Company(models.Model):
    INDUSTRY_CHOICES = [
        ("technology", "Technology"),
        ("finance", "Finance"),
        ("healthcare", "Healthcare"),
        ("education", "Education"),
        ("retail", "Retail"),
        ("manufacturing", "Manufacturing"),
        ("real_estate", "Real Estate"),
        ("hospitality", "Hospitality"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200)
    industry = models.CharField(
        max_length=50,
        choices=INDUSTRY_CHOICES,
        blank=True
    )
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_companies"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
# CONTACT
# ==========================================================
class Contact(models.Model):
    STATUS_CHOICES = [
        ("lead", "Lead"),
        ("prospect", "Prospect"),
        ("customer", "Customer"),
        ("inactive", "Inactive"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contacts"
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_contacts"
    )

    job_title = models.CharField(max_length=150, blank=True)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=50, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="lead"
    )

    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# ==========================================================
# LEAD
# ==========================================================

class Lead(models.Model):

    STATUS_NEW = "new"
    STATUS_CONTACTED = "contacted"
    STATUS_QUALIFIED = "qualified"
    STATUS_UNQUALIFIED = "unqualified"
    STATUS_CONVERTED = "converted"

    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_CONTACTED, "Contacted"),
        (STATUS_QUALIFIED, "Qualified"),
        (STATUS_UNQUALIFIED, "Unqualified"),
        (STATUS_CONVERTED, "Converted"),
    ]

    SOURCE_WEBSITE = "website"
    SOURCE_REFERRAL = "referral"
    SOURCE_SOCIAL = "social"
    SOURCE_EMAIL = "email"
    SOURCE_CALL = "call"
    SOURCE_ADVERTISEMENT = "advertisement"
    SOURCE_OTHER = "other"

    SOURCE_CHOICES = [
        (SOURCE_WEBSITE, "Website"),
        (SOURCE_REFERRAL, "Referral"),
        (SOURCE_SOCIAL, "Social Media"),
        (SOURCE_EMAIL, "Email"),
        (SOURCE_CALL, "Phone Call"),
        (SOURCE_ADVERTISEMENT, "Advertisement"),
        (SOURCE_OTHER, "Other"),
    ]

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    job_title = models.CharField(
        max_length=150,
        blank=True
    )

    source = models.CharField(
        max_length=30,
        choices=SOURCE_CHOICES,
        default=SOURCE_OTHER
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )

    estimated_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_leads"
    )

    description = models.TextField(
        blank=True
    )

    tags = models.ManyToManyField(
        "Tag",
        blank=True,
        related_name="leads"
    )

    converted_company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="converted_leads"
    )

    converted_contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="converted_leads"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["source"]),
            models.Index(fields=["email"]),
            models.Index(fields=["owner"]),
        ]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


# ==========================================================
# PIPELINE
# ==========================================================

class Pipeline(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
# PIPELINE STAGE
# ==========================================================

class PipelineStage(models.Model):

    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        related_name="stages"
    )

    name = models.CharField(
        max_length=100
    )

    probability = models.PositiveIntegerField(
        default=0
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_closed = models.BooleanField(
        default=False
    )

    is_won = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["pipeline", "name"],
                name="unique_stage_name_per_pipeline"
            ),
            models.UniqueConstraint(
                fields=["pipeline", "order"],
                name="unique_stage_order_per_pipeline"
            ),
        ]

    def __str__(self):
        return f"{self.pipeline.name} - {self.name}"

    def clean(self):

        if self.probability > 100:
            raise ValidationError(
                {
                    "probability":
                    "Probability must be between 0 and 100."
                }
            )


# ==========================================================
# DEAL
# ==========================================================

class Deal(models.Model):

    name = models.CharField(
        max_length=200
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deals"
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deals"
    )

    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.PROTECT,
        related_name="deals"
    )

    stage = models.ForeignKey(
        PipelineStage,
        on_delete=models.PROTECT,
        related_name="deals"
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00"))
        ]
    )

    expected_close_date = models.DateField(
        null=True,
        blank=True
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_deals"
    )

    description = models.TextField(
        blank=True
    )

    tags = models.ManyToManyField(
        "Tag",
        blank=True,
        related_name="deals"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["pipeline"]),
            models.Index(fields=["stage"]),
            models.Index(fields=["owner"]),
            models.Index(fields=["expected_close_date"]),
        ]

    def __str__(self):
        return self.name

    def clean(self):

        if self.stage_id and self.pipeline_id:

            if self.stage.pipeline_id != self.pipeline_id:

                raise ValidationError(
                    {
                        "stage":
                        "The selected stage does not belong to this pipeline."
                    }
                )


# ==========================================================
# ACTIVITY
# ==========================================================

class Activity(models.Model):

    TYPE_CALL = "call"
    TYPE_EMAIL = "email"
    TYPE_MEETING = "meeting"
    TYPE_SMS = "sms"
    TYPE_OTHER = "other"

    TYPE_CHOICES = [
        (TYPE_CALL, "Call"),
        (TYPE_EMAIL, "Email"),
        (TYPE_MEETING, "Meeting"),
        (TYPE_SMS, "SMS"),
        (TYPE_OTHER, "Other"),
    ]

    subject = models.CharField(
        max_length=200
    )

    activity_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="activities"
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="activities"
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="activities"
    )

    deal = models.ForeignKey(
        Deal,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="activities"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities"
    )

    activity_date = models.DateTimeField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_activities"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-activity_date"]
        indexes = [
            models.Index(fields=["activity_date"]),
            models.Index(fields=["activity_type"]),
            models.Index(fields=["assigned_to"]),
        ]

    def __str__(self):
        return self.subject


# ==========================================================
# TASK
# ==========================================================

class Task(models.Model):

    PRIORITY_LOW = "low"
    PRIORITY_NORMAL = "normal"
    PRIORITY_HIGH = "high"
    PRIORITY_URGENT = "urgent"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_NORMAL, "Normal"),
        (PRIORITY_HIGH, "High"),
        (PRIORITY_URGENT, "Urgent"),
    ]

    STATUS_PENDING = "pending"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks"
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks"
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks"
    )

    deal = models.ForeignKey(
        Deal,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )

    due_date = models.DateTimeField(
        null=True,
        blank=True
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_NORMAL
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_tasks"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["due_date", "-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["due_date"]),
            models.Index(fields=["assigned_to"]),
        ]

    def __str__(self):
        return self.title


# ==========================================================
# Note
# ==========================================================

class Note(models.Model):

    title = models.CharField(
        max_length=200,
        blank=True
    )

    content = models.TextField()

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notes"
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="contact_notes"
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notes"
    )

    deal = models.ForeignKey(
        Deal,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notes"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_notes"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or "Untitled Note"


# ==========================================================
# AUDIT LOG / SYSTEM ACTIVITY
# ==========================================================

class AuditLog(models.Model):

    ACTION_CREATE = "create"
    ACTION_UPDATE = "update"
    ACTION_DELETE = "delete"
    ACTION_LOGIN = "login"
    ACTION_LOGOUT = "logout"
    ACTION_OTHER = "other"

    ACTION_CHOICES = [
        (ACTION_CREATE, "Created"),
        (ACTION_UPDATE, "Updated"),
        (ACTION_DELETE, "Deleted"),
        (ACTION_LOGIN, "Logged In"),
        (ACTION_LOGOUT, "Logged Out"),
        (ACTION_OTHER, "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs"
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES
    )

    model_name = models.CharField(
        max_length=100,
        blank=True
    )

    object_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    object_repr = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["action"]),
            models.Index(fields=["model_name"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.description or f"{self.action} - {self.model_name}"




# ==========================================================
# NOTIFICATION
# ==========================================================

class Notification(models.Model):

    TYPE_INFO = "info"
    TYPE_SUCCESS = "success"
    TYPE_WARNING = "warning"
    TYPE_DANGER = "danger"

    TYPE_CHOICES = [
        (TYPE_INFO, "Info"),
        (TYPE_SUCCESS, "Success"),
        (TYPE_WARNING, "Warning"),
        (TYPE_DANGER, "Danger"),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_INFO
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["recipient", "is_read"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"


# ==========================================================
# CALENDAR EVENT
# ==========================================================

class CalendarEvent(models.Model):

    EVENT_TYPE_CHOICES = [
        ("meeting", "Meeting"),
        ("call", "Call"),
        ("task", "Task"),
        ("reminder", "Reminder"),
        ("other", "Other"),
    ]

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default="meeting"
    )

    start_datetime = models.DateTimeField()

    end_datetime = models.DateTimeField(
        null=True,
        blank=True
    )

    all_day = models.BooleanField(
        default=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="calendar_events"
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="calendar_events"
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="calendar_events"
    )

    deal = models.ForeignKey(
        Deal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="calendar_events"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_calendar_events"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_calendar_events"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["start_datetime"]

        indexes = [
            models.Index(fields=["start_datetime"]),
            models.Index(fields=["event_type"]),
            models.Index(fields=["assigned_to"]),
        ]

    def __str__(self):
        return self.title

# ==========================================================
# TAG
# ==========================================================

class Tag(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
# ==========================================================
# USER PREFERENCES
# ==========================================================

class UserPreference(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="preferences"
    )

    # Appearance
    theme = models.CharField(
        max_length=20,
        choices=[
            ("light", "Light"),
            ("dark", "Dark"),
            ("system", "System Default"),
        ],
        default="light"
    )

    sidebar_collapsed = models.BooleanField(
        default=False
    )

    # Dashboard
    dashboard_layout = models.CharField(
        max_length=30,
        choices=[
            ("default", "Default"),
            ("compact", "Compact"),
            ("comfortable", "Comfortable"),
        ],
        default="default"
    )

    # Notifications
    email_notifications = models.BooleanField(
        default=True
    )

    task_notifications = models.BooleanField(
        default=True
    )

    activity_notifications = models.BooleanField(
        default=True
    )

    # Display
    items_per_page = models.PositiveIntegerField(
        choices=[
            (10, "10"),
            (25, "25"),
            (50, "50"),
            (100, "100"),
        ],
        default=25
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} Preferences"


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "action",
        "model_name",
        "object_id",
        "ip_address",
        "created_at",
    )

    list_filter = (
        "action",
        "model_name",
        "created_at",
    )

    search_fields = (
        "description",
        "model_name",
        "object_id",
        "user__username",
        "user__first_name",
        "user__last_name",
        "ip_address",
    )

    readonly_fields = (
        "user",
        "action",
        "model_name",
        "object_id",
        "description",
        "ip_address",
        "created_at",
    )















