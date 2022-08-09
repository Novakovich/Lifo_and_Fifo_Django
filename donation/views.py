from django.shortcuts import render, redirect
from donation.models import Donate, Office


def home_page(request):
    state = Office.objects.order_by('office_count').last()
    context = {
        "office": Office.objects.all(),
        "disabled": state.office_count > state.capacity,
    }
    return render(request, 'main.html', context)

def session_office(request):
    office_id = request.session["office"] = request.POST["office"]
    return render(request, 'main.html')

def donate(request):
    Donate.objects.create(
        name=request.POST["name"],
        amount=request.POST["amount"],
        office_id=request.session["office"]
    )
    return render(request, 'donate.html')

def donation(request):
    donate = Donate.objects.order_by('id').filter(state='Available').first()
    if not donate:
        return render(request, 'no_data.html')
    donate.state = 'Booked'
    donate.save()
    return render(request, 'donation.html', {"donate": donate})

def list(request):
    context = {'data': []}
    donate = Donate.objects.all()
    context['data'] = donate
    return render(request, 'list.html', context)

