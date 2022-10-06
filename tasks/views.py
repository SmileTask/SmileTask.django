from turtle import title
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import tareas
from django.utils import timezone
# Create your views here.
def home(request):
    return render(request, 'home.html')

# inicio de sesion de usuarios
def loginuser(request):
    if request.user.is_authenticated:
        return redirect('/dashboardtask/')
    else:    
        if request.method == 'GET':
            return render(request, 'login.html')
        else:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'subTemplate/loginError/loginE.html')
            else:
                login(request, user)
                return redirect('/dashboardtask/')

# registro de usuarios nuevos a la plataforma
def registeruser(request):
    if request.user.is_authenticated:
        return redirect('/dashboardtask/')
    else:
        if request.method == 'GET':
            return render(request, 'register.html')
        else:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                    user.first_name = request.POST['fisrtname']
                    user.last_name = request.POST['lastname']
                    user.email = request.POST['email']
                    user.save()
                    login(request, user)
                    return redirect('/dashboardtask/')
                except:
                    return render(request, 'subTemplate/registerError/registerE.html')
            return render(request, 'subTemplate/registerError/registerP.html')

# vista de la dashboar
def dashboardtask(request):
    if request.user.is_authenticated:
        task = tareas.objects.filter( user = request.user, datacompleted__isnull=True )
        return render(request ,'dashboard.html', {
            'nombre': request.user.get_full_name(),
            'task': task
        })
    else:
        return redirect('/')

# vista de creacion de tareas en la dashboard
def createtask(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'subTemplate/subDash/createTask.html')
        else:
            if request.POST['importantInput'].lower() == 'si':
                important = True
            elif request.POST['importantInput'].lower() == 'no':
                important = False
            else:
                return render(request, 'subTemplate/subDash/createTaskE.html')
            title = request.POST['title']
            time = request.POST['time']
            description = request.POST['description']
            user = request.user
            tarea = tareas.objects.create(title=title, ejecution=time, description=description, important=important, user=user)
            return render(request, 'subTemplate/subDash/createTask.html')
    else:
        return redirect('/')

# vista para actualizar tareas
def updatetask(request, task__id):
    if request.user.is_authenticated:
        task = get_object_or_404(tareas , pk=task__id)
        if request.method == 'GET':
            return render(request, 'subTemplate/subDash/updateTask.html', {'task':task})
        else:
            if request.POST['importantInput'].lower() == 'si':
                important = True
            elif request.POST['importantInput'].lower() == 'no':
                important = False
            else:
                return render(request, 'subTemplate/subDash/updateTaskE.html', {'task':task})
            title = request.POST['title']
            time = request.POST['time']
            description = request.POST['description']
            task.title = title
            task.description = description
            task.ejecution = time
            task.important = important
            task.save()
            return redirect('/dashboardtask/')
    else:
        return redirect('/')


# vista para terminar las tareas
def taskterminated(request, task__id):
    if request.user.is_authenticated:
        task = get_object_or_404(tareas ,pk=task__id, user=request.user)
        task.datacompleted = timezone.now()
        task.save()
        return redirect('/dashboardtask/')
    else:
        return redirect('/')


# vista template tareas terminadas
def deletetask(request):
    if request.user.is_authenticated:
        task = tareas.objects.filter( user = request.user, datacompleted__isnull=False )
        return render(request, 'subTemplate/subDash/terminated.html', {'task':task})
    else:
        return redirect('/')

# vista para eliminar la tarea

def deletetaskid(request, task__id):
    if request.user.is_authenticated:
        task = get_object_or_404(tareas ,pk=task__id, user=request.user)
        task.delete()
        return redirect('/dashboardtask/terminate/')
    else:
        return redirect('/')

# cerrar la sesion de los usuarios
def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')