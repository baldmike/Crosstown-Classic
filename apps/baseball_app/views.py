from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import strftime, localtime
from django.core.urlresolvers import reverse
import random

from models import *

def index(request):

    if 'activities' not in request.session:
        request.session['activities'] = []
    if 'curr_inn' not in request.session:
        request.session['curr_inn'] = 0
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



    if 'ball' not in request.session:
        request.session['ball'] = 0
    if 'strike' not in request.session:
        request.session['strike'] = 0
    if 'out' not in request.session:
        request.session['out'] = 0

    if 'box_score' not in request.session:
        request.session['box_score'] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    print"BOX SCORE OF ZERO: " + str(request.session['box_score'][0])

    print "CURRENT INNING: " + str(request.session['curr_inn'])

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

    return render(request, 'baseball_app/index.html')


def watch(request):
    i = request.session['curr_inn']
    rand = random.randint(1,100)
    if rand <= 10:
        request.session['strike'] += 1
        activities = request.session['activities'] 
        activities.insert(0, "STRIKE " + str(request.session['strike']))
        if request.session['strike'] == 3:
            activities = request.session['activities'] 
            activities.insert(0, "***** STRIKE OUT!! *****")
            request.session['strike'] = 0
            request.session['ball'] = 0
            request.session['out'] += 1
            if request.session['out'] == 3:
                activities = request.session['activities'] 
                activities.insert(0, "*****  INNING'S OVER! ***** ")
                end_of_inning(request)
        return redirect('/')
    else:
        request.session['ball'] += 1
        activities = request.session['activities'] 
        activities.insert(0, "BALL " + str(request.session['ball']))
        if request.session['ball'] == 4:
            request.session['ball'] = 0
            request.session['strike'] = 0
            activities = request.session['activities'] 
            activities.insert(0, "*****  Ball Four, Take your base. ***** ")
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
    rand = random.randint(0,100)
    if rand < 20:
        request.session['strike'] += 1
        if request.session['strike'] == 3:
            print "STRIKE OUT SWINGING!"
            request.session['out'] += 1
            request.session['strike'] = 0
            request.session['ball'] = 0
        return redirect('/')
    else:

        hit = ['single', 'double', 'triple', 'Home Run!', 'ground out', 'fly out', 'foul ball', 'hit by pitch']
        x = random.randint(0,7)
        this_hit = hit[0]
        print this_hit
        i = request.session['curr_inn']
        print "THE CURRENT INNING IS: " + str(i)

        if this_hit == 'single':
            request.session['first'] = True
            if request.session['first']:
                request.session['second'] = True
            if request.session['third']:
                request.session['third'] = False
                request.session['box_score'][i] += 1
                if request.session['curr_inn'] % 2 == 0:
                    request.session['visitor_score'] += 1
                else:
                    request.session['home_score'] += 1
                    request.session['first'] = False
            activities = request.session['activities']
            activities.insert(0, this_hit)
            return redirect('/')

        if this_hit == 'double':
            if request.session['first']:
                request.session['first'] = False
                request.session['third'] = True
            if request.session['second']:
                request.session['box_score'][i] += 1
                if request.session['curr_inn'] % 2 == 0:
                    request.session['visitor_score'] += 1
                else:
                    request.session['home_score'] += 1
                    request.session['first'] = False
            if request.session['third']:
                request.session['box_score'][i] += 1
                request.session['third'] = False
            request.session['second'] = True
            activities = request.session['activities'] 
            activities.insert(0, this_hit)
            return redirect('/')

        if this_hit == 'triple':
            if request.session['first']:
                request.session['box_score'][i] += 1
                if request.session['curr_inn'] % 2 == 0:
                    request.session['visitor_score'] += 1
                else:
                    request.session['home_score'] += 1
                    request.session['first'] = False
                request.session['first'] = False
            if request.session['second']:
                request.session['box_score'][i] += 1
                if request.session['curr_inn'] % 2 == 0:
                    request.session['visitor_score'] += 1
                else:
                    request.session['home_score'] += 1
                    request.session['first'] = False
                request.session['second'] = False
            if request.session['third']:
                request.session['box_score'][i] += 1
                if request.session['curr_inn'] % 2 == 0:
                    request.session['visitor_score'] += 1
                else:
                    request.session['home_score'] += 1
                    request.session['first'] = False
            request.session['third'] = True
            activities = request.session['activities'] 
            activities.insert(0, this_hit)
            return redirect('/')

        if this_hit == 'Home Run!':
            if request.session['first']:
                request.session['box_score'][i] += 1
                if request.session['curr_inn'] % 2 == 0:
                    request.session['visitor_score'] += 1
                else:
                    request.session['home_score'] += 1
                    request.session['first'] = False
            
            if request.session['second']:
                request.session['box_score'][i] += 1
                if request.session['curr_inn'] % 2 == 0:
                    request.session['visitor_score'] += 1
                else:
                    request.session['home_score'] += 1
                    request.session['first'] = False
                request.session['second'] = False
            
            if request.session['third']:
                request.session['box_score'][i] += 1
                if request.session['curr_inn'] % 2 == 0:
                    request.session['visitor_score'] += 1
                else:
                    request.session['home_score'] += 1
                    request.session['first'] = False
                request.session['third'] = False
            
            request.session['box_score'][i] += 1
            if request.session['curr_inn'] % 2 == 0:
                    request.session['visitor_score'] += 1
            else:
                request.session['home_score'] += 1
                request.session['first'] = False
            request.session['ball'] = 0
            request.session['strike'] = 0

            if request.session['curr_inn'] % 2 == 0:
                request.session['visitor_score'] += 1
            else:
                request.session['home_score'] += 1
            

            activities = request.session['activities'] 
            activities.insert(0, this_hit)
            return redirect('/')

        if this_hit == 'fly out':
            request.session['out'] += 1
            if request.session['out'] == 3:
                end_of_inning(request)
            print request.session['out']
            if request.session['third']:
                request.session['box_score'][i] += 1
            
            activities = request.session['activities'] 
            activities.insert(0, this_hit)
            return redirect('/')

        if this_hit == 'ground out':
            activities = request.session['activities'] 
            activities.insert(0, this_hit)
            request.session['out'] += 1
            if request.session['out'] == 3:
                end_of_inning(request)
            print "OUT: " + str(request.session['out'])
            if request.session['third']:
                if request.session['out'] < 3:
                    request.session['box_score'][i] += 1
            return redirect('/')

        if this_hit == 'hit by pitch':
            activities = request.session['activities'] 
            activities.insert(0, this_hit)
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




def end_of_inning(request):
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