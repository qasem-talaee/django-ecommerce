from django.shortcuts import render, redirect
from app.models import *
from datetime import datetime
from django.db.models import Q
from .form import *
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import random

def diffNowDate(DateStr):
   fmt = '%Y-%m-%d'
   d2 = datetime.strptime(str(datetime.now().year)+'-'+str(datetime.now().month)+'-'+str(datetime.now().day), fmt)
   d1 = datetime.strptime(DateStr, fmt)
   return (d2-d1).days

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_html_email(to_list, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL):
    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, bcc=to_list)
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()

def get_sender_price(id, count):
    product = Product.objects.filter(id=id)
    global sender_id, weight
    for i in product:
        sender_id = i.sender
        weight = i.weight
    sender_way = Sender_way.objects.filter(name=sender_id)
    for i in sender_way:
        if i.price:
            return i.price
        if i.price_per_weight:
            return round(i.price_per_weight*((weight/1000)*count))
    return 0

def get_price(id):
    offer_count = Reduction.objects.filter(product_id=id, status=1).count()
    if offer_count != 0:
        offer = Reduction.objects.filter(product_id=id)
        for i in offer:
            percent = i.percent
            expired_time = i.expired_time
            if diffNowDate(str(expired_time)) < 0:
                product = Product.objects.filter(id=id)
                for i in product:
                    old_price = i.price
                return '<bold class="text-red">%s&#37; OFFER</bold><br><del>$%s</del><br><bold>$%s</bold>' % (percent, old_price, ((1-(percent/100))*old_price))
            else:
                product = Product.objects.filter(id=id)
                for i in product:
                    old_price = '$%s' % (i.price)
                return old_price
    else:
        product = Product.objects.filter(id=id)
        for i in product:
            old_price = '$%s' % (i.price)
        return old_price

def get_price_cart(id):
    offer_count = Reduction.objects.filter(product_id=id, status=1).count()
    old_price = 0
    if offer_count != 0:
        offer = Reduction.objects.filter(product_id=id)
        for i in offer:
            percent = i.percent
            expired_time = i.expired_time
            if diffNowDate(str(expired_time)) < 0:
                product = Product.objects.filter(id=id)
                for i in product:
                    old_price = i.price
                return (1 - (percent / 100)) * old_price
            else:
                product = Product.objects.filter(id=id)
                for i in product:
                    old_price = i.price
                return old_price
    else:
        product = Product.objects.filter(id=id)
        for i in product:
            old_price = i.price
        return old_price

def home(request):
    new_product = Product.objects.filter(Q(status=1) & ~Q(count=0)).order_by('-date')[:10]
    a = []
    for i in new_product:
        b = []
        b.append(i.id)
        b.append(i.name)
        b.append(i.image)
        b.append(i.desc)
        b.append(get_price(i.id))
        a.append(b)
    category = Category.objects.filter(submenu_id=0)
    offer = Reduction.objects.all()
    c = []
    for i in offer:
        if diffNowDate(str(i.expired_time)) < 0:
            product = Product.objects.filter(Q(status=1) & ~Q(count=0) & Q(id=i.product_id))
            for j in product:
                d = []
                d.append(j.id)
                d.append(j.name)
                d.append(j.image)
                d.append(j.desc)
                d.append(get_price(j.id))
                c.append(d)
    context = {
        'new_product': a,
        'category': category,
        'offer': c,
    }
    return render(request, 'index.html', context)

def shop(request):
    per_page = 9
    product_count = Product.objects.filter(Q(status=1)).count()
    count_page = int(product_count/per_page) + 1
    product = Product.objects.filter(Q(status=1))[:per_page]
    a = []
    for i in product:
        b = []
        b.append(i.name)
        b.append(i.image)
        b.append(i.desc)
        b.append(get_price(i.id))
        a.append(b)
    cat = Category.objects.filter(submenu_id=0)
    context = {
        'product': a,
        'count_page': range(count_page),
        'cat': cat,
    }
    return render(request, 'shop.html', context)

def shop_page(request, page):
    per_page = 9
    product_count = Product.objects.filter(Q(status=1)).count()
    count_page = int(product_count / per_page) + 1
    start_page = (page-1)*per_page
    product = Product.objects.filter(Q(status=1))[start_page:per_page]
    a = []
    for i in product:
        b = []
        b.append(i.name)
        b.append(i.image)
        b.append(i.desc)
        b.append(get_price(i.id))
        a.append(b)
    cat = Category.objects.filter(submenu_id=0)
    context = {
        'product': a,
        'count_page': range(count_page),
        'cat': cat,
    }
    return render(request, 'shop.html', context)

