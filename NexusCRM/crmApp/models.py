from django.db import models
from django.contrib.auth.models import User


# Create your models here.
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
        (ROLE_SUPPORT, "SUpport"),
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
        upload_to="avaters/",
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} Profile"

    @property
    def role_display(self):
        return self.get_role_display()



