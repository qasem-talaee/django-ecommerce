from .models import *
from myshop.form import SearchForm

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def base_template(request):
    auth = 0
    if 'email' in request.session.keys():
        if request.session._session['email']:
            auth = 1
            user = User.objects.filter(email=request.session['email'])
            for i in user:
                user_id = i.id
            cart = Cart_user.objects.filter(user_id=user_id, payed=0).count()
    else:
        auth = 0
        ip = get_client_ip(request)
        cart = Cart_non_user.objects.filter(ip_address=ip).count()
    main_cat = Category.objects.filter(submenu_id=0)
    form = SearchForm(request.POST or None)
    context = {
        'auth': auth,
        'cart_count': cart,
        'main_cat': main_cat,
        'search_form': form,
    }
    return context