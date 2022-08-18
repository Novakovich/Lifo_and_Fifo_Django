from django.db import transaction
from django.shortcuts import render
from donation.models import Donate, Office, Request, Item


def home_page(request):
    state = Office.objects.order_by('office_count').last()
    if state.office_count is None:
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
    context = {
        'data': [],
        'data_request': []
               }
    donate = Donate.objects.all()
    req = Item.objects.all()
    context['data'] = donate
    context['data_request'] = req
    return render(request, 'list.html', context)


@transaction.atomic
def correct_request(request):
    req = Request.objects.order_by('id').last()
    number_req = range(req.request_amount)
    for i in number_req:
        Item.objects.create(
            name_item=request.POST[f'name{i}'],
            amount_item=request.POST[f'amount{i}'],
            office_id=request.session["office"],
            request_hash_id=req.id
        )
    return render(request, 'correct_request.html')
