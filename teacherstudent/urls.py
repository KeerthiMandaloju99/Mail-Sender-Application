"""
URL configuration for teacherstudent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from school.views import (home_view, employer_signup, employee_signup, user_login, user_logout,
                          employee_home, employer_home, mail_details, delete_mail_details, send_email, sent_emails)


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', user_login, name='login'),
    path('signup/employee/', employee_signup, name='employee_signup'),
    path('signup/employer/', employer_signup, name='employer_signup'),
    path('employee_home/', employee_home, name='employee_home'),
    path('employer_home/', employer_home, name='employer_home'),
    path('employer/mail_details/', mail_details, name='mail_details'),
    path('employer/delete_mail_details/', delete_mail_details, name='delete_mail_details'),
    path('employee/send-email/', send_email, name='send_email'),
    path('employee/sent-emails/', sent_emails, name='sent_emails'),
    path('logout/', user_logout, name='logout'),
]
