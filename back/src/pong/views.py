from django.views.decorators.http import require_GET
from django.http import JsonResponse

from . import rooms

# Create your views here.


@require_GET
def get_rooms(_):
    return JsonResponse(rooms.Rooms.get_rooms(), safe=False)
