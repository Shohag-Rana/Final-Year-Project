from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from authentication.models import *
from chairman.models import Course, Teacher_Student_Info
from . models import Attendence_and_CT_Mark, Theory_Marks
# Create your views here.
def faculty_profile(request):
    if request.user.is_authenticated:
        res = Teacher.objects.filter(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            return render(request, 'faculty/profile.html', {'faculty': res})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

def faculty_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')

def faculty_pswreset(request):
    if request.user.is_authenticated:
        res = Teacher.objects.filter(email= request.user)
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
                    return HttpResponseRedirect('/faculty/profile/')
            else:
                fm = PasswordChangeForm(request.user)
            return render(request, 'faculty/pswreset1.html', {'form': fm, 'faculty': res})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/') 

def faculty_pswreset2(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            res = Teacher.objects.filter(email= request.user)
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
                        return HttpResponseRedirect('/faculty/profile/')
                else:
                    fm = SetPasswordForm(request.user)
                return render(request, 'faculty/pswreset2.html', {'form': fm, 'faculty': res})
            else:
                return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

def current_course(request):
    if request.user.is_authenticated:
        all_semesters = ['1st Year 1st Semester', '1st Year 2nd Semester',
                        '2nd Year 1st Semester', '2nd Year 2nd Semester', '3rd Year 1st Semester',
                        '3rd Year 2nd Semester', '4th Year 1st Semester', '4th Year 2nd Semester']
        user = request.user
        faculty = Teacher.objects.filter(email= request.user)
        courses = Course.objects.filter(course_teacher = user)
        all_semester_list = []
        for semester in all_semesters:
            c_list = []
            flag = False
            for course in courses:
                if semester == course.semister_no:
                    c_list.append(course.course_code)
                    flag = True
            if flag == True:
                all_semester_list.append(semester)
        context = {
            'courses': courses, 
            'faculty': faculty, 
            'all_semesters': all_semester_list,
            }
        return render(request, 'faculty/current_course.html', context)
    else:
        return HttpResponseRedirect('/')

def course_details(request, course_code):
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Special').order_by('student_id')
    course = Course.objects.get(course_code= course_code)
    c_code = (course.course_code)
    c_name = (course.course_name)
    c_credit = (course.credit)
    c_teacher = course.course_teacher
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    for stu in backLog_students:
        count += 1
        backLogStudents[stu] = count
    context = {
        'c_code': c_code,
        'c_name': c_name,
        'c_credit': c_credit,
        'regular_students': regular_students,
        'c_teacher': c_teacher,
        'backLogStudents': backLogStudents,
        'special_students': special_students,
    }
    return render(request, 'faculty/course_details.html', context)

def attendence_sheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    for stu in backLog_students:
        count += 1
        backLogStudents[stu] = count
    print(backLogStudents)
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_students': regular_students,
        'backLogStudents': backLogStudents,
        'special_students': special_students,
    }
    return render(request, 'faculty/attendence_sheet.html', context)

def ct_and_attendence_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks= 'Regular').order_by('student_id')
    ct_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code)
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    for stu in backLog_students:
        count += 1
        backLogStudents[stu] = count
    for check in ct_attend_marks:
        return HttpResponseRedirect(f'/faculty/edit_ct_and_attendence_mark/{course_code}/') 
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_students': regular_students,
        'ct_attend_marks': ct_attend_marks,
        'backLogStudents': backLogStudents,
        'special_students': special_students,
        }
    if request.method == 'POST':
        course = Course.objects.get(course_code= course_code)
        students = Teacher_Student_Info.objects.filter(course_code= course_code)
        ct_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code)
        context = {
            'semister_no': course.semister_no,
            'c_code': course_code,
            'c_teacher': course.course_teacher,
            'credit': course.credit,
            'c_name': course.course_name,
            'students': students,
            'ct_attend_marks': ct_attend_marks,
            }
        for student in students:
            ct_marks = request.POST.get(f'{student.student_id}')
            attend_marks = request.POST.get(f'{student.student_name}')
            if ct_marks and attend_marks:
                ct_marks = (float(ct_marks))
                attend_marks = (float(attend_marks))
                if ct_marks > 20 or attend_marks > 10:
                    messages.warning(request, 'ct marks can not greater than 20 and attendence mark can not grater than 10')
                    return HttpResponseRedirect(f'/faculty/ct_and_attendence_mark/{course_code}/')       
            else:
                ct_marks = 0
                attend_marks = 0
            student_id = student.student_id
            student_name = student.student_name
            session = student.session
            semester_no = course.semister_no
            course_code = course_code
            course_name = course.course_name
            course_teacher = course.course_teacher
            credit = course.credit
            remarks = student.remarks
            ct_marks = ct_marks
            attendence_marks = attend_marks
            total_ct_and_attendence_marks = ct_marks + attendence_marks
            checker = Attendence_and_CT_Mark.objects.filter(student_id= student_id, course_code=course_code, course_teacher= course.course_teacher)
            flag = False
            for c in checker:
                id = c.id
                data = Attendence_and_CT_Mark(id=id,student_id = student_id,student_name = student_name,session = session,semester_no = semester_no,course_code = course_code,course_name = course_name,course_teacher = course_teacher,credit = credit,remarks =remarks,ct_marks = ct_marks,attendence_marks = attendence_marks,total_ct_and_attendence_marks = total_ct_and_attendence_marks)
                data.save()
                flag = True
            if flag == False:
                data = Attendence_and_CT_Mark(
                    student_id = student_id,
                    student_name = student_name,
                    session = session,
                    semester_no = semester_no,
                    course_code = course_code,
                    course_name = course_name,
                    course_teacher = course_teacher,
                    credit = credit,
                    remarks =remarks,
                    ct_marks = ct_marks,
                    attendence_marks = attendence_marks,
                    total_ct_and_attendence_marks = total_ct_and_attendence_marks
                    )
                data.save()
        messages.success(request,'CT and Attendence Mark Added Successfully!!!!')
        return HttpResponseRedirect(f'/faculty/student_ct_and_attendence_mark/{course_code}/')  
    return render(request, 'faculty/ct_and_attendence_mark.html', context)

