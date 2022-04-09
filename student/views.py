from authentication.models import *
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserChangeForm
from chairman.models import Course, Running_Semester, Roll_Sheet, Teacher_Student_Info


def student_profile(request):
    if request.user.is_authenticated:
        student = Student.objects.get(email= request.user)
        res = Student.objects.filter(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            return render(request, 'student/profile.html', {'student': student})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

#logout
def student_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')


def student_password_reset(request):
    if request.user.is_authenticated:
        res = Student.objects.filter(email= request.user)
        student = Student.objects.get(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            fm = PasswordChangeForm(request.user)
            if request.method == 'POST':
                fm = PasswordChangeForm(user = request.user, data = request.POST)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Password change successfully...')
                    update_session_auth_hash(request, fm.user)
                    return HttpResponseRedirect('/student/profile/')
            else:
                fm = PasswordChangeForm(request.user)
            return render(request, 'student/pswreset1.html', {'form': fm, 'student': student})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/') 

def student_password_reset2(request):
    if request.user.is_authenticated:
        student = Student.objects.get(email= request.user)
        res = Student.objects.filter(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            if request.method == 'POST':
                fm = SetPasswordForm(user= request.user, data= request.POST)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Password change successfully...')
                    update_session_auth_hash(request, fm.user)
                    return HttpResponseRedirect('/student/profile/')
            else:
                fm = SetPasswordForm(request.user)
            return render(request, 'student/pswreset2.html', {'form': fm, 'student': student})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

def current_courses(request):
    if request.user.is_authenticated:
        student = Student.objects.get(email= request.user)
        k = student.session
        running_semester = Running_Semester.objects.filter(session= k)
        for r in running_semester:
            semester = r.semester_no
        courses = Course.objects.filter(semister_no = semester)
        return render(request, 'student/current_courses.html', {'courses': courses, 'student':student})
    else:
        return HttpResponseRedirect('/')

def complete_courses(request):
    student = Student.objects.get(email= request.user)
    k = student.session
    running_semester = Running_Semester.objects.filter(session= k)
    for r in running_semester:
        semester = r.semester_no
    if semester == '4th Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester)
    if semester == '4th Year 1st Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester')
    if semester == '3rd Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester')
    if semester == '3rd Year 1st Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester')
    if semester == '2nd Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester')
    if semester == '2nd Year 1st Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester').exclude(semister_no= '2nd Year 2nd Semester')
    if semester == '1st Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester').exclude(semister_no= '2nd Year 1st Semester')
    if semester == '1st Year 1st Semester':
        courses = Course.objects.all()
    return render(request, 'student/complete_courses.html', {'courses': courses, 'student':student})