def product(request, name):
    product_count = Product.objects.filter(name=name, status=1).count()
    if product_count != 0:
        product = Product.objects.filter(name=name)
        for i in product:
            pro_count = i.count
        a = []
        for i in product:
            b = []
            b.append(i.image)
            b.append(i.name)
            b.append(i.desc)
            b.append(get_price(i.id))
            b.append(i.id)
            a.append(b)
        last_product = Product.objects.filter(status=1)[:10]
        c = []
        for i in last_product:
            d = []
            d.append(i.image)
            d.append(i.name)
            d.append(i.desc)
            d.append(get_price(i.id))
            c.append(d)
        context = {
            'name': name,
            'product': a,
            'last_product': c,
            'count': pro_count,
        }
        return render(request, 'shop-single.html', context)
    else:
        return redirect('/shop/')

def category(request, name):
    per_page = 9
    category_count = Category.objects.filter(name=name).count()
    if category_count != 0:
        category = Category.objects.filter(name=name)
        for i in category:
            cat_id = i.id
        count_page = int(category_count / per_page) + 1
        product = Product.objects.filter(Q(status=1) & Q(category=cat_id))[:per_page]
        a = []
        for i in product:
            b = []
            b.append(i.name)
            b.append(i.image)
            b.append(i.desc)
            b.append(get_price(i.id))
            a.append(b)
        cat = Category.objects.filter(submenu_id=0)
        context = {
            'cat_name': name,
            'product': a,
            'num_page': range(count_page),
            'cat': cat,
        }
        return render(request, 'shop_cat.html', context)
    else:
        return redirect('/shop/')

def category_page(request, name, page):
    per_page = 9
    category_count = Category.objects.filter(name=name).count()
    if category_count != 0:
        category = Category.objects.filter(name=name)
        for i in category:
            cat_id = i.id
        count_page = int(category_count / per_page) + 1
        start_page = (page - 1) * per_page
        product = Product.objects.filter(Q(status=1) & Q(category=cat_id))[start_page:per_page]
        a = []
        for i in product:
            b = []
            b.append(i.name)
            b.append(i.image)
            b.append(i.desc)
            b.append(get_price(i.id))
            a.append(b)
        cat = Category.objects.filter(submenu_id=0)
        context = {
            'cat_name': name,
            'product': a,
            'num_page': range(count_page),
            'cat': cat,
        }
        return render(request, 'shop_cat.html', context)
    else:
        return redirect('/shop/')

def cart(request):
    if 'email' in request.session.keys():
        if request.session['email']:
            user = User.objects.filter(email=request.session['email'])
            for i in user:
                user_id = i.id
            cart = Cart_user.objects.filter(Q(user_id=user_id) & Q(payed=0))
            a = []
            total = 0
            for i in cart:
                product_id = i.product_id
                product = Product.objects.filter(id=product_id)
                for j in product:
                    b = []
                    b.append(j.id)
                    b.append(j.name)
                    b.append(j.image)
                    b.append(i.count)
                    b.append(get_price(j.id))
                    b.append(get_price_cart(j.id)*i.count)
                    total += (get_price_cart(j.id)*i.count)
                    a.append(b)
            context = {
                'detail': a,
                'total': total,
            }
            return render(request, 'cart.html', context)
    else:
        ip = get_client_ip(request)
        cart = Cart_non_user.objects.filter(Q(ip_address=ip))
        a = []
        total = 0
        for i in cart:
            product_id = i.product_id
            product = Product.objects.filter(id=product_id)
            for j in product:
                b = []
                b.append(j.id)
                b.append(j.name)
                b.append(j.image)
                b.append(i.count)
                b.append(get_price(j.id))
                b.append(get_price_cart(j.id) * i.count)
                total += (get_price_cart(j.id) * i.count)
                a.append(b)
        context = {
            'detail': a,
            'total': total,
        }
        return render(request, 'cart.html', context)

