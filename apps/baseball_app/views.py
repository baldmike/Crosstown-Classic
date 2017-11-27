from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import strftime, localtime
from django.core.urlresolvers import reverse
import random

from models import *

def index(request):

    if 'curr_inn' not in request.session:
        request.session['curr_inn'] = 0

    if 'outcome' not in request.session:
        request.session['outcome'] = ['It\'s a beautiful 78 degrees and the sun is shining!', 'Here we go, folks, Play Ball!']
        
    if 'side' not in request.session:
        request.session['side'] = 'top'
    if request.session['curr_inn'] % 2 == 0:
        request.session['side'] = 'bottom'
    if request.session['curr_inn'] % 2 != 0:
        request.session['side'] = 'top'

    if 'home_order' not in request.session:
        request.session['home_order'] = 8
        
    if 'away_order' not in request.session:
        request.session['away_order'] = 0
    
    home_team = Player.objects.filter(team="Home")
    home_order = request.session['home_order']
    away_team = Player.objects.filter(team="Away")
    away_order = request.session['away_order']

    if request.session['curr_inn'] % 2 == 0:
        team_at_bat = away_team
        counter = away_order
    else: 
        team_at_bat = home_team
        counter = home_order

    if 'batter' not in request.session:
        request.session['batter'] = team_at_bat[counter].first_name + " " + team_at_bat[counter].last_name
    
    if 'inning' not in request.session:
        request.session['inning'] = "Top of the first"
    if request.session['curr_inn'] == 1:
        request.session['inning'] = "Bottom of the first"
    if request.session['curr_inn'] == 2:
        request.session['inning'] = "Top of the second"
    if request.session['curr_inn'] == 3:
        request.session['inning'] = "Bottom of the second"
    if request.session['curr_inn'] == 4:
        request.session['inning'] = "Top of the third"
    if request.session['curr_inn'] == 5:
        request.session['inning'] = "Bottom of the third"
    if request.session['curr_inn'] == 6:
        request.session['inning'] = "Top of the fourth"
    if request.session['curr_inn'] == 7:
        request.session['inning'] = "Bottom of the fourth"
    if request.session['curr_inn'] == 8:
        request.session['inning'] = "Top of the fifth"
    if request.session['curr_inn'] == 9:
        request.session['inning'] = "Bottom of the fifth"
    if request.session['curr_inn'] == 10:
        request.session['inning'] = "Top of the sixth"
    if request.session['curr_inn'] == 11:
        request.session['inning'] = "Bottom of the sixth"
    if request.session['curr_inn'] == 12:
        request.session['inning'] = "Top of the seventh"
    if request.session['curr_inn'] == 13:
        request.session['inning'] = "Bottom of the seventh"
    if request.session['curr_inn'] == 14:
        request.session['inning'] = "Top of the eighth"
    if request.session['curr_inn'] == 15:
        request.session['inning'] = "Bottom of the eighth"
    if request.session['curr_inn'] == 16:
        request.session['inning'] = "Top of the ninth"
    if request.session['curr_inn'] == 17:
        request.session['inning'] = "Bottom of the ninth"

    if 'ball' not in request.session:
        request.session['ball'] = 0
    if 'strike' not in request.session:
        request.session['strike'] = 0
    if 'out' not in request.session:
        request.session['out'] = 0

    if 'box_score' not in request.session:
        request.session['box_score'] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if 'visitor_score' not in request.session:
        request.session['visitor_score'] = 0
    if 'home_score' not in request.session:
        request.session['home_score'] = 0
          
    if 'first' not in request.session:
        request.session['first'] = False
    if 'second' not in request.session:
        request.session['second'] = False
    if 'third' not in request.session:
        request.session['third'] = False

    print"BOX SCORE OF ZERO: " + str(request.session['box_score'][0])
    print "CURRENT INNING: " + str(request.session['curr_inn'])

    context = {
        'inning': range(1,10)
    }

    return render(request, 'baseball_app/index.html', context)


