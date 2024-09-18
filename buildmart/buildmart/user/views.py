from django.shortcuts import render,redirect
from .forms import UserRegistationForm




# Create your views here.
def register_user(request):
   
    if request.method == "POST":
        form = UserRegistationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ("register_user")


    else:
        form = UserRegistationForm()
    return render(request,"user/register_user.html", {"form":form})

