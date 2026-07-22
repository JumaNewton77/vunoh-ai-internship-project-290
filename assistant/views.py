from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from .forms import CustomUserCreationForm

from rest_framework.decorators import api_view
from rest_framework.response import Response

from PIL import Image
import pytesseract

from .services.ai_service import process_request
from .services.risk_service import calculate_risk
from .services.assignment_service import assign_employee

from .models import (
    Task,
    StatusHistory
)


@api_view(['POST'])
def ai_api(request):

    customer_request = request.data.get('customer_request')

    ai_response = process_request(customer_request)

    is_returning = (
        request.user.is_authenticated
        and Task.objects.filter(user=request.user).exists()
    )

    risk_result = calculate_risk(
        ai_response["intent"],
        ai_response["entities"],
        is_returning_customer=is_returning,
    )

    employee = assign_employee(ai_response["intent"])

    ai_response["risk_score"] = risk_result["score"]
    ai_response["risk_level"] = risk_result["level"]
    ai_response["risk_reasons"] = risk_result["reasons"]
    ai_response["employee_assignment"] = employee

    return Response(ai_response)


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')

        # Previously this fell through to render(request, 'login.html')
        # with no context at all on a failed login, so the template had
        # no way to know it should show an error message.
        return render(request, 'login.html', {'error': True})

    return render(request, 'login.html')


def register(request):

    form = CustomUserCreationForm()

    if request.method == "POST":

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'register.html', {'form': form})


def user_logout(request):

    logout(request)
    return redirect('login')


@login_required
def home(request):

    if request.method == "POST":

        customer_request = request.POST.get('customer_request')
        document = request.FILES.get('document')

        ai_response = process_request(customer_request)

        if document:
            try:
                image = Image.open(document)
                ocr_text = pytesseract.image_to_string(image)
                ai_response['ocr_text'] = ocr_text
            except Exception as e:
                ai_response['ocr_text'] = f"OCR failed: {str(e)}"

        is_returning = Task.objects.filter(user=request.user).exists()

        risk_result = calculate_risk(
            ai_response["intent"],
            ai_response["entities"],
            is_returning_customer=is_returning,
        )

        employee = assign_employee(ai_response["intent"])

        task = Task.objects.create(
            user=request.user,
            customer_request=customer_request,
            intent=ai_response['intent'],
            extracted_entities=ai_response.get('entities', {}),
            risk_score=risk_result["score"],
            employee_assignment=employee,
            generated_steps=ai_response.get('steps', ["Manual review"]),
            whatsapp_message=ai_response.get('whatsapp_message', 'Request received'),
            email_message=ai_response.get('email_message', 'Request received'),
            sms_message=ai_response.get('sms_message', 'Request received'),
            document=document
        )

        # Surface the risk level/reasons to the template even though
        # they aren't persisted as separate columns on Task - level is
        # derivable from risk_score (see Task.risk_level property).
        ai_response["risk_level"] = risk_result["level"]
        ai_response["risk_reasons"] = risk_result["reasons"]

        return render(
            request,
            'index.html',
            {
                'task': task,
                'response': ai_response
            }
        )

    return render(request, 'index.html')


@login_required
def dashboard(request):

    tasks = Task.objects.filter(user=request.user).order_by('-created_at')

    return render(
        request,
        'dashboard.html',
        {
            'tasks': tasks,
            'total_tasks': tasks.count(),
            'money_transfer_count': tasks.filter(intent='send_money').count(),
            'document_count': tasks.filter(intent='verify_document').count(),
            # Risk score is now 0-100 (was 0-10) - "High" is >= 61 per
            # the documented bands, so the dashboard threshold below
            # was updated to match.
            'high_risk_tasks': tasks.filter(risk_score__gte=61).count(),
            'completed': tasks.filter(status='Completed').count(),
            'pending': tasks.filter(status='Pending').count(),
            'in_progress': tasks.filter(status='In Progress').count(),
            'employees': tasks.values('employee_assignment').distinct().count()
        }
    )


@login_required
def task_detail(request, task_id):

    task = get_object_or_404(Task, id=task_id, user=request.user)

    return render(request, 'task_detail.html', {'task': task})


@login_required
def update_status(request, id):

    # Previously this looked up the task by id alone, with no check
    # that it belonged to request.user - any logged-in user could
    # update any other user's task by guessing/incrementing the id.
    # Scoped to the current user now, same as task_detail already was.
    task = get_object_or_404(Task, id=id, user=request.user)

    old_status = task.status
    task.status = request.POST["status"]
    task.save()

    StatusHistory.objects.create(
        task=task,
        old_status=old_status,
        new_status=task.status
    )

    return redirect("dashboard")


@login_required
def tasks(request):

    tasks = Task.objects.filter(user=request.user)

    return render(request, "tasks.html", {"tasks": tasks})


@login_required
def analytics(request):

    tasks = Task.objects.filter(user=request.user)

    return render(
        request,
        "analytics.html",
        {
            "high_risk": tasks.filter(risk_score__gte=61).count(),
            "money_transfer": tasks.filter(intent='send_money').count(),
            "documents": tasks.filter(intent='verify_document').count()
        }
    )


@login_required
def settings(request):

    return render(request, "settings.html")