def watch(request):
    i = request.session['curr_inn']
    rand = random.randint(1, 100)
    print "************************************* RANDOM NUMBER: " + str(rand)
    if rand <= 60:
        request.session['strike'] += 1
        outcome = request.session['outcome'] 
        outcome.insert(0, "Strike " + str(request.session['strike']))
        if request.session['strike'] == 3:
            outcome = request.session['outcome'] 
            outcome.insert(0, "Steeee - rike THREE!!")
            request.session['strike'] = 0
            request.session['ball'] = 0
            request.session['out'] += 1
            if request.session['out'] == 3:
                if request.session['curr_inn'] == 17:
                    print "THIS SHOULD HIT AT END OF 9th **************************&&&&&&&&&&&&&&&&&&&&"
                    return redirect('/game_over')
                end_of_inning(request)
        return redirect('/')
    elif rand > 60 and rand < 99:
        request.session['ball'] += 1
        outcome = request.session['outcome'] 
        outcome.insert(0, "Ball " + str(request.session['ball']))
        if request.session['ball'] == 4:
            reset_at_bat(request)
            outcome = request.session['outcome'] 
            outcome.insert(0, "Ball Four, Take your base.")
            if request.session['third'] and request.session['second'] and request.session['third']:
                score(request)
                return redirect('/')
            if request.session['second'] and request.session['first']:
                request.session['third'] = True
            if request.session['first']:
                request.session['second'] = True
            request.session['first'] = True
        return redirect('/')
    else:
        outcome = request.session['outcome'] 
        outcome.insert(0, "HIT BY PITCH, take your base")
        request.session['ball'] = 0
        request.session['strike'] = 0
        if request.session['third'] and request.session['second'] and request.session['third']:
            request.session['box_score'][i] += 1
            if request.session['curr_inn'] % 2 == 0:
                request.session['visitor_score'] += 1
            return redirect('/')
        if request.session['second'] and request.session['first']:
            request.session['third'] = True
        if request.session['first']:
            request.session['second'] = True
        request.session['first'] = True
        return redirect('/')


