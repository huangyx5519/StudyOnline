# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField

from courses.models import Course
from users.models import UserProfile

# class PublishForm(forms.Form):
#
#     name = forms.CharField(max_length=50, verbose_name=u"课程名称")
#     desc = forms.CharField(max_length=300, verbose_name=u"课程描述")
#     detail = forms.CharField(max_length=300, verbose_name=u"课程详情")
#     degree = forms.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2, verbose_name=u"难度")
#     learn_times = forms.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    # image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图")







    # image = models.ImageField(default='', upload_to="teachers/%Y/%m", verbose_name=u"老师头像")


class beTeacherForm(forms.Form):
    work_years = forms.IntegerField()
    work_company = forms.CharField(max_length=50)
    work_position = forms.CharField(max_length=50)
    points = forms.CharField(max_length=50)

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5,error_messages={"invalid": u"密码至少包含5个字符",'required':u"密码至少包含5个字符"})
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误",'required':u"请输入验证码"})




class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class UploadCourseImgForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']