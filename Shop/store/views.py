from django.http import Http404, JsonResponse
from django.shortcuts import render
from .models import Order
from .forms import LoginForm
import requests

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            response = requests.post('http://127.0.0.1:8080/api/login', json={'username': username, 'password': password})
            if response.status_code == 200:
                token = response.json().get('token')
                return render(request, 'token.html', {'token': token})
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Login failed'})
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})

def order_detail(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        data = {
            "order_id": order.id,
            "status": order.status,
            "amount": order.amount,
            "shop_id": order.shop.id
        }
        return JsonResponse(data)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")