from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('finance', 'Finance'),
        ('legal', 'Legal'),
        ('operations', 'Operations'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )

    def __str__(self):
        return self.username


class Task(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ]

    INTENT_CHOICES = [
        ('send_money', 'Send Money'),
        ('hire_service', 'Hire Service'),
        ('verify_document', 'Verify Document'),
        ('airport_transfer', 'Airport Transfer'),
        ('check_status', 'Check Status')
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    task_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    customer_request = models.TextField(
        default="No request provided"
    )

    intent = models.CharField(
        max_length=50,
        choices=INTENT_CHOICES,
        default='check_status'
    )

    extracted_entities = models.JSONField(
        default=dict,
        blank=True,
        null=True
    )

    document = models.FileField(
        upload_to='documents/',
        null=True,
        blank=True
    )

    # Score is 0-100 - see assistant/services/risk_service.py for the
    # bands (0-30 Low, 31-60 Medium, 61-100 High) and the risk_level
    # property below, which derives the label from this score.
    risk_score = models.IntegerField(
        default=0
    )

    employee_assignment = models.CharField(
        max_length=100,
        default="Support Team"
    )

    generated_steps = models.JSONField(
        default=list,
        blank=True,
        null=True
    )

    whatsapp_message = models.TextField(
        default="Request received"
    )

    email_message = models.TextField(
        default="Your request is under review"
    )

    sms_message = models.TextField(
        default="Request received"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    @property
    def risk_level(self):
        """
        Derives Low/Medium/High from risk_score on the fly - no extra
        DB column or migration needed. Use in templates as
        {{ task.risk_level }}.
        """
        if self.risk_score <= 30:
            return "Low"
        elif self.risk_score <= 60:
            return "Medium"
        return "High"

    def save(self, *args, **kwargs):

        if not self.task_code:

            while True:

                code = f"VUN-{uuid.uuid4().hex[:8].upper()}"

                if not Task.objects.filter(task_code=code).exists():
                    self.task_code = code
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task_code}"


class StatusHistory(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='history'
    )

    old_status = models.CharField(
        max_length=50
    )

    new_status = models.CharField(
        max_length=50
    )

    changed_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return (
            f"{self.task.task_code}"
            f" : "
            f"{self.old_status}"
            f" → "
            f"{self.new_status}"
        )


class AuditLog(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    action = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.action[:50]