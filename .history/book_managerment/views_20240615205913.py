from django.shortcuts import render
from book_managerment import models
from django.shortcuts import redirect
from django.http import HttpResponse
import hashlib
from django.http import HttpResponseRedirect
from book_managerment.models import LmsUser
from book_managerment.models import Book
from book_managerment.models import Borrow
from book_managerment.models import overdue

from django.utils import timezone
from datetime import timedelta


def index(request):
    return render(request, 'index.html')
 
# 登录
def user_login(request):
    if request.method == 'POST' and request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        e = LmsUser.objects.filter(username = username).first()
        
        if e:
            if e.password == password:
                #user = models.LmsUser.objects.get(id=user)
                return render(request, 'user_home.html', {'user': e})
            else:
                return HttpResponse("密码错误")
        else:
            return HttpResponse("用户名不存在")
    
    return render(request, "user_login.html")

'''def user_home(request, username):
    # 显示当前用户的所有信息
    e = LmsUser.objects.filter(username = username).first()
    context = {
        'user': e
    }
    return render(request, 'user_home.html', context)'''

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get("password")
        e = LmsUser.objects.filter(username = username).first()
        
        if e:
            if e.is_admin:
                if e.password == password:
                    return redirect('/book_list/')
                else:
                    return HttpResponse("密码错误")
            else:
                return HttpResponse("您不是管理员")
        else:
            return HttpResponse("用户名不存在")
 
    return render(request, "admin_login.html")

def book_search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        uname = request.POST.get('username')
        #print(uname)
        try:
            book = Book.objects.get(name__icontains=search_query)
            username = LmsUser.objects.get(username__icontains=username)
            context = {
                'context': book
            }
            '''
            return render(request, 'book_search_result.html', {"book":book, "username":username})
        except Book.DoesNotExist:
            error_message = "没有此藏书"
            return render(request, 'book_search_result.html', {'error_message': error_message})

    return render(request, 'book_search.html')

def book_borrow(request, book_id, username):
    if request.method == 'GET':
        book = models.Book.objects.get(id=int(book_id))
         # 检查用户是否已经借阅了5本图书
        #uname = request.session.get('id')
        username = LmsUser.objects.get(username=int(username))
        print(username)
        uname = username
        if Borrow.objects.filter(user=uname, is_return=False).count() >= 5:
            # 如果已经借阅了5本图书，拒绝借阅请求
            return render(request, 'borrow_limit_exceeded.html')
        
        # 检查用户是否有逾期未归还的图书
        overdue_records = overdue.objects.filter(user=uname, is_return=False, return_date__lt=timezone.now())
        if overdue_records.exists():
            # 如果有逾期未归还的图书，设置用户的可借状态为no
            request.user.is_allow_borrow = False
            request.user.save()
            overdue_records = overdue.objects.filter(user=uname, is_return=False, return_date__lt=timezone.now())
            return render(request, 'overdue_book.html', {'overdue_records': overdue_records})
        
        # 创建借阅记录
        borrow_record = Borrow(user=uname, book=book, borrow_date=timezone.now(), return_date=timezone.now() + timedelta(days=14))
        borrow_record.save()
        
        return redirect('book_search')
    else:
        return render(request, 'book_search.html')

def book_return(request):
    if request.method == 'GET':
        book_id = request.GET.get('book_id')
        book = Book.objects.get(id=book_id)
        
        # 查找用户借阅的记录
        borrow_record = Borrow.objects.get(user=request.user, book=book, is_return=False)
        
        # 更新借阅记录
        borrow_record.return_date = timezone.now()
        borrow_record.is_return = True
        borrow_record.save()
        
        # 检查是否有预约该图书的用户，如果有则发送提醒
        
        # 检查是否可以解除用户的借书限制
        overdue_records = overdue.objects.filter(user=request.user, is_return=False, return_date__lt=timezone.now())
        if not overdue_records.exists():
            request.user.can_borrow = True
            request.user.save()
        
        return redirect('book_search')
    else:
        return render(request, 'book_search.html')
    
def book_appointment(request):
    if request.method == 'GET':
        book_id = request.GET.get('book_id')
        book = Book.objects.get(id=book_id)
        # 这里可以添加预约逻辑，例如将书籍标记为已预约
        return redirect('book_search')  # 重定向到书籍搜索页面


'''## 出版社
# 出版社列表
def publisher_list(request): #处理用户提交的表单数据，将数据保存到数据库中的Book模型对象中，然后根据操作结果重定向用户到另一个页面或者返回一个包含表单的页面
    publishers = models.Publisher.objects.all()
    return render(request, 'publisher_list.html', {'publisher': publishers})

# 添加出版社
def add_publisher(request):
    if request.method == 'POST':
        new_publisher_name = request.POST.get('name')
        new_publisher_addr = request.POST.get('addr')
        models.Publisher.objects.create(name=new_publisher_name, addr=new_publisher_addr)
        return redirect('/publisher_list/')
    return render(request, 'publisher_add.html')

