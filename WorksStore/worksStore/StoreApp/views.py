from django.http import HttpResponse
from django.shortcuts import render
 
def index(request):
    data = {
        "header": "Нихуя хедер",
        "message": "нихуя месседж"
    }
    return render(request, "home.html", context=data)
 
def about(request):
    return HttpResponse("<h2>О сайте</h2>")
 
def contact(request):
    return HttpResponse("<h2>Контакты</h2>")