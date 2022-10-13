from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.showHome,name='showHome'),
    path('userLogin',views.userLogin,name='userLogin'),
    path('userLogout',views.userLogout,name='userLogout'),
    path('adminHome',views.adminHome,name='adminHome'),
    path('staffHome',views.staffHome,name='staffHome'),
    path('RegisterStaff_page',views.RegisterStaff_page,name='RegisterStaff_page'),
    path('registerStaff',views.registerStaff,name='registerStaff'),
    path('showStaff',views.showStaff,name='showStaff'),
    path('deleteStaff/<int:pk>',views.deleteStaff,name='deleteStaff'),
    path('addCourse_page',views.addCourse_page,name='addCourse_page'),
    path('addCourse',views.addCourse,name='addCourse'),
    path('addStudent_page',views.addStudent_page,name='addStudent_page'),
    path('addStudent',views.addStudent,name='addStudent'),
    path('showStudents',views.showStudents,name='showStudents'),
    path('deleteStudent/<int:pk>',views.deleteStudent,name='deleteStudent'),
    path('editStudents_page/<int:pk>',views.editStudents_page,name='editStudents_page'),
    path('editStudent/<int:pk>',views.editStudent,name='editStudent'),
    path('studentsList',views.studentsList,name='studentsList'),
    path('viewStaffcard',views.viewStaffcard,name='viewStaffcard'),
    path('profileEditpage',views.profileEditpage,name="profileEditpage"),
    path('editProfile/<int:pk>',views.editProfile,name='editProfile'),
]