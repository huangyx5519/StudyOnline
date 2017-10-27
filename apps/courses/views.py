# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from operation.models import UserFavorite, UserCourse, CourseComments
from utils.mixin_utils import LoginRequireMixin
from .models import Course, CourseResource, Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from users.models import UserProfile
from utils.utils import *


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_num')[:3]

        # 课程分类检索
        tag = request.GET.get('tag', "")
        if tag:
            all_courses = all_courses.filter(tag = tag)

        # 课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_num")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)


        return render(request, 'course-list.html', {
            'all_courses': courses,
            'tag':tag,
            'hot_courses':hot_courses
        })

class CourseDetailView(View):
    '''
    课程详情页
    '''
    def get(self, request, course_id):

        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_num += 1
        course.save()


        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            # if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
            #     has_fav_org = True

        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)[:1]
        else:
            related_courses = []

        return render(request, "course-detail.html", {
            'course': course,
            'related_courses': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequireMixin, View):
    '''
    课程章节信息
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))


        # 查询用户是否已经关联了改课程
        user_coursers = UserCourse.objects.filter(user=request.user, course=course)
        if not user_coursers:
            user_course = UserCourse(user=request.user, course=course)
            course.students+=1
            user_course.save()
            course.save()

        course_resources = CourseResource.objects.filter(course=course)
        # 获取所有学习该课程的user
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取所有学习该课程的user学习的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]

        return render(request, 'course-info.html', {
            'course': course,
            'course_resources': course_resources,
            'relate_courses': relate_courses,
        })


class CommentsView(LoginRequireMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course_resources = CourseResource.objects.filter(course=course)
        course_comments = CourseComments.objects.filter(course=course).order_by("-add_time")

        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': course_resources,
            'course_comments': course_comments,
        })


class AddCommentsView(View):
    # 用户添加用户评论
    def post(self, request):
        # 判断用户是否登录
        if not request.user.is_authenticated():
            # 未登录
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            #sendmessage
            receiver_id = UserProfile.objects.get(teacher_id=course.teacher.id).id
            sendMsg(receiver_id,"课程"+course.name +"有了新评论:\n"+  comments  +"\n from " + request.user.nick_name,request.user.id)


            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type="application/json")

        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type="application/json")




class VideoPlayView(View):
    '''
    视频播放页面
    '''
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        # 查询用户是否已经关联了改课程
        user_coursers = UserCourse.objects.filter(user=request.user, course=course)
        if not user_coursers:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        course_resources = CourseResource.objects.filter(course=course)
         # course_resources = "http://127.0.0.1:8000/media/0001.mp4"
        # 获取所有学习该课程的user
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取所有学习该课程的user学习的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]

        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': course_resources,
            'relate_courses': relate_courses,
            'video': video,
        })
