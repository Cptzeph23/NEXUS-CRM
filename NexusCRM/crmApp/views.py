from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'dashboard.html')


def module_placeholder(request, module_name):
    return render(request, "placeholder.html",
        {
            "module_name": module_name,
        }
    )
