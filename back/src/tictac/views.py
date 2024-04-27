from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt


import json
import logging

from .models import Game


@csrf_exempt
def home(request):
    response_data = {}
    if not request.user.is_authenticated:
        response_data['error'] = "User not authenticated"
        return (JsonResponse(response_data, encoder=DjangoJSONEncoder))
    logging.debug("estoy en home")
    if request.method == "POST":
        try:
            json_data = request.body.decode('utf-8')
            json_data = json.loads(json_data)
            logging.debug("json_data is %s", json_data)
            username = request.user.username
            option = json_data['option']
            room_code = json_data['room_code']

            if option != 'create':
                game = Game.objects.filter(room_code=room_code).first()

                if game is None:
                    error = "Invalid room code"
                    response_data['error'] = error
                    return (JsonResponse(
                        response_data, encoder=DjangoJSONEncoder))
                if game.is_over:
                    error = "Game is over"
                    response_data['error'] = error
                    return (JsonResponse(
                        response_data, encoder=DjangoJSONEncoder))

                game.opponent = username
                game.save()
                response_data['room_code'] = room_code
                response_data['opponent'] = username
            else:
                game = Game(creator=username, room_code=room_code)
                game.save()
                response_data['room_code'] = room_code
                response_data['creator'] = username
        except Exception as e:
            error = "Invalid data" + str(e)
            response_data['error'] = error
            logging.debug("error is %s", error)
            return (JsonResponse(
                response_data, encoder=DjangoJSONEncoder))
    else:
        error = "Invalid request method"
        response_data['error'] = error
        return (JsonResponse(response_data, encoder=DjangoJSONEncoder))
    logging.debug("home is %s", response_data)
    return (JsonResponse(response_data, encoder=DjangoJSONEncoder))


def play(request, room_code):
    response_data = {}
    if not request.user.is_authenticated:
        response_data['error'] = "User not authenticated"
        return (JsonResponse(response_data, encoder=DjangoJSONEncoder))
    try:
        json_data = request.body.decode('utf-8')
        json_data = json.loads(json_data)
        game = Game.objects.get(room_code=room_code)
        response_data['creator'] = game.creator
        response_data['opponent'] = game.opponent
        response_data['room_code'] = room_code
    except Game.DoesNotExist:
        response_data['error'] = "Game not found"
    except Exception as e:
        error = "Invalid data" + str(e)
        response_data['error'] = error
    return (JsonResponse(response_data, encoder=DjangoJSONEncoder))
