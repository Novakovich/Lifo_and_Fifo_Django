from django.db import transaction
from django.forms import formset_factory
from django.shortcuts import render
from donation.forms import DescribedItem, DescribedItemFormSet, SearchingItem
from donation.models import Donate, Office, Request, DonateItem, RequestItem
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
        "criterion": SearchingItem(),
    }
    return render(request, 'main.html', context)


def session_office(request):
    office_id = request.session["office"] = request.POST["office"]
    place = Office.objects.get(id=office_id)
    return render(request, 'main.html', {"place": place})


def request(request):
    if request.POST.get('request'):
        Request.objects.create(request_amount=request.POST["request"])
        n = Request.objects.order_by('-id').first()
        context = {
            "request": range(n.request_amount),
                }
        return render(request, 'number.html', context)
    else:
        Donate.objects.create(donate_amount=request.POST["donate"])
        n = Donate.objects.order_by('-id').first()
        how_many = n.donate_amount
        DescribedItemFormSet = formset_factory(DescribedItem, extra=how_many)
        formset = DescribedItemFormSet()
        context = {
            'form': formset,
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
    req = Request.objects.order_by('-id').first()
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


def described_item(request, **kwargs):
    req = Donate.objects.order_by('-id').first()
    if request.method == 'POST':
        formset = DescribedItemFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                new_item = form.save(commit=False)
                new_item.office_id = request.session["office"]
                new_item.request_hash_id = req.id
                new_item.save()
                form.save_m2m()
        return render(request, 'donate.html')


def criterion(request, **kwargs):
    queryset = DonateItem.objects.all()
    if request.method == 'GET':
        form = SearchingItem(request.GET)
        if form.is_valid():
            get_name = request.GET['name_item']
            get_amount = request.GET['amount_item']
            get_condition = request.GET['condition']
            name = queryset.order_by('name_item').filter(name_item=get_name)
            context = {
                "donate": name,
                "amount": int(get_amount),
                "condition": get_condition,
                     }
            return render(request, 'criterion_list.html', context)
