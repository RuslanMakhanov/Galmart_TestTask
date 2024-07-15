from venv import logger
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
import requests        

session = requests.Session()

def get_auth_token():
    url = 'http://127.0.0.1:8080/api/login'
    credentials = {'username': 'your_username', 'password': 'your_password'}
    response = session.post(url, json=credentials)
    response.raise_for_status()
    token = response.json().get('token')
    return token

def send_order_data(order_id, amount, shop_id, token):
    url = 'http://127.0.0.1:8080/api/order'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'order_id': order_id, 'amount': amount, 'shop_id': shop_id}
    response = session.post(url, json=data, headers=headers)
    try:
        response.raise_for_status()
        print("Data sent successfully")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to send data: {str(e)}")

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        try:
            token = get_auth_token()
            send_order_data(instance.id, instance.amount, instance.shop.id, token)
        except Exception as e:
            # Логируем ошибку для последующего анализа
            logger.error(f"Ошибка при отправке данных: {e}")

        