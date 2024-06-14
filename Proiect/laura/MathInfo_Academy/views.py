from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from graph.Graph import Graph, NodeDetails
from django.http import Http404


from MathInfo_Academy.models import User, Materials, Students_Activity, Subject, Teacher_Activity
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

from django.core.files.storage import default_storage




def home(request):
    return render(request, 'home.html', {}) 


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    

def user_logout(request):
    if not request.user.is_authenticated:
            return redirect('/login')
    auth.logout(request)
    return redirect('/')



def register(request):
    print("register", request.POST)
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)        
        if form.is_valid():
            form.save()            
            return redirect('login')
    else:
        form = RegistrationForm()
        
    return render(request, 'register.html', {'form': form})
 




@login_required
def activity(request):
    if request.method != 'GET':
        return redirect('/')
   
    if request.user.is_student:
        student_activities = list(Students_Activity.objects.filter(student=request.user))
        info_dict = {}
        teachers_names = {}
        for student_activity in student_activities:
            teacher_activity = student_activity.teacher_activity
            course_name = teacher_activity.course.name
            activity_type = teacher_activity.activity_type
            teacher_name = teacher_activity.teacher.first_name + " " + teacher_activity.teacher.last_name
 
            if course_name not in info_dict:
                info_dict[course_name] = {}
                teachers_names[course_name] = {}
 
            if activity_type not in info_dict[course_name]:
                info_dict[course_name][activity_type] = []
                teachers_names[course_name][activity_type] = teacher_name
 
            materials = Materials.objects.filter(teacher_activity=teacher_activity)
            for material in materials:
                info_dict[course_name][activity_type].append({
                    'url': material.documentation.url,
                    'name': material.documentation.name.split('/')[-1]
                })
               
 
        return render(request, 'activity.html', {'info_dict': info_dict, "teachers_names": teachers_names})
       
    else:
        teacher_activities = list(Teacher_Activity.objects.filter(teacher=request.user))
        info_dict = {}
        teach_act_dict = {}
        for teacher_activity in teacher_activities:
            course_name = teacher_activity.course.name
            activity_type = teacher_activity.activity_type
 
            if course_name not in info_dict:
                info_dict[course_name] = {}
                teach_act_dict[course_name] = {}
 
            if activity_type not in info_dict[course_name]:
                info_dict[course_name][activity_type] = []
                teach_act_dict[course_name][activity_type] = teacher_activity
 
            materials = Materials.objects.filter(teacher_activity=teacher_activity)
            for material in materials:
                info_dict[course_name][activity_type].append({
                    'url': material.documentation.url,
                    'name': material.documentation.name.split('/')[-1],
                    'id': material.id
                })
 
        return render(request, 'activity.html', {'info_dict': info_dict, 'teach_act_dict': teach_act_dict})


def upload_material(request, course_name, activity_type):
    if request.method == 'POST' and request.user.is_teacher:
        teacher = request.user  
        course = Subject.objects.get(name=course_name)
        teacher_activity = Teacher_Activity.objects.get(teacher=teacher, course=course, activity_type=activity_type)
        if 'documentation' not in request.FILES:
            messages.error(request, 'No file selected for upload!')
            return redirect('/activity')
        documentation = request.FILES['documentation']
        if documentation.name.split('.')[-1] != 'pdf':
            messages.error(request, 'Invalid file format! Please, upload a pdf file!')
            return redirect('/activity')
        form = Materials(teacher_activity=teacher_activity, documentation=request.FILES['documentation'])
        form.save()
        messages.success(request, 'Material uploaded successfully!')
        return redirect('/activity')
    else:
        return redirect('/')



def delete_material(request, material_id):
    material = Materials.objects.get(id=material_id)

    try:
        material = Materials.objects.get(id=material_id)
    except Materials.DoesNotExist:
        messages.error("Material not found!")


    if request.user.is_teacher:
        if default_storage.exists(material.documentation.name):
            default_storage.delete(material.documentation.name)
        material.delete()

        messages.success(request, 'Material deleted successfully!')

        return redirect('/activity')
    
    else:
        return redirect('/')

    

