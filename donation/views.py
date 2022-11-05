import emoji
from django.contrib import messages, auth
from django.db import transaction, IntegrityError
from django.forms import formset_factory
from django.shortcuts import render, redirect, reverse
from donation.forms import DescribedItem, DescribedItemFormSet, SearchingItem, UserRegisterForm
from donation.models import Donate, Office, Request, DonateItem, RequestItem
from itertools import chain
from donation.tasks import send_mail_func


@transaction.atomic
def home_page(request):
    current_office = request.session.get("office")
    context = {
        "criterion": SearchingItem(),
        "data": [],
        "current_office": current_office,
    }
    donate = DonateItem.objects.all().select_for_update().order_by('-id').filter(state='Available')
    context['data'] = donate
    return render(request, 'main.html', context)


def session_office(request):
    request.session["office"] = request.POST["office"]
    return redirect(reverse('main'))


def request(request):
    if request.POST.get('request'):
        n = Request.objects.create(request_amount=request.POST["request"])
        context = {
            "request": range(int(n.request_amount)),
            "req_id": n.id,
                }
        return render(request, 'number.html', context)
    else:
        n = Donate.objects.create(donate_amount=request.POST["donate"])
        how_many = int(n.donate_amount)
        DescribedItemFormSet = formset_factory(DescribedItem, extra=how_many)
        formset = DescribedItemFormSet()
        context = {
            'form': formset,
                }
        return render(request, 'donate_amount.html', context)


@transaction.atomic
def donation(request):
    donate = DonateItem.objects.select_for_update().order_by('?').filter(state='Available').first()
    if not donate:
        return render(request, 'no_data.html')
    donate.state = 'Booked'
    donate.save()
    context = {
        "donate": donate,
        "luck": '🚀',
    }
    return render(request, 'donation.html', context)


def list(request):
    context = {
        'data': []
            }
    donate = DonateItem.objects.all().order_by('-id')
    req = RequestItem.objects.all().order_by('-id')
    context['data'] = chain(donate, req)

    return render(request, 'list.html', context)


@transaction.atomic
def correct_request(request, req_id):
    req = Request.objects.get(id=req_id)
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
    req = Donate.objects.order_by('-datetime').first()
    if request.method == 'POST':
        formset = DescribedItemFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                new_item = form.save(commit=False)
                new_item.office_id = request.session["office"]
                new_item.donate_uuid = req
                try:
                    with transaction.atomic():
                        new_item.save()
                except IntegrityError:
                    office = Office.objects.all().filter(id=request.session["office"])
                    for i in office:
                        possible = i.capacity - i.office_count
                        context = {
                            'office': office,
                            "possible": possible,
                        }
                        return render(request, "full_storage.html", context)
                form.save_m2m()
        context = {
            "request_hash_id": req,
            "heart": (emoji.emojize(":red_heart:", variant="emoji_type"))
        }
        return render(request, 'donate.html', context)


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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} account created!')
            user_id = user.id
            send_mail_func.delay(user_id)
            return redirect('main')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@transaction.atomic
def request_from_main(request):
    if request.method == 'POST':
        req = request.POST["req"]
        donate = DonateItem.objects.get(id=req)
        donate.state = 'Booked'
        donate.save()
        context = {
            "donate": donate,
            "thumbs_up": (emoji.emojize(":thumbs_up:", variant="emoji_type")),
            "heart": (emoji.emojize(":red_heart:", variant="emoji_type"))
        }
        return render(request, 'request_from_main.html', context)