def student_ct_and_attendence_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_student_ct_and_attend_marks:
        count += 1
    for stu in backLog_student_ct_and_attend_marks:
        count += 1
        backLogStudents[stu] = count
    context = {
        'course_code': course_code,
        'course_name': course.course_name,
        'credit': course.credit,
        'semester_no': course.semister_no,
        'course_teacher': course.course_teacher,
        'regular_student_ct_and_attend_marks': regular_student_ct_and_attend_marks,
        'backLogStudents': backLogStudents,
        'special_student_ct_and_attend_marks': special_student_ct_and_attend_marks,
    }
    return render(request, 'faculty/student_ct_and_attendence_mark.html', context)

def edit_ct_and_attendence_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_student_ct_and_attend_marks:
        count += 1
    for stu in backLog_student_ct_and_attend_marks:
        count += 1
        backLogStudents[stu] = count
    context = {
        'course_code': course_code,
        'course_name': course.course_name,
        'credit': course.credit,
        'semester_no': course.semister_no,
        'course_teacher': course.course_teacher,
        'regular_student_ct_and_attend_marks': regular_student_ct_and_attend_marks,
        'backLogStudents': backLogStudents,
        'special_student_ct_and_attend_marks': special_student_ct_and_attend_marks,
    }
    if request.method == 'POST':
        course = Course.objects.get(course_code= course_code)
        students = Teacher_Student_Info.objects.filter(course_code= course_code)
        ct_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code)
        context = {
            'semister_no': course.semister_no,
            'c_code': course_code,
            'c_teacher': course.course_teacher,
            'credit': course.credit,
            'c_name': course.course_name,
            'students': students,
            'ct_attend_marks': ct_attend_marks,
            }
        for student in students:
            ct_marks = request.POST.get(f'{student.student_id}')
            attend_marks = request.POST.get(f'{student.student_name}')
            if ct_marks and attend_marks:
                ct_marks = (float(ct_marks))
                attend_marks = (float(attend_marks))
                if ct_marks > 20 or attend_marks > 10:
                    messages.warning(request, 'ct marks can not greater than 20 and attendence mark can not grater than 10')
                    return HttpResponseRedirect(f'/faculty/edit_ct_and_attendence_mark/{course_code}/')       
            else:
                ct_marks = 0
                attend_marks = 0
            student_id = student.student_id
            student_name = student.student_name
            session = student.session
            semester_no = course.semister_no
            course_code = course_code
            course_name = course.course_name
            course_teacher = course.course_teacher
            credit = course.credit
            remarks = student.remarks
            ct_marks = ct_marks
            attendence_marks = attend_marks
            total_ct_and_attendence_marks = ct_marks + attendence_marks
            checker = Attendence_and_CT_Mark.objects.filter(student_id= student_id, course_code=course_code, course_teacher= course.course_teacher)
            flag = False
            for c in checker:
                id = c.id
                data = Attendence_and_CT_Mark(id=id,student_id = student_id,student_name = student_name,session = session,semester_no = semester_no,course_code = course_code,course_name = course_name,course_teacher = course_teacher,credit = credit,remarks =remarks,ct_marks = ct_marks,attendence_marks = attendence_marks,total_ct_and_attendence_marks = total_ct_and_attendence_marks)
                data.save()
                flag = True
            if flag == False:
                data = Attendence_and_CT_Mark(
                    student_id = student_id,
                    student_name = student_name,
                    session = session,
                    semester_no = semester_no,
                    course_code = course_code,
                    course_name = course_name,
                    course_teacher = course_teacher,
                    credit = credit,
                    remarks =remarks,
                    ct_marks = ct_marks,
                    attendence_marks = attendence_marks,
                    total_ct_and_attendence_marks = total_ct_and_attendence_marks
                    )
                data.save()
        messages.success(request,'CT and Attendence Mark Added Successfully!!!!')
        return HttpResponseRedirect(f'/faculty/student_ct_and_attendence_mark/{course_code}/') 
    return render(request, 'faculty/edit_ct_and_attendence_mark.html', context)

