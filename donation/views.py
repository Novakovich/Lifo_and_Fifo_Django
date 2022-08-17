from django.db import transaction
from django.shortcuts import render
from donation.models import Donate, Office, Request, Request_item

def home_page(request):
    state = Office.objects.order_by('office_count').last()
    if state.office_count == None:
        office = 0
    else:
        office = state.office_count
    context = {
        "office": Office.objects.all(),
        "disabled": office > state.capacity,
    }
    return render(request, 'main.html', context)

def session_office(request):
    office_id = request.session["office"] = request.POST["office"]
    place = Office.objects.get(id=office_id)
    return render(request, 'main.html', {"place": place})

def request(request):
    Request.objects.create(request_amount=request.POST["request"])
    n = Request.objects.order_by('id').last()
    context = {
        "request": range(n.request_amount),
    }
    return render(request, 'number.html', context)

@transaction.atomic
def donate(request):
    Donate.objects.create(
        name=request.POST["name"],
        amount=request.POST["amount"],
        office_id=request.session["office"],
    )
    return render(request, 'donate.html')

@transaction.atomic
def donation(request):
    donate = Donate.objects.select_for_update().order_by('id').filter(state='Available').first()
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

def correct_request(request):
    req = Request.objects.order_by('id').last()
    number = Request.objects.order_by('request_amount').last()
    number_req = range(number.request_amount)
    for i in number_req:
        Request_item.objects.create(
            name_item=request.POST[f'name{i}'],
            office_id=request.session["office"],
            request_hash_id=req.id
        )
    return render(request, 'correct_request.html')
