from email import message
from sys import flags
from django.shortcuts import render, HttpResponseRedirect
from authentication.models import ExamCommitte, Student
from chairman.models import Running_Semester, Course, Teacher_Student_Info
from django.contrib.auth import logout
from faculty.models import *
from . models import External_teacher_marks, Send_To_Third_Examinner, Third_Examinner_Marks
# Create your views here.
def exam_committe_profile(request):
    exam_committe = ExamCommitte.objects.filter(email = request.user)
    return render(request, 'examcommite/profile.html', {'exam_committe': exam_committe})

#logout
def exam_committe_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')

def exam_committte_current_courses(request):
    exam_committe = ExamCommitte.objects.filter(email = request.user)
    running_semester = Running_Semester.objects.all()
    courses = Course.objects.all()
    context={
        'exam_committe': exam_committe,
        'running_semester': running_semester,
        'courses': courses,
    }
    return render(request, 'examcommite/current_courses.html', context)

def exam_committte_special_courses(request):
    all_semesters = ['1st Year 1st Semester', '1st Year 2nd Semester', '2nd Year 1st Semester', '2nd Year 2nd Semester',
    '3rd Year 1st Semester', '3rd Year 2nd Semester', '4th Year 1st Semester', '4th Year 2nd Semester']
    running_semester = Running_Semester.objects.all()
    exam_committe = ExamCommitte.objects.filter(email = request.user)
    courses = Course.objects.all()
    special_semester = []
    for s in all_semesters:
        flag = False
        for r in running_semester:
            if s == r.semester_no:
                flag = True
        if flag == False:
            special_semester.append(s)
    
    context = {
        'exam_committe': exam_committe,
        'special_semester': special_semester,
        'courses': courses,
    }
    
    return render(request, 'examcommite/special_courses.html', context)

def exam_committe_course_details(request, course_code):
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
    return render(request, 'examcommite/course_details.html', context)  

def course_teacher_marks(request, course_code):
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
    return render(request, 'examcommite/course_teacher_marks.html', context)

def external_teacher_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    checker = External_teacher_marks.objects.filter(course_code=course_code)
    for c in checker:
        return HttpResponseRedirect(f'/examcommitte/edit_external_teacher_marks/{course_code}/')
    if request.method == 'POST':
        for r in regular_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        for r in backLog_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        for r in special_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        return HttpResponseRedirect(f"/examcommitte/details_external_teacher_marks/{course_code}")
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'regular_students': regular_students,
        'backLog_students': backLog_students,
        'special_students': special_students,
    }
    return render(request, 'examcommite/external_teacher_marks.html', context)

def details_external_teacher_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'regular_students': regular_students,
        'backLog_students': backLog_students,
        'special_students': special_students,
    }
    return render(request, 'examcommite/details_external_teacher_marks.html', context)

def edit_external_teacher_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    if request.method == 'POST':
        for r in regular_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        for r in backLog_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        for r in special_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        return HttpResponseRedirect(f'/examcommitte/details_external_teacher_marks/{course_code}/')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'regular_students': regular_students,
        'backLog_students': backLog_students,
        'special_students': special_students,
    }
    return render(request, 'examcommite/edit_external_teacher_marks.html', context)

def compare_internal_external_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    checker = Third_Examinner_Marks.objects.filter(course_code= course_code)
    for check in checker:
        return HttpResponseRedirect(f'/examcommitte/edit_third_examinner_mark/{course_code}/')
    students = Teacher_Student_Info.objects.filter(course_code = course_code).order_by('student_id')
    third_examine_students = {}
    all_teacher_marks = {}
    save_button = False
    for s in students:
        course_teacher_mark = Theory_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_teacher_marks.objects.get(student_id= s.student_id, course_code= course_code)
        dif = abs((course_teacher_mark.total_marks) - (external_teacher_mark.marks))
        average_marks = ((course_teacher_mark.total_marks) + (external_teacher_mark.marks))/2
        third_examiner_mark = False
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_marks, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.marks, 'third_examiner_mark': third_examiner_mark}
    
    if request.method == 'POST':
        for key, value in third_examine_students.items():
            data = request.POST.get(f'totalMark_{key.student_id}')
            if data:
                marks = float(data)
                student_id = key.student_id
                course_code = course_code
                session = key.session
                data = Third_Examinner_Marks(
                    student_id = student_id,
                    course_code = course_code,
                    session = session,
                    marks = marks
                )
                checker = Third_Examinner_Marks.objects.filter(student_id = student_id, course_code= course_code)
                flag = False
                for c in checker:
                    flag = True
                    id = c.id
                if flag == True:
                    data = Third_Examinner_Marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        session = session,
                        marks = marks
                    )
                    data.save()
                else:
                    data.save()
        return HttpResponseRedirect(f'/examcommitte/show_all_marks/{course_code}/')
    
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'all_teacher_marks': all_teacher_marks,
        'save_button': save_button,
    }
    return render(request, 'examcommite/compare_internal_external_marks.html', context)