def swing(request):
    rand = random.randint(1,100)
    print "********** RANDOM NUMBER: " + str(rand)
    i = request.session['curr_inn']
    
    if rand < 20:
        request.session['strike'] += 1
        outcome = request.session['outcome'] 
        outcome.insert(0, "Strike " + str(request.session['strike']) + "!")
        if request.session['strike'] == 3:
            
            outcome = request.session['outcome'] 
            outcome.insert(0, "Strike out swinging!")
            request.session['out'] += 1
                       
            if request.session['out'] == 3:
                if request.session['curr_inn'] == 17:
                    return redirect('/game_over')
                end_of_inning(request)

            reset_at_bat(request)

        return redirect('/')
    
    elif rand >= 20 and rand <=75:
        hit = ['Ground Out!', 'Fly Out!', 'Line Out!', 'Foul Ball!']
        x = random.randint(0,3)
        this_hit = hit[x]
        print this_hit
        
        if this_hit == 'Ground Out!':
            outcome = request.session['outcome']
            outcome.insert(0, this_hit)
            request.session['out'] += 1
            if request.session['out'] == 3:
                if request.session['curr_inn'] == 17:
                    return redirect('/game_over')
                end_of_inning(request)
            
            reset_at_bat(request)
            return redirect('/')

        if this_hit == 'Fly Out!':
            outcome = request.session['outcome'] 
            outcome.insert(0, this_hit)
            request.session['out'] += 1
            if request.session['out'] == 3:
                if request.session['curr_inn'] == 17:
                    return redirect('/game_over')
                end_of_inning(request)
            if request.session['first'] == False and request.session['second'] == False and request.session['third']:
                if request.session['out'] < 3:
                    score(request)
            reset_at_bat(request)
            return redirect('/')
        
        if this_hit == 'Line Out!':
            outcome = request.session['outcome'] 
            outcome.insert(0, this_hit)
            request.session['out'] += 1
            if request.session['out'] == 3:
                if request.session['curr_inn'] == 17:
                    return redirect('/game_over')
                end_of_inning(request)
            if request.session['third']:
                if request.session['out'] < 3:
                    request.session['box_score'][i] += 1
            reset_at_bat(request)
            return redirect('/')

        if this_hit == 'Foul Ball!':
            outcome = request.session['outcome']
            outcome.insert(0, this_hit)
            print "FOUL BALL*********"
            if request.session['strike'] < 2:
                request.session['strike'] += 1
            return redirect('/')
            

    elif rand > 75 and rand < 92:

        hit = ['Single!', 'Double!']
        x = random.randint(0,1)
        this_hit = hit[0]
        print"this_hit is a: " + this_hit

        if this_hit == 'Single!':
            
            if request.session['first'] == False and request.session['second'] == False and request.session['third'] == False:
                # BASES EMPTY
                request.session['first'] = True
                on_base = "Runner on first"
                print "after on_base"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')

            if request.session['first'] and request.session['second'] == False and request.session['third'] == False:
                # MAN ON FIRST
                request.session['second'] = True
                on_base = "Runners on first and second"
                finish_at_bat(request, on_base, this_hit)
                # return redirect('/')
            
            if request.session['first'] == False and request.session['second'] and request.session['third'] == False:
                # MAN ON SECOND
                request.session['first'] = True
                request.session['second'] = False
                request.session['third'] = True
                on_base = "Runners on first and third"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')

            if request.session['first'] == False and request.session['second'] == False and request.session['third']:
                #MAN ON THIRD
                request.session['first'] = True
                request.session['third'] = False
                score(request)
                on_base = "Run scores!  Runner on first"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
            
            if  request.session['first'] and request.session['second'] and request.session['third'] == False:
                # FIRST AND SECOND
                request.session['third'] = True
                on_base = "Bases loaded!"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                        
            if request.session['first'] and request.session['second'] == False and request.session['third']:
                # FIRST AND THIRD
                request.session['second'] = True
                request.session['third'] = False
                score(request)
                on_base = "One run scores!  Runners on first and second"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
            
            if request.session['first'] == False and request.session['second'] and request.session['third']:
                # SECOND AND THIRD
                request.session['first'] = True
                request.session['second'] = False
                request.session['third'] = True
                on_base = "Runners on first and third"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] and request.session['second'] and request.session['third']:
                # BASES LOADED
                score(request)
                on_base = "A run scores, bags still packed!"
                finish_at_bat(request, on_base, this_hit)
                print "BASES LOADED SINGLE, AFTER finish_at_bat THIS IS LINE 309"
                return redirect('/')

        if this_hit == 'Double!':
            
            if request.session['first'] == False and request.session['second'] == False and request.session['third'] == False:
                # BASES EMPTY
                request.session['second'] = True
                on_base = "Runner on second"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] and request.session['second'] == False and request.session['third'] == False:
                # MAN ON FIRST
                request.session['first'] = False
                request.session['second'] = True
                request.session['third'] = True
                on_base = "Runners on second and third"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] == False and request.session['second'] and request.session['third'] == False:
                # MAN ON SECOND
                score(request)
                request.session['second'] = True
                on_base = "The runner scores, man on second"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] == False and request.session['second'] == False and request.session['third']:
                # MAN ON THIRD
                request.session['third'] = False
                request.session['second'] = True
                score(request)
                on_base = "One run in, runner on second"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] and request.session['second'] and request.session['third'] == False:
                # FIRST AND SECOND
                request.session['first'] = False
                request.session['second'] = True
                score(request)
                request.session['third'] = True
                on_base = "A run scores - runners on second and third"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] and request.session['second'] == False and request.session['third']:
                # FIRST AND THIRD
                request.session['first'] = False
                request.session['second'] = True
                request.session['third'] = True
                score(request)
                on_base = "One run scores, runners on second and third."
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] == False and request.session['second'] and request.session['third']:
                # SECOND AND THIRD
                request.session['second'] = True
                request.session['third'] = False
                score(request)
                score(request)
                on_base = "Both runners score! Runner on second"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] and request.session['second'] and request.session['third']:
                # BASES LOADED
                request.session['first'] = False
                request.session['second'] = True
                score(request)
                score(request)
                on_base = "Two runs score! Runners on second and third"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
            

    elif rand > 91 and rand < 100:
        hit = ['Triple!', 'Home Run!']
        x = random.randint(0,1)
        this_hit = hit[1]
        print this_hit

        if this_hit == 'Triple!':
            if request.session['first'] == False and request.session['second'] == False and request.session['third'] == False:
                request.session['third'] = True
                on_base = "Runner on Third."
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')

            if request.session['first'] and request.session['second'] == False and request.session['third'] == False:
                request.session['first'] = False
                request.session['third'] = True
                score(request)
                on_base = "The runner scores! Man on third."
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] == False and request.session['second'] and request.session['third'] == False:
                request.session['second'] = False
                request.session['third'] = True
                score(request)
                on_base = "One run scores, runner on Third."
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')

            if request.session['first'] == False and request.session['second'] == False and request.session['third']:
                score(request)
                on_base = "One run in, runner on Third!"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')

            if request.session['first'] and request.session['second'] and request.session['third'] == False:  
                request.session['first'] = False
                request.session['second'] = False
                request.session['third'] = True
                score(request)
                score(request)
                on_base = "Two runs score, man on third."
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')

            if request.session['first'] and request.session['second'] == False and request.session['third']:  
                request.session['first'] = False
                score(request)
                score(request)
                on_base = "The two runners score, man on third"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')

            if request.session['first'] == False and request.session['second'] and request.session['third']:  
                request.session['first'] = False
                score(request)
                score(request)
                on_base = "Two runs in, runner on third."
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')

            if request.session['first'] and request.session['second'] and request.session['third']:
                request.session['first'] = False
                request.session['second'] = False
                score(request)
                score(request)
                score(request)
                on_base = "He clears the bags and lands on third"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')

            

        if this_hit == 'Home Run!':
            if request.session['first'] == False and request.session['second'] == False and request.session['third'] == False:
                # BASES EMPTY
                score(request)
                on_base = "Solo shot onto the Dan Ryan!"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] and request.session['second'] == False and request.session['third'] == False:
                # MAN ON FIRST
                request.session['first'] = False
                score(request)
                score(request)
                on_base = "You can put it on the board....  YES! Two run ding dong!"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] == False and request.session['second'] and request.session['third'] == False:
                # MAN ON SECOND
                request.session['second'] = False
                score(request)
                score(request)
                on_base = "He goes yard! It's a two run shot!"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] == False and request.session['second'] == False and request.session['third']:
                # MAN ON THIRD
                request.session['third'] = False
                score(request)
                score(request)
                on_base = "He goes yard! It's a two run shot!"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] and request.session['second'] and request.session['third'] == False:
                # FIRST AND SECOND
                request.session['first'] = False
                request.session['second'] = False
                score(request)
                score(request)
                score(request)
                on_base = "That ball's on 35th!  A 3 run shot!"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] and request.session['second'] == False and request.session['third']:
                # FIRST AND THIRD
                request.session['first'] = False
                request.session['third'] = False
                score(request)
                score(request)
                score(request)
                on_base = "It's OUTTA HERE!!  A 3 run shot!"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] == False and request.session['second'] and request.session['third']:
                # SECOND AND THIRD
                request.session['second'] = False
                request.session['third'] = False
                score(request)
                score(request)
                score(request)
                on_base = "It's OUTTA HERE!!  A 3 run shot!"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')
                
            if request.session['first'] and request.session['second'] and request.session['third']:
                # BASES LOADED
                request.session['first'] = False
                request.session['second'] = False
                request.session['third'] = False
                score(request)
                score(request)
                score(request)
                score(request)
                on_base = "GRAND SLAM!!!"
                finish_at_bat(request, on_base, this_hit)
                return redirect('/')

    elif rand == 100:
        print "**************HIT BY PITCH, BITCH*******************"
        this_hit = 'Hit By Pitch!'
        i = request.session['curr_inn']
    
        if request.session['first'] and request.session['second'] == False and request.session['third'] == False:
            request.session['second'] = True
            on_base = "Hit by pitch, runners on first and second."
            finish_at_bat(request, on_base, this_hit)
            return redirect('/')
        
        if request.session['first'] and request.session['second'] and request.session['third'] == False:
            request.session['third'] = True
            on_base = "Hit by pitch! That fills the bases."
            finish_at_bat(request, on_base, this_hit)
            return redirect('/')

        if request.session['third'] and request.session['second'] and request.session['third']:
            score(request)
            on_base = "Hit by pitch! That walks in a run, bases still loaded."
            finish_at_bat(request, on_base, this_hit)
            return redirect('/')

        request.session['first'] = True
        on_base = "Hit by pitch, take your base."
        finish_at_bat(request, on_base, this_hit)
        return redirect('/')