# 编辑出版社
def edit_publisher(request):
    if request.method == 'POST':
        edit_id = request.GET.get('id')
        edit_obj = models.Publisher.objects.get(id=edit_id)
        new_name = request.POST.get('edit_name')
        new_addr = request.POST.get('edit_addr')
        edit_obj.name = new_name
        edit_obj.addr = new_addr
        edit_obj.save()
        return redirect('/publisher_list/')
 
    edit_id = request.GET.get('id')
    edit_obj = models.Publisher.objects.get(id=edit_id)
    return render(request, 'publisher_edit.html', {'publisher': edit_obj})

# 删除出版社
def drop_publisher(request):
    drop_id = request.GET.get('id')
    drop_obj = models.Publisher.objects.get(id=drop_id)
    drop_obj.delete()
    return redirect('/publisher_list/')'''



## 图书增删改查
# 书籍的列表
def book_list(request):
    book = models.Book.objects.all()
    return render(request, 'book_list.html', {'book_list': book})
 
 
# 添加本书籍
def add_book(request):
    if request.method == 'POST':
        new_book_name = request.POST.get('name')
        new_book_author = request.POST.get('author')
        new_book_publish_date = request.POST.get('publish_date')
        new_book_catagoery = request.POST.get('catagoery')
        publisher = request.POST.get('publisher')
        new_book_picture = request.FILES.get('picture')
        models.Book.objects.create(name=new_book_name, author=new_book_author, publish_date=new_book_publish_date, 
                                   catagoery=new_book_catagoery, publisher=publisher, picture=new_book_picture)
        return redirect('/book_list/')
    #res = models.Publisher.objects.all()
    return render(request, 'book_add.html') 
 
 
# 删除本书籍
def drop_book(request, book_id):
    models.Book.objects.filter(id=book_id).delete()
    return redirect('/book_list/')
 
 
# 编辑本书籍
def edit_book(request, book_id):
    if request.method == 'POST':
        edit_obj = models.Book.objects.get(id=book_id)
        new_name = request.POST.get('name')
        new_author = request.POST.get('author')
        new_publish_date = request.POST.get('publish_date')
        new_catagoery = request.POST.get('catagoery')
        new_publisher = request.POST.get('publisher')
        new_picture = request.FILES.get('picture')
        edit_obj.name = new_name
        edit_obj.author = new_author
        edit_obj.publish_date = new_publish_date
        edit_obj.catagoery = new_catagoery
        edit_obj.publisher = new_publisher
        edit_obj.picture = new_picture
        edit_obj.save()
        return redirect('/book_list/')
 
    edit_obj = models.Book.objects.get(id=book_id)
    return render(request, 'book_edit.html', {'book': edit_obj})



'''## 用户增删改查
# 用户列表
def user_list(request):
    user = models.LmsUser.objects.all()
    return render(request, 'user_list.html', {'user_list': user})

# 添加用户
def add_user(request):
    if request.method == 'POST':
        new_user_name = request.POST.get('username')
        new_user_password = request.POST.get('password')
        new_user_email = request.POST.get('email')
        new_user_mobile = request.POST.get('mobile')
        new_user_borrow_num = request.POST.get('borrow_num')
        new_user_is_allow_borrow = request.POST.get('is_allow_borrow')
        new_user_class_major = request.POST.get('class_major')
        models.LmsUser.objects.create(username=new_user_name, password=new_user_password, email=new_user_email,
                                      mobile=new_user_mobile, borrow_num=new_user_borrow_num, is_allow_borrow=new_user_is_allow_borrow,
                                      class_major=new_user_class_major)
        return redirect('/user_list/')
    return render(request, 'user_add.html')

# 删除用户
def drop_user(request, user_id):
    models.LmsUser.objects.filter(id=user_id).delete()
    return redirect('/user_list/')

# 编辑用户
def edit_user(request, user_id):
    if request.method == 'POST':
        edit_obj = models.LmsUser.objects.get(id=user_id)
        new_name = request.POST.get('username')
        new_password = request.POST.get('password')
        new_email = request.POST.get('email')
        new_mobile = request.POST.get('mobile')
        new_borrow_num = request.POST.get('borrow_num')
        new_is_allow_borrow = request.POST.get('is_allow_borrow')
        new_class_major = request.POST.get('class_major')
        edit_obj.username = new_name
        edit_obj.password = new_password
        edit_obj.email = new_email
        edit_obj.mobile = new_mobile
        edit_obj.borrow_num = new_borrow_num
        edit_obj.is_allow_borrow = new_is_allow_borrow
        edit_obj.class_major = new_class_major
        edit_obj.save()
        return redirect('/user_list/')

    edit_obj = models.LmsUser.objects.get(id=user_id)
    return render(request, 'user_edit.html', {'user': edit_obj})'''