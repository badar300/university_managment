# dissertation_app/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib import messages
from subject_supervision.models import *
import random


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('passw')
        university_id = random.randint(100000, 999999)
        legal_status = 'Active'

        # Create a new user
        user = User.objects.create(email=email, username=username, password=password)

        # Create a new student
        student = Student.objects.create(
            user=user,
            university_id=university_id,
            LegalStatus=legal_status,
            role='Student'  # Default role for a student
        )
        return render(request, 'login.html', context={'success_message': 'You have successfully registered!'})
    return render(request, 'registration.html')


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = User.objects.filter(username=username, password=password).first()
        if not user:
            user = authenticate(username=username, password=password)
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('dashboard')

        else:
            # Authentication failed, display an error message
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})

        # If it's not a POST request, render the login page
    return render(request, 'login.html')


@csrf_exempt
def dashboard(request):
    user = request.user
    if hasattr(user, 'student') and not user.is_superuser:
        return redirect('/dissertations')  # Replace 'home' with the desired URL after successful login
    if hasattr(user, 'supervisor') and not user.is_superuser:
        return redirect('/dissertations')  # Replace 'home' with the desired URL after successful login
    else:
        students = Student.objects.filter()
        supervisor = Supervisor.objects.filter(job_title='teacher')
        return render(request, 'dashboard.html', {'students': students,
                                                  'supervisors': supervisor})  # Replace 'home' with the desired URL after successful login

        # If you want to access the corresponding User objects for these students
        # student_users = [student.user for student in students]


def all_students(request):
    students = Student.objects.all()
    return render(request, 'all_students.html', {'students': students})


def all_majors(request):
    user = request.user
    Majors = Major.objects.filter(std_id=user.student.id)
    return render(request, 'all_dessertations.html', {'majors': Majors})


def all_dissertations(request):
    user = request.user
    if hasattr(user, 'student'):
        theses = Dissertation.objects.filter(std_id=user.student.id)
    if hasattr(user, 'supervisor'):
        theses = Dissertation.objects.filter(supervis_id=user.supervisor.id)
    if user.is_superuser:
        theses = Dissertation.objects.all()
    return render(request, 'all_dessertations.html', {'dissertations': theses, 'user': request.user})


@csrf_exempt
def update_legal_status(request, student_id):
    try:
        # Get the student by ID
        student = Student.objects.get(id=student_id)

        # Update the legal status
        student.LegalStatus = 'Inactive'
        student.save()

        return JsonResponse({'message': 'Legal status updated successfully'})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)


@csrf_exempt
def delete_theses(request, theses_id):
    try:
        # Get the Dissertation by ID
        Dissertation.objects.get(id=theses_id).delete()
        theses = Dissertation.objects.all()
        return render(request, 'all_dessertations.html', {'dissertations': theses})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)


@csrf_exempt
def update_user_role(request, student_id):
    try:
        # Get the student by ID
        student = Student.objects.get(id=student_id)

        # Update the legal status
        student.role = 'External supervisor'
        student.save()

        return JsonResponse({'message': 'Legal status updated successfully'})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)


@csrf_exempt
def create_dissertation(request):
    if request.method == 'POST':
        data = request.POST  # Use request.POST or request.data depending on your data format
        try:
            # Extract data from the request
            std_id = int(data.get('std_id', 0))
            supervis_id = int(data.get('supervis_id', 0))
            title = data.get('title', 'No')
            faculty = data.get('faculty', '')
            institute = data.get('institute', '')
            department = data.get('department', '')
            sub_year = data.get('sub_year', '')
            def_year = data.get('def_year', '')
            def_grade = data.get('def_grade', '')

            # Create a new Dissertation instance and save it
            dissertation = Dissertation(
                std_id=std_id,
                supervis_id=supervis_id,
                title=title,
                faculty=faculty,
                institue=institute,
                department=department,
                sub_year=sub_year,
                def_year=def_year,
                def_grade=def_grade,
            )
            dissertation.save()

            return render(request, 'dashboard.html', {'msg': 'Theses Added Successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Invalid method'}, status=405)


@csrf_exempt
def update_title(request, theses_id):
    # Get the new title from the POST data
    new_title = request.POST.get('newTitle')
    dissertation = Dissertation.objects.get(id=theses_id)
    dissertation.title = new_title
    dissertation.save()

    # Update the title in the database or perform any desired action
    # ...

    # Return a JSON response indicating success
    return redirect('/dissertations')


def user_logout(request):
    logout(request)
    # Handle user logout
    return redirect('login')


# Add views for other actions (e.g., dissertation entry, supervisor registration, etc.)
