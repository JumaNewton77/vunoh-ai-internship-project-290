from django.db import models
import uuid


class Task(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    INTENT_CHOICES = [
        ('send_money', 'Send Money'),
        ('hire_service', 'Hire Service'),
        ('verify_document', 'Verify Document'),
        ('airport_transfer', 'Airport Transfer'),
        ('check_status', 'Check Status'),
    ]

    task_code = models.CharField(max_length=20, unique=True, blank=True)

    customer_request = models.TextField()

    intent = models.CharField(
        max_length=50,
        choices=INTENT_CHOICES
    )

    extracted_entities = models.JSONField()

    document = models.FileField(upload_to='documents/', null=True, blank=True)


    risk_score = models.IntegerField(default=0)

    employee_assignment = models.CharField(max_length=100)

    generated_steps = models.JSONField()

    whatsapp_message = models.TextField()

    email_message = models.TextField()

    sms_message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.task_code:
            self.task_code = f"VUN-{uuid.uuid4().hex[:8].upper()}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.task_code