def Theory_mark_sheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
    checker = Theory_Marks.objects.filter(course_code= course_code)
    for c in checker:
        return HttpResponseRedirect(f'/faculty/update_theory_marks/{course_code}/')
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    for stu in backLog_students:
        count += 1
        backLogStudents[stu] = count
    if request.method == 'POST':
        for student in regular_students:
            total_marks = 0
            count = 0;
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/detailed_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        for student in backLog_students:
            total_marks = 0
            count = 0;
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/detailed_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        for student in special_students:
            total_marks = 0
            count = 0;
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/detailed_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        
        messages.success(request, 'Theory Marks added/updated successfully')
        return HttpResponseRedirect(f'/faculty/show_theory_marks/{course_code}/')
            
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_students': regular_students,
        'backLogStudents': backLogStudents,
        'special_students': special_students,
        }
    return render(request, 'faculty/detailed_mark_sheet.html', context)

def show_theory_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students_marks = Theory_Marks.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
    backLog_students_marks = Theory_Marks.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
    special_students_marks = Theory_Marks.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students_marks:
        count += 1
    for stu in backLog_students_marks:
        count += 1
        backLogStudents[stu] = count
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_students_marks': regular_students_marks,
        'backLogStudents': backLogStudents,
        'special_students_marks': special_students_marks,
        }
    return render(request, 'faculty/show_theory_marks.html', context)

