from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category
from .forms import TaskForm, CategoryForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

# Register View
def registers(request):
    if request.method == "POST":
        name = request.POST['register-name']
        email = request.POST['register-email']
        password = request.POST['register-password']
        confirm_password = request.POST['register-confirm-password']
        
        if password != confirm_password:
            return HttpResponse("Passwords do not match") 
        
        if User.objects.filter(username=name).exists():
            messages.error(request, "A user with this username already exists.")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect('register')
        
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')
    
    return render(request, 'register.html')

# Login View
def logins(request):
    if request.method == "POST":
        login_name = request.POST['login-name']
        login_password = request.POST['login-password']
        
        user = authenticate(request, username=login_name, password=login_password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    
    return render(request, "login.html")

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Index View (Shows tasks only for the logged-in user)
def index(request):
    tasks = Task.objects.filter(user=request.user).order_by('-priority', 'due_date') if request.user.is_authenticated else []
    categories = Category.objects.all()
    form = TaskForm()

    search_query = request.GET.get('search', '')
    priority_filter = request.GET.get('priority', '')
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')

    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'pending':
        tasks = tasks.filter(completed=False)

    if category_filter:
        tasks = tasks.filter(category__name=category_filter)

    # If the user is not authenticated, show a general index page (without tasks)
    return render(request, 'index.html', {'tasks': tasks, 'form': form, 'categories': categories})

# Add Task View
def add_task(request):
    print(f"User authenticated: {request.user.is_authenticated}")  # Debugging
    if not request.user.is_authenticated:
        messages.error(request, "Login required! Please log in to add a task.")
        return redirect('login')
    
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            
            # Set default category to "Personal" if not selected
            if not task.category:
                personal_category, created = Category.objects.get_or_create(name="Personal")
                task.category = personal_category  # Set "Personal" category
                
            task.user = request.user  # Associate task with the logged-in user
            task.save()
            
    return redirect('index')  # Redirect to homepage after task is added

# Delete Task View
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Only allow deletion if task belongs to the user
    task.delete()
    return redirect('index')

# Complete Task View
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Only allow completion if task belongs to the user
    task.completed = not task.completed
    task.save()
    return redirect('index')

# Edit Task View (Fix Duplicate edit_task and ensure user ownership)
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Only allow editing if task belongs to the user
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        category_id = request.POST.get('category')

        category = get_object_or_404(Category, id=category_id)

        # Update task
        task.title = title
        task.description = description
        task.due_date = due_date
        task.priority = priority
        task.category = category
        task.save()

        return redirect('index')  # Redirect to task list after editing

    return render(request, 'edit_task.html', {'task': task, 'categories': categories})

def intro(request):
    return render(request,"intro.html")