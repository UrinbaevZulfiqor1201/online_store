from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
User = get_user_model()


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                user.save()
                return redirect('login')  # Ro'yxatdan o'tgandan so'ng foydalanuvchini boshqa sahifaga yo'naltirish
            else:
                return render(request, 'app_users/register.html', {'error': 'Email already registered'})
        else:
            return render(request, 'app_users/register.html', {'error': 'Passwords do not match'})

    return render(request, 'app_users/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'app_users/login.html', {'error': 'Email or password is incorrect'})

    return render(request, 'app_users/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'app_users/logout.html')