def checkout(request):
    auth = 0
    global a, sub_total, user_detail, context, user_id, sender_price, total
    user_detail = ''
    if 'email' in request.session.keys():
        if request.session['email']:
            auth = 1
            user_detail = User.objects.filter(email=request.session['email'])
            for i in user_detail:
                user_id = i.id
            cart = Cart_user.objects.filter(user_id=user_id, payed=0)
            a = []
            sub_total = 0
            sender_price = 0
            total = 0
            for i in cart:
                product = Product.objects.filter(id=i.product_id)
                for j in product:
                    b = []
                    b.append(j.name)
                    b.append(i.count)
                    b.append(get_price_cart(j.id)*i.count)
                    b.append(j.image)
                    a.append(b)
                    sender_price += get_sender_price(j.id, i.count)
                    sub_total += (get_price_cart(j.id)*i.count)
            total = sub_total + sender_price
    else:
        auth = 0
        cart = Cart_non_user.objects.filter(ip_address=get_client_ip(request))
        a = []
        sub_total = 0
        sender_price = 0
        total = 0
        for i in cart:
            product = Product.objects.filter(id=i.product_id)
            for j in product:
                b = []
                b.append(j.name)
                b.append(i.count)
                b.append(get_price_cart(j.id) * i.count)
                b.append(j.image)
                a.append(b)
                sender_price += get_sender_price(j.id, i.count)
                sub_total += (get_price_cart(j.id) * i.count)
        total = sub_total + sender_price
    context = {
        'auth': auth,
        'user': user_detail,
        'order': a,
        'sub_total': sub_total,
        'sender_price': sender_price,
        'total': total,
    }
    return render(request, 'checkout.html', context)

def Profile(request):
    if 'email' in request.session.keys():
        if request.session['email']:
            a = []
            global user_id, name, email, mobile, address, postal_code
            user = User.objects.filter(email=request.session['email'])
            for i in user:
                user_id = i.id
                name = i.name
                email = i.email
                mobile = i.mobile
                address = i.address
                postal_code = i.postal_code
            form = RegisterForm(request.POST or None, initial={'name': name, 'email': email, 'mobile': mobile, 'address': address, 'postal_code': postal_code})
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('name')
                    email = form.cleaned_data.get('email')
                    mobile = form.cleaned_data.get('mobile')
                    address = form.cleaned_data.get('address')
                    postal_code = form.cleaned_data.get('postal_code')
                    User.objects.filter(id=user_id).update(name=name, email=email, mobile=mobile, address=address,postal_code=postal_code)
                    return redirect('/profile/')
            cart = Cart_user.objects.filter(user_id=user_id, payed=1)
            for i in cart:
                product = Product.objects.filter(id=i.product_id)
                for j in product:
                    b = []
                    b.append(j.image)
                    b.append(j.name)
                    b.append(i.date)
                    b.append(i.count)
                    b.append(get_price_cart(j.id)*i.count)
                    b.append(i.send_status)
                    a.append(b)
            context = {
                'detail': a,
                'form': form,
            }
            return render(request, 'profile.html', context)
    else:
        return redirect('/login/')
    return redirect('/login/')

def login(request):
    login_form = LoginForm(request.POST or None)
    register_form = RegisterForm(request.POST or None)
    flag_register = 0
    if request.method == 'POST':
        ###login form
        if request.POST.get('login_submit'):
            if login_form.is_valid():
                email = login_form.cleaned_data.get('email')
                user_exist = User.objects.filter(email=email).count()
                if user_exist != 0:
                    chars = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                    password = ''
                    for i in range(10):
                        password += random.choice(chars)
                    if 'password' in request.session.keys():
                        del request.session['password']
                    if 'user_id' in request.session.keys():
                        del request.session['user_id']
                    request.session['password'] = password
                    user = User.objects.filter(email=email)
                    for i in user:
                        request.session['user_id'] = i.id
                    email_template_context = {
                        'password': password,
                    }
                    send_html_email([email, ], 'Your password for online shopping', 'email.html', email_template_context, "info@gmail.com")
                    return redirect('/login_step2/')
                else:
                    flag_register = 3
        if request.POST.get('register_submit'):
            #### register form
            if register_form.is_valid():
                name = register_form.cleaned_data.get("name")
                email = register_form.cleaned_data.get("email")
                mobile = register_form.cleaned_data.get("mobile")
                address = register_form.cleaned_data.get("address")
                postal_code = register_form.cleaned_data.get("postal_code")
                user_exist = User.objects.filter(email=email, name=name).count()
                if user_exist == 0:
                    user = User(name=name, email=email, mobile=mobile, address=address, postal_code=postal_code)
                    user.save()
                    flag_register = 1
                else:
                    flag_register = 2
    context = {
        'login_form': login_form,
        'register_form': register_form,
        'flag': flag_register,
    }
    return render(request, 'login.html', context)

