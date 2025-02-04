"""
URL configuration for booktest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from book_managerment import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('user_login/', views.user_login, name='user_login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    #path('user_home/', views.user_home, name='user_home'),
    path('book_search/', views.book_search, name='book_search'),
    #path('book_borrow/', views.book_borrow, name='book_borrow'),
    re_path('book_borrows/(\d+)/', views.book_borrow),
    re_path('book_returns/(\d+)/', views.book_return, name='book_return'),


    path('book_list/', views.book_list, name='book_list'),
    path('add_book/', views.add_book),
    re_path('books/(\d+)/delete/', views.drop_book),
    re_path('books/(\d+)/edit/', views.edit_book),

]