from django.shortcuts import render
from donation.models import Donate


def home_page(request):
    return render(request, 'main.html')

def donate(request):
    Donate.objects.create(
        name=request.POST["name"],
        amount=request.POST["amount"]
    )
    return render(request, 'donate.html')

def donation(request):
    donate = Donate.objects.order_by('id').first()
    if not donate:
        return render(request, 'no_data.html')
    donate.delete()
    return render(request, 'donation.html', {"donate": donate})

def list(request):
    context = {'data':[]}
    donate = Donate.objects.all()
    context['data'] = donate
    return render(request, 'list.html', context)


