from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .services.ai_service import process_request
from .models import Task
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pytesseract
from PIL import Image


@api_view(['POST'])
def ai_api(request):
    customer_request = request.data.get('customer_request')
    ai_response = process_request(customer_request)
    return Response(ai_response)


def home(request):
    if request.method == 'POST':
        customer_request = request.POST.get('customer_request')
        document = request.FILES.get('document')

        ai_response = process_request(customer_request)

        # OCR extraction if a document is uploaded
        ocr_text = None
        if document:
            try:
                image = Image.open(document)
                ocr_text = pytesseract.image_to_string(image)
                ai_response['ocr_text'] = ocr_text
            except Exception as e:
                ai_response['ocr_text'] = f"OCR failed: {str(e)}"

        task = Task.objects.create(
            customer_request=customer_request,
            intent=ai_response['intent'],
            extracted_entities=ai_response['entities'],
            risk_score=ai_response['risk_score'],
            employee_assignment=ai_response['employee_assignment'],
            generated_steps=ai_response['steps'],
            whatsapp_message=ai_response['whatsapp_message'],
            email_message=ai_response['email_message'],
            sms_message=ai_response['sms_message'],
            document=document if document else None
        )

        return render(request, 'index.html', {
            'task': task,
            'response': ai_response
        })

    return render(request, 'index.html')


@login_required
def dashboard(request):
    tasks = Task.objects.all().order_by('-created_at')

    total_tasks = tasks.count()
    high_risk_tasks = tasks.filter(risk_score__gte=4).count()
    send_money_count = tasks.filter(intent='send_money').count()
    verify_document_count = tasks.filter(intent='verify_document').count()
    airport_transfer_count = tasks.filter(intent='airport_transfer').count()

    return render(request, 'dashboard.html', {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'high_risk_tasks': high_risk_tasks,
        'send_money_count': send_money_count,
        'verify_document_count': verify_document_count,
        'airport_transfer_count': airport_transfer_count,
    })


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {
        'task': task
    })
