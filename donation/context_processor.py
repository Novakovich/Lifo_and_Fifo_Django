from donation.models import Office


def post_office(request):
    if request.session.get("office"):
        name = Office.objects.get(id=request.session["office"])
    else:
        name = Office.objects.all().first()
    office = name.office_count
    if office is None:
        office = 0
    return {'office': Office.objects.all(), 'name': name, "disabled_office": office >= name.capacity}
