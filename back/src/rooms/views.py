from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import Room  # Import the Room model
from django.shortcuts import get_object_or_404

# Create your views here.

@require_GET
def index(_):
    return JsonResponse({"rooms": "lol"}, safe=False)

@csrf_exempt
def rooms_view(request, *args, **kwargs):
    if request.method == "GET":
        rooms = Room.objects.all()

        # Extract relevant information from each room
        rooms_data = []
        for room in rooms:
            room_info = {
                "id": room.id,
                "name": room.name,
                "player1": room.player1_id,
                "player2": room.player2_id,
                "is_active": room.is_active,
                "created_at": room.created_at,
                "updated_at": room.updated_at,
            }
            rooms_data.append(room_info)

        # Return the list of room information in the JSON response
        return JsonResponse({"rooms": rooms_data}, safe=False)

    elif request.method == "POST":
        try:
            # Assuming the data is sent in JSON format
            data = json.loads(request.body)

            # Extracting data from the request
            name = data.get('name')
            player1_id = data.get('player1')
            player2_id = data.get('player2', None)
            is_active = data.get('is_active', False)

            # Creating a new room
            room = Room.objects.create(
                name=name,
                player1_id=player1_id,
                player2_id=player2_id,
                is_active=is_active
            )

            # Returning the created room data in the JSON response
            return JsonResponse({
                "id": room.id,
                "name": room.name,
                "player1": room.player1_id,
                "player2": room.player2_id,
                "is_active": room.is_active,
                "created_at": room.created_at,
                "updated_at": room.updated_at
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    elif request.method == "DELETE":
        # Retrieve the room_id from URL parameters
        room_id = kwargs.get('room_id')

        if room_id is not None:
            # Use get_object_or_404 to get the room or return a 404 response if not found
            room = get_object_or_404(Room, id=room_id)

            # Delete the room
            room.delete()

            return JsonResponse({"message": "Room deleted successfully"}, status=200)
        else:
            return JsonResponse({"error": "Missing room_id parameter"}, status=400)

    else:
        return JsonResponse({"error": "Unsupported HTTP method"}, status=405)
