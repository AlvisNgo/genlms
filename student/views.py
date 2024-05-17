from django.shortcuts import render, redirect

# Create your views here.
def root(request):
    return redirect('/student/dashboard')

def dashboard(request):
    return render(request, 'dashboard.html')