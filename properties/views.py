from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property


@cache_page(60 * 15)  # Cache for 15 minutes (60 seconds * 15)
def property_list(request):
    properties = Property.objects.all()
    return render(request, "properties/list.html", {"properties": properties})