def login_step2(request):
    if 'password' in request.session.keys():
        if request.session['password']:
            form = LoginStep2Form(request.POST or None)
            flag = 0
            if request.method == 'POST':
                if form.is_valid():
                    password = form.cleaned_data.get('password')
                    sent_pass = request.session['password']
                    if password == sent_pass:
                        del request.session['password']
                        cart_non_user = Cart_non_user.objects.filter(ip_address=get_client_ip(request))
                        user = User.objects.get(id=request.session['user_id'])
                        for i in cart_non_user:
                            cart_exist = Cart_user.objects.filter(user_id=request.session['user_id'], product_id=i.product_id).count()
                            if cart_exist == 0:
                                cart = Cart_user(user_id=user, product_id=i.product_id, count=i.count, payed=0, send_status=0, date=datetime.now().strftime('%Y-%m-%d'))
                                cart.save()
                            Cart_non_user.objects.filter(ip_address=get_client_ip(request), id=i.id).delete()
                        user = User.objects.filter(id=request.session['user_id'])
                        for i in user:
                            request.session['email'] = i.email
                        del request.session['user_id']
                        return redirect('/')
                    else:
                        flag = 1
            context = {
                'flag': flag,
                'form': form,
            }
            return render(request, 'login_step2.html', context)
    else:
        return redirect('/login/')
    return redirect('/login/')

def logout(request):
    if 'email' in request.session.keys():
        if request.session['email']:
            del request.session['email']
            return redirect('/')
    else:
        return redirect('/')

def contact(request):
    if 'email' in request.session.keys():
        if request.session['email']:
            global name, email, user_id, flag
            flag = 0
            user = User.objects.filter(email=request.session['email'])
            for i in user:
                user_id = i.id
                name = i.name
                email = i.email
            form = ContactForm(request.POST or None, initial={'name': name, 'email': email})
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('name')
                    email = form.cleaned_data.get('email')
                    subject = form.cleaned_data.get('subject')
                    message = form.cleaned_data.get('message')
                    date = datetime.now().strftime('%Y-%m-%d')
                    contact = Contact(name=name, email=email, subject=subject, message=message, date=date, status=0, id_ip=user_id)
                    contact.save()
                    flag = 1
            context = {
                'form': form,
                'flag': flag,
            }
            return render(request, 'contact.html', context)
    else:
        flag = 0
        form = ContactForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                subject = form.cleaned_data.get('subject')
                message = form.cleaned_data.get('message')
                date = datetime.now().strftime('%Y-%m-%d')
                contact = Contact(name=name, email=email, subject=subject, message=message, date=date, status=0, id_ip=get_client_ip(request))
                contact.save()
                flag = 1
        context = {
            'form': form,
            'flag': flag,
        }
        return render(request, 'contact.html', context)

def place_order(request):
    return render(request, 'thankyou.html', {})


###############SEARCH FORMS
def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        product_count = Product.objects.filter(Q(name__contains=search) | Q(desc__contains=search)).count()
        per_page = 9
        count_page = int(product_count / per_page) + 1
        product = Product.objects.filter(Q(name__contains=search) | Q(desc__contains=search))[:per_page]
        a = []
        for i in product:
            b = []
            b.append(i.name)
            b.append(i.image)
            b.append(i.desc)
            b.append(get_price(i.id))
            a.append(b)
        cat = Category.objects.filter(submenu_id=0)
        context = {
            'search': search,
            'product': a,
            'cat': cat,
            'count_page': range(count_page),
        }
        return render(request, 'search.html', context)
    else:
        return redirect('/')
    return redirect('/')

def search_page(request, page):
    if request.method == 'POST':
        search = request.POST.get('search')
        product_count = Product.objects.filter(Q(name__contains=search) | Q(desc__contains=search)).count()
        per_page = 9
        count_page = int(product_count / per_page) + 1
        start_page = (page - 1) * per_page
        product = Product.objects.filter(Q(name__contains=search) | Q(desc__contains=search))[start_page:per_page]
        a = []
        for i in product:
            b = []
            b.append(i.name)
            b.append(i.image)
            b.append(i.desc)
            b.append(get_price(i.id))
            a.append(b)
        cat = Category.objects.filter(submenu_id=0)
        context = {
            'search': search,
            'product': a,
            'cat': cat,
            'count_page': range(count_page),
        }
        return render(request, 'search.html', context)
    else:
        return redirect('/')
    return redirect('/')

