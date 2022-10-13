import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import student, course, staff
from django.contrib.auth.decorators import login_required


# Create your views here.
def showHome(request):
    return render(request, 'home.html')


@login_required(login_url='userLogin')
def adminHome(request):
    return render(request, 'adminTemplates/adminHome.html')


@login_required(login_url='userLogin')
def staffHome(request):
    return render(request, 'staff/staffHome.html')


def addCourse_page(request):
    return render(request, 'adminTemplates/addCourse.html')


def RegisterStaff_page(request):
    return render(request, 'RegisterStaff.html')


def addStudent_page(request):
    courses = course.objects.all()
    return render(request, 'adminTemplates/addStudent.html', {'courselist': courses})


def showStudents(request):
    studs = student.objects.all()
    return render(request, 'adminTemplates/students.html', {'std': studs})


def deleteStudent(request, pk):
    stud = student.objects.get(id=pk)
    stud.delete()
    messages.info(request, f'{stud.std_name} deleted')
    return redirect('showStudents')


def editStudents_page(request, pk):
    studs = student.objects.get(id=pk)
    courses = course.objects.all()
    return render(request, 'adminTemplates/studentEdit.html', {'std': studs, 'c': courses})

@login_required(login_url='userLogin')
def addStudent(request):
    if request.method == 'POST':
        cid = request.POST['scourse']
        name = request.POST['sname']
        addr = request.POST['saddr']
        age = request.POST['sage']
        jd = request.POST['sjdate']

        course1 = course.objects.get(id=cid)

        std = student(
            std_course=course1,
            std_name=name,
            std_address=addr,
            std_age=age,
            std_joindate=jd
        )
        std.save()
        messages.success(request, f'Successfully Registered {name}')
        return redirect('addStudent_page')


def editStudent(request, pk):
    if request.method == 'POST':
        std = student.objects.get(id=pk)
        std.std_name = request.POST.get('sname')
        std.std_address = request.POST.get('saddr')
        std.std_age = request.POST.get('sage')
        std.std_joindate = request.POST.get('sjdate')
        cid = request.POST.get('scourse')
        course1 = course.objects.get(id=cid)
        std.std_course = course1
        std.save()
        messages.success(request, f'Successfully updated the details of{std.std_name}')
        return redirect('showStudents')


def addCourse(request):
    if request.method == 'POST':
        name = request.POST['cname']
        fee = request.POST['cfee']
        crs = course(course_name=name, course_fee=fee)
        crs.save()
        messages.success(request, 'course details saved successfully')
        return redirect('addCourse_page')


def showStaff(request):
    staffs = staff.objects.all()
    return render(request, 'adminTemplates/staffdetails.html', {'stf': staffs})


def deleteStaff(request, pk):
    staff1 = staff.objects.get(id=pk)
    user1 = User.objects.get(id=staff1.st_user.id)
    staff1.delete()
    user1.delete()
    return redirect('showStaff')


def registerStaff(request):
    if request.method == 'POST':
        fname = request.POST['s_fname']
        lname = request.POST['s_lname']
        addr = request.POST['s_addr']
        emailid = request.POST['s_email']
        uname = request.POST['s_uname']
        pswd = request.POST['s_pwd']
        rpswd = request.POST['r_pwd']
        gender = request.POST['s_gender']
        phno = request.POST['s_phone']
        if request.FILES.get('s_image') is not None:
            img = request.FILES['s_image']
        else:
            img = "/static/images/default.jpg"
        if pswd == rpswd:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'This username already exist')
                return redirect('RegisterStaff_page')
            else:
                user = User.objects.create_user(
                    first_name=fname,
                    last_name=lname,
                    username=uname,
                    password=pswd,
                    email=emailid)
                user.save()
                u = User.objects.get(id=user.id)
                stf = staff(
                    st_user=u,
                    st_address=addr,
                    st_gender=gender,
                    st_phone=phno,
                    st_photo=img
                )
                stf.save()
                messages.success(request, f'Successfully Registered {fname}')
                return redirect('showHome')
        else:
            messages.error(request, "Password missmatch")
            return redirect('RegisterStaff_page')
    else:
        return render(request, 'home.html')


def userLogin(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['upwd']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                # messages.info(request, f'Welcome {username}')
                return redirect('adminHome')
            else:
                auth.login(request, user)
                messages.info(request, f' {username}')
                return redirect('staffHome')
        else:
            messages.info(request, 'Invalid Username or Password. Try Again.')
            return redirect('showHome')
    else:
        messages.info(request, 'Oops,please log in !!!!!!!!! .')
        return redirect('showHome')


@login_required(login_url='userLogin')
def userLogout(request):
    auth.logout(request)
    return redirect('showHome')


# STAFF OPERATIONS
def studentsList(request):
    studs = student.objects.all()
    return render(request, 'staff/studentlist.html', {'std': studs})


def viewStaffcard(request):
    currentUser = staff.objects.filter(st_user=request.user)
    return render(request, 'staff/staffCard.html', {'curuser': currentUser})


def profileEditpage(request):
    currentUser = staff.objects.filter(st_user=request.user)
    return render(request, 'staff/profileEdit.html', {'staffs': currentUser})


def editProfile(request, pk):
    if request.method == 'POST':
        user1 = request.user
        user1.first_name = request.POST.get('s_fname')
        user1.last_name = request.POST.get('s_lname')
        user1.email = request.POST.get('s_email')
        user1.username = request.POST.get('s_uname')
        user1.save()
        staff1 = staff.objects.get(id=pk)
        if request.FILES.get('s_image') is not None:
            if not staff1.st_photo == "/static/images/default.jpg":
                os.remove(staff1.st_photo.path)
                staff1.st_photo = request.FILES['s_image']
            else:
                staff1.st_photo = request.FILES['s_image']

        # staff1.st_user.first_name=request.POST.get('s_fname')
        # staff1.st_user.last_name=request.POST.get('s_lname')
        # staff1.st_user.email=request.POST.get('s_email')
        # staff1.st_user.username=request.POST.get('s_uname')
        staff1.st_user = user1
        staff1.st_address = request.POST.get('s_addr')
        staff1.st_gender = request.POST.get('s_gender')
        staff1.st_phone = request.POST.get('s_phone')
        staff1.save()
        print("EDITED")
        return redirect('viewStaffcard')



