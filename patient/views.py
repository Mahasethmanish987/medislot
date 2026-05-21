from django.shortcuts import render

def patient_dashboard(request):
    return render(request, "patient/patient_dashboard.html")