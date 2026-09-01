from rest_framework import serializers

from crmApp.models import (
    Company,
    Contact,
    Lead,
    Deal,
    Activity,
    Task,
    Note,
)


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = "__all__"


class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = "__all__"


class DealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deal
        fields = "__all__"


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = "__all__"