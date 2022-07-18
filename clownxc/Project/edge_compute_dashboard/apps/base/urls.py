#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project: edge_compute_dashboard
@File: urls.py
@Description: //todo
@Author: chen
@Email: chen3494269@163.com
@Date: 2022/7/18 20:23
"""
from django.urls import path
from .views import TestView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("test/", TestView.as_view()),
    path("api/token/", TokenObtainPairView.as_view())
]