def update_theory_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students_theory_marks = Theory_Marks.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students_theory_marks = Theory_Marks.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students_theory_marks = Theory_Marks.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students_theory_marks:
        count += 1
    for stu in backLog_students_theory_marks:
        count += 1
        backLogStudents[stu] = count
    
    if request.method == 'POST':
        regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
        backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
        special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
        for student in regular_students:
            total_marks = 0
            count = 0;
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/Theory_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        for student in backLog_students:
            total_marks = 0
            count = 0;
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/Theory_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        for student in special_students:
            total_marks = 0
            count = 0;
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/Theory_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        
        messages.success(request, 'Theory Marks added/updated successfully')
        return HttpResponseRedirect(f'/faculty/show_theory_marks/{course_code}/')
    context = {
        'course_code': course_code,
        'course_name': course.course_name,
        'credit': course.credit,
        'semester_no': course.semister_no,
        'course_teacher': course.course_teacher,
        'regular_students_theory_marks': regular_students_theory_marks,
        'backLogStudents': backLogStudents,
        'special_students_theory_marks': special_students_theory_marks,
    }
    return render(request, 'faculty/update_theory_marks.html', context)

def consolidated_marks_sheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    consolidated_marks_regular = {}
    consolidated_marks_backLog = {}
    consolidated_marks_special = {}
    for student in regular_students:
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        theory_marks = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course_code)
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        for mark in theory_marks:
            theory_mark = mark.total_marks
        total_marks = ct_marks + attendence_mark + theory_mark
        if total_marks >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks > 74 and total_marks < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks > 69 and total_marks < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks > 64 and total_marks < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks > 59 and total_marks < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks > 54 and total_marks < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks > 49 and total_marks < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks > 44 and total_marks < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks > 39 and total_marks < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        consolidated_marks_regular[student] = {'ct_mark': ct_marks, 'attendence_mark': attendence_mark,
        'theory_mark':theory_mark, 'full_marks': total_marks, 'LG': LG, 'GP': GP}
    
    for student in backLog_students:
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        theory_marks = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course_code)
        ct_marks = 0
        attendence_mark = 0
        theory_mark =0 
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        for mark in theory_marks:
            theory_mark = mark.total_marks
        total_marks = ct_marks + attendence_mark + theory_mark
        if total_marks >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks > 74 and total_marks < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks > 69 and total_marks < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks > 64 and total_marks < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks > 59 and total_marks < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks > 54 and total_marks < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks > 49 and total_marks < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks > 44 and total_marks < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks > 39 and total_marks < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        count += 1
        consolidated_marks_backLog[student] = {'ct_mark': ct_marks, 'attendence_mark': attendence_mark,
        'theory_mark':theory_mark, 'full_marks': total_marks, 'LG': LG, 'GP': GP, 'count': count}
    
    for student in special_students:
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        theory_marks = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course_code)
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        for mark in theory_marks:
            theory_mark = mark.total_marks
        total_marks = ct_marks + attendence_mark + theory_mark
        if total_marks >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks > 74 and total_marks < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks > 69 and total_marks < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks > 64 and total_marks < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks > 59 and total_marks < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks > 54 and total_marks < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks > 49 and total_marks < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks > 44 and total_marks < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks > 39 and total_marks < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        consolidated_marks_special[student] = {'ct_mark': ct_marks, 'attendence_mark': attendence_mark,
        'theory_mark':theory_mark, 'full_marks': total_marks, 'LG': LG, 'GP': GP}
    
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'consolidated_marks_regular': consolidated_marks_regular,
        'consolidated_marks_backLog': consolidated_marks_backLog,
        'consolidated_marks_special': consolidated_marks_special,
    }
    return render(request, 'faculty/consolidated_marks_sheet.html', context)

def send_to_controller_theory_marks(request,course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Theory_Marks.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Theory_Marks.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Theory_Marks.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'regular_students': regular_students,
        'backLog_students': backLog_students,
        'special_students': special_students,
    }
    return render(request, 'faculty/send_to_controller.html', context)