def reset_at_bat(request):

    print "RESET AT BAT **********RESET AT BAT FUNCTION*************************"
    home_team = Player.objects.filter(team="Home")
    home_order = request.session['home_order']
    away_team = Player.objects.filter(team="Away")
    away_order = request.session['away_order']  

    if request.session['curr_inn'] % 2 == 0:
        team_at_bat = away_team
        if request.session['away_order'] == 8:
            request.session['away_order'] = 0
        else:
            request.session['away_order'] += 1
        counter = request.session['away_order']

    else:
        team_at_bat = home_team
        if request.session['home_order'] == 8:
            request.session['home_order'] = 0
        else:
            request.session['home_order'] += 1
        counter = request.session['home_order']

    request.session['ball'] = 0
    request.session['strike'] = 0
      

    request.session['batter'] = team_at_bat[counter].first_name + " " + team_at_bat[counter].last_name
    print request.session['batter'] + "*******************************************************"
    print "CURRENT INNING - RESET_AT_BAT: " + str(request.session['curr_inn'])

def end_of_inning(request):

    home_team = Player.objects.filter(team="Home")
    home_order = request.session['home_order']
    away_team = Player.objects.filter(team="Away")
    away_order = request.session['away_order']

    if request.session['curr_inn'] % 2 == 0:
        team_at_bat = away_team
        counter = away_order
    else: 
        team_at_bat = home_team
        counter = home_order

    request.session['batter'] = team_at_bat[counter].first_name + " " + team_at_bat[counter].last_name
    
    outcome = request.session['outcome'] 
    outcome.insert(0, "END OF INNING")
    request.session['ball'] = 0
    request.session['strike'] = 0
    request.session['out'] = 0
    
    request.session['first'] = False
    request.session['second'] = False
    request.session['third'] = False

    request.session['curr_inn'] += 1

    return redirect('/')

def reset(request):
    request.session.flush()

    return redirect('/')

def finish_at_bat(request, on_base, this_hit):
    outcome = request.session['outcome'] 
    outcome.insert(0, this_hit)

    baserunners = request.session['outcome']
    baserunners.insert(0, on_base)

    reset_at_bat(request)
    return redirect('/')

def score(request):
    i = request.session['curr_inn']
    request.session['box_score'][i] += 1
    if request.session['curr_inn'] % 2 == 0:
        request.session['visitor_score'] += 1
    else:
        request.session['home_score'] += 1

def game_over(request):
    print "this is the GAME OVER FUNCTION"
    request.session.flush()

    return render(request, 'baseball_app/game_over.html')

    