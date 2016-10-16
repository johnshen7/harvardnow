from flask import Flask, request, redirect
import twilio.twiml
import data
from services import *

app = Flask(__name__)

## the sublist of commands that contain the given tag
def filter(tag,cmds=data.box):
    return [cmd for cmd in cmds if tag in cmd['tags']]

## evaluates a given command to a string by delegating to the proper service
def eval(cmd, input=None):
    s = ""
    if cmd['service'] == 'L': ## Laundry
        return laundry.eval(cmd['args'])
    elif cmd['service'] == 'S': ## Shuttle
        return shuttle.eval(cmd['args'])
    elif cmd['service'] == 'W': ## Weather
        return weather.eval(input)
    elif cmd['service'] == 'H': ## History
        return history.eval(input)
    elif cmd['service'] == 'N': ## National Day
        return nationalday.eval(input)
    else:
        return "ERROR 42: service not recognized"

## list of services that need the user's input to work, not a command
def needsInput(cmd):
    return cmd['service'] in ['W']

def special(incoming):
    body = ''
    if incoming.upper() == "SHUTTLE" :
        body = shuttle.special
    elif incoming.upper() == "LAUNDRY":
        body = laundry.special
    elif incoming.upper() == "WEATHER":
        body = weather.special
    elif incoming.upper() == "HISTORY":
        body = history.special
    elif incoming.upper() == "NATIONALDAY":
        body = nationalday.special
    elif incoming.upper() == "DEMO":
        ## welcome/instructions
        body = 'Thanks for using Harvard Now!\n'
        body += 'Laundry Information is accessed by sending the name of your laundry room\n'
        body += 'e.g. Lowell D\n'
        body += 'For a list of all laundry rooms send laundry\n\n'
        body += 'To access shuttle information send the name of the stop or name of the route\n'
        body += 'e.g. Widener Gate; Quad Yard Express\n'
        body += 'For a list of all shuttle stops and routes send shuttle\n\n'
        body += 'Sending part of a name gives all information associated with that name.\n'
        body += 'For example sending Quad will give information about the shuttle stop Quad and the shuttle'
        body += 'route Quad Yard Express and sending Quincy laundry will give all the laundry rooms in Quincy.\n'
    return body

## main function
@app.route("/", methods=['GET', 'POST'])
def response():
    resp = twilio.twiml.Response()
    incoming = request.values.get('Body',None)

    ## first check if the query is a special case
    body = special(incoming.replace(' ',''))
    if body != '':
        resp.message(body)
        return str(resp)
    ## if not, continue with command filtering
    words = set(incoming.upper().split(" "))
    started = False
    results = data.box
    for word in words:
        r = filter(word,results)
        if r == []:
            continue
        else:
            started = True
            results = r
    if not started:
        body = "Sorry, I don't know what that is."
    elif len(results) > 12:
        body = "Sorry, that's too many requests."
    else:
        if any(needsInput(cmd) for cmd in results):
            body = "\n".join(['\n'+eval(cmd, words) for cmd in results])
        else:
            body = "\n".join(['\n'+eval(cmd) for cmd in results])

    resp.message(body)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