def edit_third_examinner_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    third_examine_students = {}
    all_teacher_marks = {}
    save_button = False
    for s in regular_students:
        course_teacher_mark = Theory_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_teacher_marks.objects.get(student_id= s.student_id, course_code= course_code)
        dif = abs((course_teacher_mark.total_marks) - (external_teacher_mark.marks))
        average_marks = ((course_teacher_mark.total_marks) + (external_teacher_mark.marks))/2
        third_examiner_mark = False
        prev_value = 0
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
            value = Third_Examinner_Marks.objects.filter(student_id= s.student_id, course_code= course_code)
            for v in value:
                prev_value = v.marks
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_marks, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.marks, 'third_examiner_mark': third_examiner_mark, 'prev_value': prev_value}
    for s in backLog_students:
        course_teacher_mark = Theory_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_teacher_marks.objects.get(student_id= s.student_id, course_code= course_code)
        dif = abs((course_teacher_mark.total_marks) - (external_teacher_mark.marks))
        average_marks = ((course_teacher_mark.total_marks) + (external_teacher_mark.marks))/2
        third_examiner_mark = False
        prev_value = 0
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
            value = Third_Examinner_Marks.objects.filter(student_id= s.student_id, course_code= course_code)
            for v in value:
                prev_value = v.marks
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_marks, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.marks, 'third_examiner_mark': third_examiner_mark, 'prev_value': prev_value}
    for s in special_students:
        course_teacher_mark = Theory_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_teacher_marks.objects.get(student_id= s.student_id, course_code= course_code)
        dif = abs((course_teacher_mark.total_marks) - (external_teacher_mark.marks))
        average_marks = ((course_teacher_mark.total_marks) + (external_teacher_mark.marks))/2
        third_examiner_mark = False
        prev_value = 0
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
            value = Third_Examinner_Marks.objects.filter(student_id= s.student_id, course_code= course_code)
            for v in value:
                prev_value = v.marks
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_marks, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.marks, 'third_examiner_mark': third_examiner_mark, 'prev_value': prev_value}
    
    if request.method == 'POST':
        for key, value in third_examine_students.items():
            data = request.POST.get(f'totalMark_{key.student_id}')
            if data:
                marks = float(data)
                student_id = key.student_id
                course_code = course_code
                session = key.session
                data = Third_Examinner_Marks(
                    student_id = student_id,
                    course_code = course_code,
                    session = session,
                    marks = marks
                )
                checker = Third_Examinner_Marks.objects.filter(student_id = student_id, course_code= course_code)
                flag = False
                for c in checker:
                    flag = True
                    id = c.id
                if flag == True:
                    data = Third_Examinner_Marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        session = session,
                        marks = marks
                    )
                    data.save()
                else:
                    data.save()
        return HttpResponseRedirect(f'/examcommitte/show_all_marks/{course_code}/')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'all_teacher_marks': all_teacher_marks,
        'save_button':save_button,
    }
    return render(request, 'examcommite/edit_third_examinner_mark.html', context)
def show_all_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    student_marks = {}
    for student in regular_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2  
        
        student_marks[student] = {'course_teacher_mark': course_teacher_mark, 'external_teacher_mark': external_teacher_mark, 
        'third_examinner_mark': third_examinner_mark, 'average_mark': average_mark}
    for student in backLog_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2  
        
        student_marks[student] = {'course_teacher_mark': course_teacher_mark, 'external_teacher_mark': external_teacher_mark, 
        'third_examinner_mark': third_examinner_mark, 'average_mark': average_mark}
    for student in special_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2  
        
        student_marks[student] = {'course_teacher_mark': course_teacher_mark, 'external_teacher_mark': external_teacher_mark, 
        'third_examinner_mark': third_examinner_mark, 'average_mark': average_mark}
       
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'student_marks': student_marks,
    }
    return render(request, 'examcommite/show_all_marks.html', context)

def mark_sheet_details(request, course_code):
    course = Course.objects.get(course_code= course_code)
    credit = course.credit
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks= 'Special').order_by('student_id')
    mark_sheets = {}
    for student in regular_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        s = Student.objects.get(student_id = student.student_id)
        full_name = s.first_name + " " + s.last_name
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2    
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        ct_marks = 0
        attendence_mark = 0
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        total_marks = ct_marks + attendence_mark + average_mark
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
        PS = credit * GP
        mark_sheets[student] = {'ct_marks': ct_marks, 'attendence_mark': attendence_mark, 'full_name': full_name,
        'average_mark': average_mark, 'total_marks': total_marks, 'LG': LG, 'GP': GP, 'PS': PS}
    for student in backLog_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        s = Student.objects.get(student_id = student.student_id)
        full_name = s.first_name + " " + s.last_name
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2    
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        ct_marks = 0
        attendence_mark = 0
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        total_marks = ct_marks + attendence_mark + average_mark
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
        PS = credit * GP
        mark_sheets[student] = {'ct_marks': ct_marks, 'attendence_mark': attendence_mark, 'full_name': full_name,
        'average_mark': average_mark, 'total_marks': total_marks, 'LG': LG, 'GP': GP, 'PS': PS}
    for student in special_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        s = Student.objects.get(student_id = student.student_id)
        full_name = s.first_name + " " + s.last_name
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2    
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        ct_marks = 0
        attendence_mark = 0
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        total_marks = ct_marks + attendence_mark + average_mark
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
        PS = credit * GP
        mark_sheets[student] = {'ct_marks': ct_marks, 'attendence_mark': attendence_mark, 'full_name': full_name,
        'average_mark': average_mark, 'total_marks': total_marks, 'LG': LG, 'GP': GP, 'PS': PS}
    
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'mark_sheets': mark_sheets,
    }
    return render(request, 'examcommite/mark_sheet_details.html', context)