def course_registration(request):
    student = Student.objects.get(email= request.user)
    session= student.session
    semester = Running_Semester.objects.get(session = session)
    sem = semester.semester_no
    courses = Course.objects.filter(semister_no = sem)
    course_code = []
    backlog_course_code = []
    if request.method == 'POST':

        #handle backlog course
        back_log_credit = 0
        bl1 = request.POST.get('backLog1')
        if bl1:
            check_bl1_course = Course.objects.filter(course_code = bl1)
            flag = False
            for course in check_bl1_course:
                flag = True
                back_log_credit += course.credit
            if flag == True:
                backlog_course_code.append(bl1)
            else:
                messages.warning(request, 'is not a valid course code', {bl1})
                return HttpResponseRedirect('/student/course_registration/')

        bl2 = request.POST.get('backLog2')
        if bl2:
            check_bl2_course = Course.objects.filter(course_code = bl2)
            flag = False
            for course in check_bl2_course:
                flag = True
                back_log_credit += course.credit
            if flag == True:
                backlog_course_code.append(bl2)
            else:
                messages.warning(request, 'is not a valid course code', {bl2})
                return HttpResponseRedirect('/student/course_registration/')

        bl3 = request.POST.get('backLog3')
        if bl3:
            check_bl3_course = Course.objects.filter(course_code = bl3)
            flag = False
            for course in check_bl3_course:
                flag = True
                back_log_credit += course.credit
            if flag == True:
                backlog_course_code.append(bl3)
            else:
                messages.warning(request, 'is not a valid course code', {bl3})
                return HttpResponseRedirect('/student/course_registration/')

        bl4 = request.POST.get('backLog4')
        if bl4:
            check_bl4_course = Course.objects.filter(course_code = bl4)
            flag = False
            for course in check_bl4_course:
                flag = True
                back_log_credit += course.credit
            if flag == True:
                backlog_course_code.append(bl4)
            else:
                messages.warning(request, 'is not a valid course code', {bl4})
                return HttpResponseRedirect('/student/course_registration/')
        
        bl5 = request.POST.get('backLog5')
        if bl5:
            check_bl5_course = Course.objects.filter(course_code = bl5)
            flag = False
            for course in check_bl5_course:
                flag = True
                back_log_credit += course.credit
            if flag == True:
                backlog_course_code.append(bl5)
            else:
                messages.warning(request, 'is not a valid course code', {bl5})
                return HttpResponseRedirect('/student/course_registration/')
        
        bl6 = request.POST.get('backLog6')
        if bl6:
            check_bl6_course = Course.objects.filter(course_code = bl6)
            flag = False
            for course in check_bl6_course:
                flag = True
                back_log_credit += course.credit
            if flag == True:
                backlog_course_code.append(bl6)
            else:
                messages.warning(request, 'is not a valid course code', {bl6})
                return HttpResponseRedirect('/student/course_registration/')

        
        #credit count
        total_credit = 0
        for course in courses:
            total_credit += course.credit
        total_credit += back_log_credit

        if total_credit > 30:
            messages.info(request, 'Total course credit can not more than 30')
            return HttpResponseRedirect('/student/course_registration/')







        session = student.session
        student_id = student.student_id
        name_of_student = student.first_name + " " + student.last_name
        hall = student.hall
        remarks = 'Regular'

        #regular course add to teacher
        for course in courses:
            course_code.append((course.course_code))
            c_code = course.course_code
            current_course = Course.objects.get(course_code = c_code)
            teacher = (current_course.course_teacher)
            credit = current_course.credit
            semister_no = current_course.semister_no
            course_name = current_course.course_name
            data = Teacher_Student_Info(
                student_name = name_of_student,
                student_id = student_id,
                course_name = course_name,
                course_code = c_code,
                teacher = teacher,
                hall = hall,
                session = session,
                credit = credit,
                remarks= 'Regular',
                semester = semister_no,
            )
            check_teacher_stu = Teacher_Student_Info.objects.filter(student_name= name_of_student, course_code = c_code, teacher = teacher)
            flag = False
            for check in check_teacher_stu:
                flag = True
            if flag == True:
                messages.warning(request, 'You are already registered these courses!!!')
                return HttpResponseRedirect('/student/course_registration/')
                break;
            else:
                data.save()
                messages.success(request, 'course added successfully to the teacher')

        
        #backlog course information add to teacher
        for backLogCourseCode in backlog_course_code:
            course_code.append(backLogCourseCode)
            c_code = backLogCourseCode
            current_course = Course.objects.get(course_code = c_code)
            teacher = current_course.course_teacher
            credit = current_course.credit
            semister_no = current_course.semister_no
            course_name = current_course.course_name
            remarks = 'BackLog'
            data = Teacher_Student_Info(
                student_name = name_of_student,
                student_id = student_id,
                course_name = course_name,
                course_code = c_code,
                teacher = teacher,
                hall = hall,
                session = session,
                credit = credit,
                remarks= remarks,
                semester = semister_no,
            )
            check_teacher_stu = Teacher_Student_Info.objects.filter(student_name= name_of_student, course_code = c_code, teacher = teacher)
            flag = False
            for check in check_teacher_stu:
                flag = True
            if flag == True:
                messages.warning(request, 'You are already registered these courses!!!')
                return HttpResponseRedirect('/student/course_registration/')
            else:
                data.save()
                #messages.success(request, 'course added successfully to the teacher')


        check = Roll_Sheet.objects.filter(student_id= student_id)
        flag = False
        for c in check:
            flag = True
        if flag == True:
            messages.warning(request, 'You are already registered in this semester!!!')
        else:
            data = Roll_Sheet(session= session, student_id= student_id, name_of_student= name_of_student, hall= hall, course_code= course_code, remarks= remarks, semester=semister_no)
            messages.success(request, 'Your Registration is successfull!!!')
            data.save()
    return render(request, 'student/course_registration.html',{'student':student, 'sem': sem, 'courses': courses})

