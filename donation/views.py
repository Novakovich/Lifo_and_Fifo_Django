from django.shortcuts import render
import json

from donation.models import Donate


def home_page(request):
    return render(request, 'main.html')

def donate(request):
    with open('datajson.json', 'r', encoding='utf-8') as data:
        data_list = json.load(data)
        data_list.append(
            {"name": request.POST["name"], "amount": request.POST["amount"]}
        )
    with open('datajson.json', 'w') as data:
        json.dump(data_list, data)
    return render(request, 'donate.html')

def donation(request):
    with open('datajson.json', 'r', encoding='utf-8') as data:
        data_list = json.load(data)
    if not data_list:
        return render(request, 'no_data.html')
    context = data_list.pop()
    with open('datajson.json', 'w') as data:
        json.dump(data_list, data)
    return render(request, 'donation.html', {'context': context})

def list(request):
    context = {'datajson':[]}
    donate = Donate.objects.all()
    context['datajson'] = donate

    return render(request, 'list.html', context)


