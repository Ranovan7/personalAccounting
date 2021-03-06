from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from .models import Wallet


class WalletInfo(View):

    def get(self, request, *args, **kwargs):
        '''Managing GET request from the server'''
        username = request.GET.get('u', 'anonymous')
        picked_wallet = Wallet.objects.get(owner__username=username).serialize

        result = {
            'data': picked_wallet,
            'status': 1
        }
        return JsonResponse(result, json_dumps_params={'indent': 2})

    def post(self, request, *args, **kwargs):
        '''Managing POST request from the server'''
        return HttpResponse(f'POST request wallet of id : {request.user.id}')
