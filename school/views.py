from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from .forms import EmployeeSignUpForm, EmployerSignUpForm, MailUpdateForm, EmailForm
from .models import Employer, CustomUser, MailDetails, Email
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

def home_view(request):
    return render(request, 'home.html')

def employer_signup(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'employer'
            user.save()
            company_name = request.POST['company_name']
            employer = Employer(user=user, company_name=company_name)
            employer.save()
            context = {'user': user}
            return render(request, 'employer_dashboard.html', context)
    else:
        form = EmployerSignUpForm()
    return render(request, 'signup.html', {'form': form})

def employee_signup(request):
    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'employee'
            user.save()
            context = {'user': user}
            return render(request, 'employee_dashboard.html', context)
    else:
        form = EmployeeSignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            userdata = CustomUser.objects.get(username=username)
            if userdata is not None and userdata.password == password:
                context = {'user': userdata}
                if userdata.user_type == 'employee':
                    return render(request, 'employee_dashboard.html', context)
                elif userdata.user_type == 'employer':
                    return render(request, 'employer_dashboard.html', context)
            else:
                error_message = "Invalid username or password"
                return render(request, 'login.html', {'error_message': error_message})
        except ObjectDoesNotExist:
            error_message = "The user does not exist."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def mail_details(request):
    if request.method == 'POST':
        form = MailUpdateForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            encrypted_password = make_password(password)
            if MailDetails.objects.filter(email=email).exists():
                form = MailUpdateForm()
                mail_details_list = MailDetails.objects.all()
            else:
                mail_details = MailDetails(email=email, encrypted_password=encrypted_password)
                mail_details.save()
                form = MailUpdateForm()
                mail_details_list = MailDetails.objects.all()
            return render(request, 'mail_setup.html', {'form': form, 'mail_details_list': mail_details_list})
    else:
        form = MailUpdateForm()
        mail_details_list = MailDetails.objects.all()  # Retrieve all mail details
        return render(request, 'mail_setup.html', {'form': form, 'mail_details_list': mail_details_list})

def delete_mail_details(request):
    MailDetails.objects.all().delete()
    return redirect('mail_details')

def send_email(request):
    error_message = ""
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            entered_password = form.cleaned_data['password']
            mail_details = MailDetails.objects.first()
            if mail_details is None:
                error_message = 'From mail and password has to be entered using Employer Dashboard'
            else:
                if check_password(entered_password, mail_details.encrypted_password):
                    # Send email
                    send_mail(
                        subject,
                        message,
                        mail_details.email,
                        [recipient_email],
                        fail_silently=False,
                        auth_user=mail_details.email,
                        auth_password=entered_password,
                    )
                    # Store the details of the scent email in the Email model
                    Email.objects.create(
                        recipient_email=recipient_email,
                        subject=subject,
                        message=message
                    )
                    error_message = "Email sent successfully"
                else:
                    error_message = "Wrong password"
    else:
        form = EmailForm()
    return render(request, 'send_email.html', {'form': form, 'error_message': error_message})

def sent_emails(request):
    emails = Email.objects.all()
    return render(request, 'sent_emails.html', {'emails': emails})

def user_logout(request):
    logout(request)
    return redirect('home')

def employee_home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'employee_dashboard.html', context)

def employer_home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'employer_dashboard.html', context)
