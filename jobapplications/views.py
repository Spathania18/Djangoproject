import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, request
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import applications
import datetime
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from .serializers import ApplicationSerializer
from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


def index(request):
    return render(request, 'index.html')

@login_required
def application(request):
    if request.method == 'POST':
        username = request.user.username
        company_name = request.POST['companyname'].title()  # Capitalize each word in the company name
        job_title = request.POST['jobtitle'].title()         # Capitalize each word in the job title
        job_type = request.POST['jobtype']
        applied_date = request.POST['applieddate']

        # Create the application object and save it
        application = applications.objects.create(
            username=username,
            company_name=company_name,
            job_title=job_title,
            job_type=job_type,
            applied_date=applied_date
        )

        application.save()

        messages.success(request, "Application submitted successfully.")
        return redirect('application')

    return render(request, 'application.html')


def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username= username, password = password)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'homepage.html', {"first_name": firstname})
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect(request, 'signin.html')



    return render(request, 'signin.html')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cnfpassword = request.POST['cnfpassword']

        newuser = User.objects.create_user(username, email, password)
        newuser.first_name = firstname
        newuser.last_name = lastname

        newuser.save()

        messages.success(request, "New User created successfully.")

        return redirect('signup')



    return render(request, 'signup.html')


@login_required
def homepage(request):
    return render(request, 'homepage.html')

@login_required
def allapplications(request):
    user_apps = applications.objects.filter(username=request.user.username)

    return render(request, 'allapplications.html', {'applications': user_apps})

@login_required
def dashboard(request):
    username = request.user.username

    # Count total applications for the logged-in user
    application_count = applications.objects.filter(username=username).count()
    
    # Count applications applied today for the logged-in user
    application_count_today = applications.objects.filter(
        username=username, 
        applied_date=datetime.date.today()
    ).count()

    # Count distinct companies the user has applied to
    distinct_companies_count = applications.objects.filter(username=username).values('company_name').distinct().count()

    # Data for charts
    # Job type distribution
    job_type_data = applications.objects.filter(username=username) \
        .values('job_type') \
        .annotate(count=Count('job_type')) \
        .order_by('-count')

    job_types = [entry['job_type'] for entry in job_type_data]
    job_type_counts = [entry['count'] for entry in job_type_data]

    # Applications by date
    applications_by_date = applications.objects.filter(username=username) \
        .values('applied_date') \
        .annotate(count=Count('id')) \
        .order_by('applied_date')

    application_dates = [entry['applied_date'].strftime('%Y-%m-%d') for entry in applications_by_date]
    application_date_counts = [entry['count'] for entry in applications_by_date]

    # Applications by company
    applications_by_company = applications.objects.filter(username=username) \
        .values('company_name') \
        .annotate(count=Count('company_name')) \
        .order_by('-count')

    company_names = [entry['company_name'] for entry in applications_by_company]
    company_counts = [entry['count'] for entry in applications_by_company]

    # Pass data to the template
    passthrough = {
        "application_count": application_count,
        "application_count_today": application_count_today,
        "distinct_companies_count": distinct_companies_count,
        "jobTypes": job_types,
        "jobTypeData": job_type_counts,
        "applicationDates": application_dates,
        "applicationDateCounts": application_date_counts,
        "companyNames": company_names,
        "companyCounts": company_counts,
    }

    return render(request, 'dashboard.html', passthrough)


# In progress filter code
'''
@login_required
@csrf_exempt
def filter_dashboard(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        job_type = data.get('job_type', 'all')
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)
        company = data.get('company', 'all')
        
        username = request.user.username
        filtered_applications = applications.objects.filter(username=username)

        # Filter by job type
        if job_type != 'all':
            filtered_applications = filtered_applications.filter(job_type=job_type)

        # Filter by date range
        if start_date and end_date:
            filtered_applications = filtered_applications.filter(applied_date__range=[start_date, end_date])

        # Filter by company
        if company != 'all':
            filtered_applications = filtered_applications.filter(company_name=company)

        # Recalculate data for the charts based on the filtered applications
        job_type_data = filtered_applications.values('job_type').annotate(count=Count('job_type')).order_by('-count')
        job_types = [entry['job_type'] for entry in job_type_data]
        job_type_counts = [entry['count'] for entry in job_type_data]

        applications_by_company = filtered_applications.values('company_name').annotate(count=Count('company_name')).order_by('-count')
        company_names = [entry['company_name'] for entry in applications_by_company]
        company_counts = [entry['count'] for entry in applications_by_company]

        applications_by_date = filtered_applications.values('applied_date').annotate(count=Count('id')).order_by('applied_date')
        application_dates = [entry['applied_date'] for entry in applications_by_date]
        application_date_counts = [entry['count'] for entry in applications_by_date]

        return JsonResponse({
            'jobTypes': job_types,
            'jobTypeData': job_type_counts,
            'companyNames': company_names,
            'companyCounts': company_counts,
            'applicationDates': application_dates,
            'applicationDateCounts': application_date_counts,
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)
    '''


@api_view(['GET'])
def dashboard_data(request):
    username = request.GET.get('username')
    
    if not username:
        return Response({"error": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST)

    application_count = applications.objects.filter(username=username).count()
    application_count_today = applications.objects.filter(username=username, applied_date=datetime.date.today()).count()
    distinct_companies_count = applications.objects.filter(username=username).values('company_name').distinct().count()

    job_type_data = applications.objects.filter(username=username) \
        .values('job_type') \
        .annotate(count=Count('job_type')) \
        .order_by('-count')

    job_types = [entry['job_type'] for entry in job_type_data]
    job_type_counts = [entry['count'] for entry in job_type_data]

    applications_by_year = applications.objects.filter(username=username) \
        .extra(select={'year': "strftime('%%Y', applied_date)"}) \
        .values('year') \
        .annotate(count=Count('id')) \
        .order_by('year')

    insightyear_labels = [entry['year'] for entry in applications_by_year]
    insightyear_counts = [entry['count'] for entry in applications_by_year]

    applications_by_company = applications.objects.filter(username=username) \
        .values('company_name') \
        .annotate(count=Count('company_name')) \
        .order_by('-count')

    company_names = [entry['company_name'] for entry in applications_by_company]
    company_counts = [entry['count'] for entry in applications_by_company]

    data = {
        "application_count": application_count,
        "application_count_today": application_count_today,
        "distinct_companies_count": distinct_companies_count,
        "jobTypes": job_types,
        "jobTypeData": job_type_counts,
        "insightyearLabels": insightyear_labels,
        "insightyearCounts": insightyear_counts,
        "companyNames": company_names,
        "companyCounts": company_counts
    }

    return Response(data)