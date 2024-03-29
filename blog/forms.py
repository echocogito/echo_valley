# !/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2019/6/29 22:38
# @Author  :Noperx
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from mdeditor.widgets import MDEditorWidget

from blog.models import Blog, BlogType


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=30, min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    email = forms.CharField(label='邮箱',
                            widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    password = forms.CharField(label='密码', min_length=8,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='确认密码', min_length=8, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请确认密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_again != password:
            raise forms.ValidationError('两次输入的密码不一致')
        return password


class BlogTypeForm(forms.ModelForm):
    class Meta:
        model = BlogType
        fields = ['type_name']
        lables = {'type_name': '新标签'}
        widgets = {'type_name': forms.TextInput(attrs={'class': 'form-control'})}


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'blog_type', 'content']
        labels = {'title': '标题', 'content': '正文', 'blog_type': '标签'}
        # widgets = {'content': CKEditorWidget()}
        widgets = {
            'content': MDEditorWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
