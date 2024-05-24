from django.shortcuts import render
# from .forms import TestForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from graph.Graph import Graph, NodeDetails


# Create your views here.
def home(request):
    return render(request, 'home.html', {}) # {} is an empty dictionary


# def test(request):
#     if request.method == 'POST':
#         form = TestForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return render(request, 'success.html')
#         print(form.errors)
#         return render(request, 'test.html', {'form': form})
#     else:
#         context = {'form': TestForm()}
#         return render(request, 'test.html', context)

def user_logout(request):    
    auth.logout(request)
    return redirect('/')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def user_logout(request):
    auth.logout(request)
    return redirect('/')

def directions(request):
    graph = Graph()
    print("HERE:", -1 in graph.info)
    directions = []
    error = ""
    start = None
    finish = None
    if request.method == 'POST':
        start = request.POST['start']
        finish = request.POST['finish']
        try :
            start = int(start)
            finish = int(finish)

            if start not in graph.info or finish not in graph.info:
                error = "Invalid or no room selected! Please, select a valid one!"
            else:
                directions = graph.get_directions(start, finish)

        except ValueError:
            error = "Invalid input"

    def process_node(node: int, graph: Graph):
        if node == None:
            return None
        if node not in graph.info:
            return None
        node = graph.info[node]
        if node.no_room == '0' or (node.details is not None and ("Terrace" in node.details or "Toilet" in node.details)):
            return node.details
        elif node.no_room != '0' and (node.details is not None and "Terrace" not in node.details and "Toilet" not in node.details):
            return f'Room {node.no_room} ({node.details})'
        else:
            return f'Room {node.no_room}'

    rooms = graph.get_rooms_info()
    sorted_rooms = sorted(rooms, key=lambda x: (len(x.no_room), x.no_room))
    return render(request, 'directions.html', {
        "rooms": sorted_rooms, 
        "directions": directions, 
        'error': error, 
        "start": process_node(start, graph), 
        "finish": process_node(finish, graph)
        })





# view pentru pagina cu directii care la GET trimite pagina doar cu informatiile 
# despre noduri
# la POST trimite si indicatiile de orientare