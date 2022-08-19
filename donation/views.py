from django.db import transaction
from django.shortcuts import render
from donation.models import Donate, Office, Request, DonateItem, RequestItem, Description
from itertools import chain


def home_page(request):
    state = Office.objects.order_by('office_count').last()
    if state.office_count is None:
        office = 0
    else:
        office = state.office_count
    context = {
        "office": Office.objects.all(),
        "disabled": office >= state.capacity,
    }
    return render(request, 'main.html', context)


def session_office(request):
    office_id = request.session["office"] = request.POST["office"]
    place = Office.objects.get(id=office_id)
    return render(request, 'main.html', {"place": place})


def request(request):
    if request.POST.get('request'):
        Request.objects.create(request_amount=request.POST["request"])
        n = Request.objects.order_by('id').last()
        context = {
            "request": range(n.request_amount),
        }
        return render(request, 'number.html', context)
    else:
        Donate.objects.create(donate_amount=request.POST["donate"])
        n = Donate.objects.order_by('id').last()
        context = {
            "request": range(n.donate_amount),
        }
        return render(request, 'donate_amount.html', context)


@transaction.atomic
def donation(request):
    donate = DonateItem.objects.select_for_update().order_by('id').filter(state='Available').first()
    if not donate:
        return render(request, 'no_data.html')
    donate.state = 'Booked'
    donate.save()
    return render(request, 'donation.html', {"donate": donate})


def list(request):
    context = {
        'data': []
               }
    donate = DonateItem.objects.all()
    req = RequestItem.objects.all()
    context['data'] = chain(donate, req)

    return render(request, 'list.html', context)


@transaction.atomic
def correct_request(request):
    req = Request.objects.order_by('id').last()
    number_req = range(req.request_amount)
    available_items = DonateItem.objects.order_by('id').filter(state='Available')
    for i in number_req:
        RequestItem.objects.create(
            name_item=request.POST[f'name{i}'],
            amount_item=request.POST[f'amount{i}'],
            office_id=request.session["office"],
            request_hash_id=req.id,
        )
    request_items = RequestItem.objects.order_by('request_hash').filter(state='Requested')
    context = {
        "donate": available_items,
        "request_items": request_items,
    }
    return render(request, 'correct_request.html', context)


@transaction.atomic
def donate(request):
    req = Donate.objects.order_by('id').last()
    number_req = range(req.donate_amount)
    for n in number_req:
        Description.objects.create(
            name_item=request.POST[f'name{n}'],
            amount_item=request.POST[f'amount{n}'],
            office_id=request.session["office"],
            request_hash_id=req.id,
            details=request.POST[f'details{n}']
        )
    return render(request, 'donate.html')