###############CART FORMS
def add_to_cart(request, id):
    if request.method == 'POST':
        if 'email' in request.session.keys():
            if request.session['email']:
                product_count = Product.objects.filter(Q(id=id) & ~Q(count=0) & Q(status=1)).count()
                if product_count != 0:
                    user = User.objects.get(email=request.session['email'])
                    cart_exist = Cart_user.objects.filter(user_id=user, product_id=id).count()
                    count = int(request.POST.get('count'))
                    if cart_exist == 0:
                        date = datetime.now().strftime('%Y-%m-%d')
                        cart = Cart_user(user_id=user, product_id=id, count=count, payed=0, send_status=0, date=date)
                        cart.save()
                        return redirect('/cart/')
                    else:
                        cart = Cart_user.objects.filter(user_id=user, product_id=id)
                        for i in cart:
                            old_count = i.count
                            Cart_user.objects.filter(user_id=user, product_id=id).update(count=old_count+count)
                            return redirect('/cart/')
                        return redirect('/cart/')
                else:
                    return redirect('/')
        else:
            product_count = Product.objects.filter(Q(id=id) & ~Q(count=0) & Q(status=1)).count()
            if product_count != 0:
                ip = get_client_ip(request)
                cart_exist = Cart_non_user.objects.filter(ip_address=ip, product_id=id).count()
                count = int(request.POST.get('count'))
                if cart_exist == 0:
                    date = datetime.now().strftime('%Y-%m-%d')
                    cart = Cart_non_user(ip_address=ip, product_id=id, count=count, date=date)
                    cart.save()
                    return redirect('/cart/')
                else:
                    cart = Cart_non_user.objects.filter(ip_address=ip, product_id=id)
                    for i in cart:
                        old_count = i.count
                        Cart_non_user.objects.filter(ip_address=ip, product_id=id).update(count=old_count + count)
                        return redirect('/cart/')
                    return redirect('/cart/')
            else:
                return redirect('/')
    else:
        return redirect('/')

def update_cart(request, id):
    if request.method == 'POST':
        if 'email' in request.session.keys():
            user = User.objects.filter(email=request.session['email'])
            for i in user:
                user_id = i.id
            cart_exist = Cart_user.objects.filter(user_id=user_id, product_id=id).count()
            if cart_exist != 0:
                cart = Cart_user.objects.filter(user_id=user_id, product_id=id)
                for i in cart:
                    old_count = i.count
                count = int(request.POST.get('count'))
                if count > old_count:
                    a = count - old_count
                    new_count = old_count + a
                    Cart_user.objects.filter(user_id=user_id, product_id=id).update(count=new_count)
                    return redirect('/cart/')
                else:
                    a = old_count - count
                    new_count = old_count - a
                    Cart_user.objects.filter(user_id=user_id, product_id=id).update(count=new_count)
                    return redirect('/cart/')
            else:
                return redirect('/')
        else:
            ip = get_client_ip(request)
            cart_exist = Cart_non_user.objects.filter(ip_address=ip, product_id=id).count()
            if cart_exist != 0:
                cart = Cart_non_user.objects.filter(ip_address=ip, product_id=id)
                for i in cart:
                    old_count = i.count
                count = int(request.POST.get('count'))
                if count > old_count:
                    a = count - old_count
                    new_count = old_count + a
                    Cart_non_user.objects.filter(ip_address=ip, product_id=id).update(count=new_count)
                    return redirect('/cart/')
                else:
                    a = old_count - count
                    new_count = old_count - a
                    Cart_non_user.objects.filter(ip_address=ip, product_id=id).update(count=new_count)
                    return redirect('/cart/')
            else:
                return redirect('/')
    else:
        return redirect('/')

def remove_cart(request, id):
    if 'email' in request.session.keys():
        if request.session['email']:
            user = User.objects.filter(email=request.session['email'])
            for i in user:
                user_id = i.id
            cart_exist = Cart_user.objects.filter(product_id=id, user_id=user_id).count()
            if cart_exist != 0:
                Cart_user.objects.filter(product_id=id, user_id=user_id).delete()
                return redirect('/cart/')
            else:
                return redirect('/cart/')
    else:
        ip = get_client_ip(request)
        cart_exist = Cart_non_user.objects.filter(ip_address=ip, product_id=id).count()
        if cart_exist != 0:
            Cart_non_user.objects.filter(ip_address=ip, product_id=id).delete()
            return redirect('/cart/')
        else:
            return redirect('/cart/')