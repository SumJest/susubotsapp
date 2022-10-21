import requests
from django.shortcuts import render
from django.http.request import HttpRequest


# Create your views here.

def index(request: HttpRequest):
    if request.method == "GET":
        params = request.GET
        if 'code' in params.keys():
            code = params['code']
            result = requests.get(f"https://oauth.vk.com/access_token?client_id=51451526&client_secret=1RN0PC2PgG9dfwlU3BNB"
                         f"&redirect_url=http://bots.sumjest.ru/accounts/login/"
                         f"&code={code}")
            print(result)
        elif 'error' in params.keys():
            print(params)
        else:
            return render(request, 'login/index.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)

