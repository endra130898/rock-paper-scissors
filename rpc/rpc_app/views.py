from django.shortcuts import render
from django.core import signing
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Flag
import random
import base64

# Create your views here.
def index(request):
    html = 'rpc_app/index.html'
    signer = signing.Signer()
    response = None
    
    if request.method == 'POST' and 'user_data' in request.COOKIES:
        try:
            wins = int(signer.unsign(base64.b64decode(request.COOKIES['user_data'])))

            player_move = request.POST['radio1']
            opponent_move = random.sample(['rock', 'paper', 'scissors'], 1)[0]

            if (player_move == 'rock' and opponent_move == 'scissors') or \
            (player_move == 'paper' and opponent_move == 'rock') or \
            (player_move == 'scissors' and opponent_move == 'paper'):
                wins += 1
            else:
                wins = 0

            if wins >= 999999999:
                wins = Flag.objects.first().flag

            wins = str(wins)

            response = render(request, html, {"wins": wins})
            response.set_cookie('user_data', base64.b64encode(signer.sign(wins).encode()))
        except:
            response = render(request, html, {"hack_attempt": True})

        return response
    else:
        if 'user_data' in request.COOKIES:
            try:
                response = render(request, html, {"wins": signer.unsign(base64.b64decode(request.COOKIES['user_data']))})
            except:
                response = render(request, html, {"hack_attempt": True})
        else:
            response = render(request, html, {"wins" : '0'})
            response.set_cookie('user_data', base64.b64encode(signer.sign('0').encode()))

        return response

@csrf_exempt
def submit_flag_without_admin(request):
    if request.method == 'POST' and len(Flag.objects.all()) == 0:
        flag = Flag(flag = request.POST['flag'])
        flag.save()
        
    return HttpResponseRedirect('/')