def directions(request):
    graph = Graph()
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


@login_required
def grades(request):
    if request.method != 'GET':
        return redirect('/')
    
    if request.user.is_student:
        student_activities = list(Students_Activity.objects.filter(student=request.user))
        info_dict = {}
        credits = {}
        course_grades = {}
        for student_activity in student_activities:
            teacher_activity = student_activity.teacher_activity
            course_name = teacher_activity.course.name
            activity_type = teacher_activity.activity_type
            credits[course_name] = teacher_activity.course.credits

            if course_name not in info_dict:
                info_dict[course_name] = {}
                course_grades[course_name] = [0, 0]

            info_dict[course_name][activity_type] = {
                "grade": student_activity.grade,
                "max_grade": teacher_activity.max_grade,
            }
            
            course_grades[course_name][0] += student_activity.grade
            course_grades[course_name][1] += teacher_activity.max_grade
            
        for course in course_grades:
            course_grades[course][0] = course_grades[course][0] / course_grades[course][1] * 10
            course_grades[course][1] = 10.0

        return render(request, 'grades.html', {'info_dict': info_dict, 'credits': credits, 'course_grades': course_grades})

    else:
        teacher_activities = list(Teacher_Activity.objects.filter(teacher=request.user))
        info_dict = {}
        max_grades = {}
        teach_act_ids = {}
        for teacher_activity in teacher_activities:
            course_name = teacher_activity.course.name
            activity_type = teacher_activity.activity_type

            if course_name not in info_dict:
                info_dict[course_name] = {}
                max_grades[course_name] = {}
                teach_act_ids[course_name] = {}

            if activity_type not in info_dict[course_name]:
                info_dict[course_name][activity_type] = []
                max_grades[course_name][activity_type] = teacher_activity.max_grade
                teach_act_ids[course_name][activity_type] = teacher_activity.id

            students_activities = list(Students_Activity.objects.filter(teacher_activity=teacher_activity))
            for student_activity in students_activities:
                info_dict[course_name][activity_type].append([student_activity.id, student_activity.student.first_name, student_activity.student.last_name, student_activity.grade])

        return render(request, 'grades.html', {'info_dict': info_dict, 'max_grades': max_grades, 'teach_act_ids': teach_act_ids})


@login_required
def grade_student(request, student_activity_id):
    if request.method == 'POST' and request.user.is_teacher:
        student_activity = Students_Activity.objects.get(id=student_activity_id)
        student = student_activity.student
        teacher_activity = student_activity.teacher_activity
        grade = request.POST['new_grade']
        if grade == '':
            messages.error(request, 'Please, enter a grade!')
            return redirect('/grades')
        try:
            grade = float(grade)
        except ValueError:
            messages.error(request, 'Invalid grade! Please, enter a number!')
            return redirect('/grades')
       
        if grade < 0 or grade > teacher_activity.max_grade:
            messages.error(request, 'Invalid grade! Please, enter a grade between 0 and the maximum grade!')
            return redirect('/grades')
        
        student_activity.grade = grade
        student_activity.save()
        messages.success(request, 'Grade updated successfully!')
        return redirect('/grades')
    
    else:
        return redirect('/grades')


@login_required
def modify_max_grade(request, teacher_activity_id):
    if request.method == 'POST' and request.user.is_teacher:
        new_max_grade = request.POST['new_max_grade']
        if new_max_grade == '':
            messages.error(request, 'Please, enter a grade!')
            return redirect('/grades')
        try:
            grade = float(new_max_grade)
        except ValueError:
            messages.error(request, 'Invalid grade! Please, enter a number!')
            return redirect('/grades')
        
        if grade < 0:
            messages.error(request, 'Invalid grade! Please, enter a positive number!')
            return redirect('/grades')
        teacher_activity = Teacher_Activity.objects.get(id=teacher_activity_id)
        teacher_activity.max_grade = new_max_grade
        teacher_activity.save()
        messages.success(request, 'Max grade updated successfully!')
    return redirect('/grades')


