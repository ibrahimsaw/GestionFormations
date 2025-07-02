# fichier middleware.py dans une app Django (ex: Utilisateur/middleware.py)
from django.shortcuts import render
from config.globals import *

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return render(request, 'errors/404.html', {'path': request.path,'data':data,}, status=404)
        return response

class Custom500Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 500:
            return render(request, 'errors/500.html', {'path': request.path}, status=404)
        return response
