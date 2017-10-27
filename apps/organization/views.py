# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from courses.models import Course
from operation.models import UserFavorite
from .models import CourseOrganization,City, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

class OrgView(View):
    def get (self,request):
        all_org = CourseOrganization.objects.all()
        all_cities = City.objects.all()

        city_id = request.GET.get('city',"")
        if city_id:
            all_org = all_org.filter(city_id = int(city_id))

        ct = request.GET.get('ct',"")
        if ct:
            all_org = all_org.filter( category = ct)

        # 机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_org = all_org.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        hot_organizations = all_org.order_by("-click_num")[:3]

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_org = all_org.order_by("-students")
            elif sort == "courses":
                all_org = all_org.order_by("-course_nums")


        organization_nums = all_org.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_org, 5, request=request)
        all_org = p.page(page)

        return render(request,"org-list.html",{
            "all_organizations":all_org,
            "all_cities":all_cities,
            "city_id" : city_id,
            "category":ct,
            "hot_organizations":hot_organizations,
            "organization_nums":organization_nums,
        })




class OrganizationHomeView(View):

    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            # 课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 通过外键反向取出所有课程
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })

class OrganizationCourseView(View):
    '''
    机构课程列表页
    '''

    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        # # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            # 课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 通过外键反向取出所有课程
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })

class OrganizationDescView(View):
    '''
    机构介绍页
    '''

    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        # # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            # 课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })

class OrganizationTeacherView(View):
    '''
    机构讲师页
    '''

    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            # 课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class AddFavView(View):
    '''
    用户收藏
    '''
    def post(self, request):
        # 数据id
        fav_id = request.POST.get('fav_id', 0)
        # 1.课程 2.课程机构 3.讲师
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登录
        if not request.user.is_authenticated():
            # 未登录
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        # 已收藏, 取消
        if exist_records:
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrganization.objects.get(id=int(fav_id))
                course_org.fav_num -= 1
                if course_org.fav_num < 0:
                    course_org.fav_num = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_num -= 1
                if teacher.fav_num < 0:
                    teacher.fav_num = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrganization.objects.get(id=int(fav_id))
                    course_org.fav_num += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_num += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type="application/json")


class TeacherListView(View):
    '''
    课程讲师列表页
    '''
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 课程老师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords) | Q(
                    work_position__icontains=search_keywords))


        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by("-click_num")

        sorted_teachers = Teacher.objects.all().order_by("-click_num")[:3]

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 5, request=request)

        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            'all_teachers': teachers,
            'sorted_teachers': sorted_teachers,
            'sort': sort,

        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        # if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.organization.id):
        #     has_org_faved = True

        # 讲师排行
        sorted_teacher = Teacher.objects.all().order_by("-click_num")[:3]
        return render(request, "teacher-detail.html", {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved,


        })