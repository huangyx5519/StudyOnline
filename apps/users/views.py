#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from django.db import transaction
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from utils.utils import *

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

import json

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm, beTeacherForm, \
    UploadCourseImgForm
from utils.email_send import send_register_email

from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrganization, Teacher
from courses.models import Course, Lesson, Video

from utils.mixin_utils import LoginRequireMixin

# Create your views here.



class Index(View):
    def get(self,request):
        teachers = Teacher.objects.all().order_by('click_num')[:4]
        courses = Course.objects.all().order_by('click_num')[:4]
        return render(request, "index.html", {
            'teachers': teachers,
            'courses':courses,
        })

class SendMsg(View):
    def post(self,request):
        receiver = request.POST.get("receiver", "")
        text = request.POST.get("text", "")
        msg =  (text + "\n  from " + request.user.username )

        sendMsg(receiver,msg,request.user.id)
        return render(request, 'usercenter-message.html', {
            'msg':"消息发送成功",
        })



class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form':register_form})

    def post(self, request):
        with transaction.atomic():
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                username = request.POST.get("email", "")
                if UserProfile.objects.filter(email=username):
                    return render(request, "register.html", {"msg": "用户已存在", "register_form": register_form})
                password = request.POST.get("password", "")
                user_profile = UserProfile()
                user_profile.username = username
                user_profile.email = username
                user_profile.password = make_password(password)
                user_profile.is_active = False
                user_profile.save()

                # 写入欢迎注册消息
                sendMsg(user_profile.id,"欢迎")

                #返回消息
                send_register_email(username, "register")

                return render(request, "login.html",{"returnMsg":"激活邮件已经发送至您邮箱，请尽快激活"})
            else:
                return render(request, "register.html", {"register_form": register_form})


class LogoutView(View):
    '''
    用户登出
    '''
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活!"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class ForgetPasswordView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_sucess.html")
        else:
            return render(request, "forgetpwd.html", {"forgetpwd.html": forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    '''
    修改用户密码
    '''
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})


class UserInfoView(LoginRequireMixin, View):
    '''
    用户个人信息
    '''
    def get(self, request):

        return render(request, 'usercenter-info.html', {

        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type="application/json")


class BeTeacher(View):
    def get(self, request):
        return render(request, 'usercenter-beteacher.html', {

        })

    def post(self, request):
        teacher_form = beTeacherForm(request.POST)
        if teacher_form.is_valid():
            # teacher = request.user.teacher_role
            teacher_id = request.user.teacher_id
            if teacher_id:
                teacher = Teacher.objects.get(id = teacher_id)
                teacher.work_years = request.POST.get("work_years", "")
                teacher.work_company = request.POST.get("work_company", "")
                teacher.work_position = request.POST.get("work_position", "")
                teacher.points = request.POST.get("points", "")
                teacher.name = request.user.nick_name
                teacher.save()
            else:
                teacher = Teacher()
                teacher.work_years = request.POST.get("work_years", "")
                teacher.work_company = request.POST.get("work_company", "")
                teacher.work_position = request.POST.get("work_position", "")
                teacher. points = request.POST.get("points", "")
                teacher.name = request.user.nick_name
                teacher.save()
                user = UserProfile.objects.get(id=int(request.user.id))
                user.teacher_id = teacher.id
                user.save()

        return render(request, 'usercenter-info.html', {
        })


from django.db import transaction
class Publish(View):
    def get(self, request):
        teacher = Teacher.objects.get(id=request.user.teacher_id)
        courses = teacher.course_set.all()

        lesson_id = request.GET.get("ls", "")
        course_id = request.GET.get('ID', "")
        is_del = request.GET.get('del', "")


        if course_id:
            course =Course.objects.get(id=course_id)
            lessons = course.lesson_set.all()
            if is_del:
                course.delete()



            if lesson_id:
                lesson = Lesson.objects.get(id = lesson_id)
            else:
                lesson = None

        else:
            lessons = None
            course = None
            lesson = None





        return render(request, 'usercenter-publish-course.html', {
            "courses": courses,
            "lessons":lessons,
            "course_re":course,
            "lesson_re":lesson,
              })

        # return render(request, 'usercenter-publish-course.html', {"courses":courses
        # })

    def post(self, request):

        ID=request.POST.get("id","")
        type = request.POST.get("type", "")
        if int(type)>0:
        #添加课程

        #此处类似于 读者－写者 模型
        #添加行级锁，防止改动课程时用户进入读取错误信息
            with transaction.atomic():
                if ID:
                    lesson=Lesson.objects.select_for_update().get(id=ID)
                else:
                    lesson=Lesson()
                lesson.course_id = request.POST.get("cId","")
                lesson.name=request.POST.get("name","")
                lesson.save()
                video = Video()
                video.lesson_id =lesson.id
                video.name = lesson.name
                video.url = request.POST.get("url","")
                video.save()




        else:
        #进行事务处理,保证课程发布可以通知到每个关注者
            with transaction.atomic():
                if ID:
                    course=Course.objects.select_for_update().get(id=ID)
                else:
                    course = Course()

                teacher = Teacher.objects.get(id = request.user.teacher_id)

                course.name=request.POST.get("name", "")
                course.tag= request.POST.get("tag", "")
                course.desc=request.POST.get("desc", "")
                course.detail = request.POST.get("detail", "")
                course.degree = request.POST.get("degree", "")
                course.learn_times = request.POST.get("learn_times", "")
                course.teacher = teacher
                course.save()
                teacher_id = teacher.id


            users = UserFavorite.objects.filter(fav_id = teacher_id, fav_type=1)
            if ID:
                for user in users:
                    sendMsg(user.user_id,teacher.name+"修改了课程:"+ course.name ,teacher.id)
            else:
                for user in users:
                    sendMsg(user.user_id, teacher.name + "发布了新课程:" + course.name, teacher.id)


        return render(request, 'usercenter-publish-course.html', {
        })








class UploadImageView(LoginRequireMixin, View):
    '''
    用户修改头像
    '''
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class UploadCourseImgView(LoginRequireMixin, View):
    '''
    修改课程封面
    '''
    def post(self, request,course_id):
        course = Course.objects.get(id=int(course_id))
        if course_id:
            image_form = UploadCourseImgForm(request.POST, request.FILES, instance=course)
            if image_form.is_valid():
                image_form.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    '''
    个人中心修改用户密码
    '''
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type="application/json")
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type="application/json")


class SendMailCodeView(LoginRequireMixin, View):
    '''
    发送邮箱验证码
    '''
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type="application/json")
        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type="application/json")


class UpdateEmailView(LoginRequireMixin, View):
    '''
    修改个人邮箱
    '''
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email")
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type="application/json")


class MyCourseView(LoginRequireMixin, View):
    '''
    我的课程
    '''
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses,

        })


class MyFavOrgView(LoginRequireMixin, View):
    '''
    我收藏的课程机构
    '''
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrganization.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list,

        })


class MyFavTeacherView(LoginRequireMixin, View):
    '''
    我收藏的课程机构
    '''
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list,

        })


class MyFavCourseView(LoginRequireMixin, View):
    '''
    我收藏的课程
    '''
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,

        })


class MyMessageView(LoginRequireMixin, View):
    '''
    我的消息
    '''
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id).order_by("-add_time")

        # 用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages': messages,

        })

