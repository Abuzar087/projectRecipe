from django.shortcuts import render,redirect
from .models import Recipe
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .form import Registrationform
from django.contrib.auth.decorators import login_required
# Create your views here.


def recipies(request):
    if request.method=="POST" and request.user.is_authenticated:
        data=request.POST
        recipe_image=request.FILES.get('recipe_image')
        recipe_name=data.get('recipe_name')
        recipe_desc=data.get('recipe_desc')
        Recipe.objects.create(recipe_name=recipe_name,
                              recipe_desc=recipe_desc,
                              recipe_image=recipe_image)
    queryset=Recipe.objects.all()

    if request.GET.get('search'):
        queryset=queryset.filter(recipe_name__icontains=request.GET.get('search'))
    context={'recipes':queryset} 

    return render(request,'recip.html',context)


@login_required
def delete_recipe(request,id):
    rec=Recipe.objects.get(id=id)
    rec.delete()
    return redirect('/recipe/')
@login_required
def update_recipe(request,id):
    data=request.POST
    rec=Recipe.objects.get(id=id)
    if request.method=="POST":
        recipe_name=data.get('recipe_name')
        recipe_desc=data.get('recipe_desc')
        recipe_image=request.FILES.get('recipe_image')
        rec.recipe_name=recipe_name
        rec.recipe_desc=recipe_desc
        if recipe_image:
         rec.recipe_image=recipe_image
        rec.save()
        messages.add_message(request,messages.SUCCESS,"Successfuly Update!!")

    return render(request,'update.html',{'recp':rec})

######################
def register(request):
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('login')  # Redirect to your recipes page
        else:
            # Display form errors
            messages.error(request, 'Please correct the errors below.')
            print(form.data)
            print(form.errors)
            print(form.cleaned_data)
    else:
        form = Registrationform()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('recipe')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


#
def user_logout(request):
    logout(request)  # This function logs out the user by clearing the session data
    return redirect('login') 