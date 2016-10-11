This fork was written by Michael Wornow, Lev Grossman, Luke Sanjer, and Jason Ren.

# HarvardNow #
## What it is ##
HarvardNow is an integrated texting service promoting information accessibility at Harvard. Get real time information about services and facilities, including shuttle schedules, laundry timers, and more (coming soon!). Text "demo" to (617) 658-4667 to try it out!

## How it Works [From the Very Beginning] ##
HarvardNow is a Python Flask App that runs on an HCS server. We use ngrok to create a url that we pass to a Twilio account. When the user texts the number, Twilio passes the text to our backend, where it gets process by `app.py`.

_Python (2)_ - the programming language we're using. A python file ends in `.py` and can be run in the terminal with `python filename.py`. In this case, the server is running `python app.py`.

_Flask_ - a framework that allows us to make an actual app out of `app.py`. When you text HarvardNow, Flask is reason we're able to do something in response, namely call the `response` function in `app.py`. We'll see more details when we look closely at the code.

_HCS server_ - this is where the app gets run from. On this server (in a terminal), we run `python app.py`

_ngrok_ - we run `app.py` on an HCS server, but we need it to be accessible from the outside world in order to call it when you text HarvardNow on your phone. That's where ngrok comes in - it gives us a URL for our server that's accessible from anywhere with an internet connection, which is important to our next point: Twilio

_Twilio_ - connects your texting to our code (which is made accessible with ngrok). When you text HarvardNow, it's Twilio that finds out first. It then passes your text on to the URL we generated with ngrok.

__So, all together now:__

1. You send a text to (617) 658-4667
2. Twilio reads your message and sends the text to a URL generated by ngrok
3. ngrok gives us access to the code (`app.py`) running on the HCS server
4. Flask tells the server to call the `response` function
5. the python code (initially `app.py` and also all the other code that it calls inside that function) does the magic functional stuff and returns the response text you see
6. Twilio gets that message back and displays it as a response message

### What's the Magic Functional Stuff?! ###

First, let's take a look at how services and commands are organized. _Services_ are categories that you might want to get information about, such as 'laundry' and 'shuttle'. A _command_ is a single function call that returns a specific piece of information, for example the status of all dryers in Weld Hall. Each service has its own folder in the `services` subdirectory.

Line 4 of `app.py` says to import everything (denoted as "`*`") from `services`. The `__init__.py` file in `services` tells python that `services` is a package that can be imported, and also specifies what to do when imported. In this case, importing from `services` should also import the `laundry` and `shuttle` subpackages. Each service is represented as a python subpackage in the `services` folder and contains its own `__init__.py` as well as a file named after that service (`laundry.py` for the `laundry` service). That file must contain two things:

* a variable called `special` - this is a special string that should give the user a sense of what they can do with the service (see examples below)
* a function `eval(cmd)` that takes a command (we'll see how exactly we represent a commmand (`cmd`) in python) and returns a string containing the results of that evaluating that command

Everything else in a service (additional functions, helper files, etc.) is just there to satisfy one of these two requirements.

Now let's take another look at commands. A command is represented as a dictionary, meaning it has keys that are mapped to values. Remember that a command is just a function call. We think of a command in this case as an object that contains all the necessary information about its function call. This consists of three things:

1. `service` - a string representing the service this command is going to call
2. `args` - this is another dictionary containing all the arguments the function call will take as parameters. For example, if we want to ask the `laundry` service for the status of all dryers in Weld Hall, we're gonna want to specift that the `roomid` for Weld Hall is 136259, the `machinetype` is "dryer", and the `label` for the command is "WELD HALL Dryers".
3. `tags` - we use tags to uniquely identify a command with keywords. `tags` is a list of these keywords.

We store all the available commands as a list of dictionaries in `data.py` in the root directory.

We're now ready to come back to `app.py`. The `response()` function processes the `incoming` text, checks that it doesn't contain a special keyword (or returns the appropriate special message if it does), determines what command(s) the user wants to run by filtering the master list of commands (`box`) with the words contained in `incoming`, and returns the result of evaluating those filtered commands. Both `special` and `eval` work by delegating to the appropriate service, since we know that every service has a `special` variable and a `eval` function (see code comments for details about the implementation of these functions).

## The Services ##

### Laundry ###

#### special ####
Laundry's special function lists all the laundry rooms available to query. Data about each rooom is stored in a separate file within the `laundry` subpackage (`data.py`) and imported on Line 3 of `laundry.py`.

#### eval ####
To evaluate a laundry command, get `roomid` and `machinetype` from the command's arguments and pass them to the `getMachines` function. `getMachines` uses `urllib` and `urllib2` to open the website containing the laundry data and get the HTML, and `beautifulsoup` to parse that HTML and find its relevant parts. We then construct a list of machines, where a machine is represented as a dictionary specifying the machine's `lr` (laundry room id), `id`, `name`, and `time` (a string describing the status of the machine)

### Shuttle ###

#### special ####
Laundry's special function lists all the shuttle stops and routes that the app knows about. This will give new users an idea of what they can find out more about.

#### eval ####
A shuttle command comes in one of two types: `stop` and `route` since the user can ask about either of these. Each of these evaluations basically do the same thing: make an API call with the given arguments and returns them as a string. The code behind making an API call, located in and imported from `api.py`, simply gives the necessary information to the API and returns the restult in JSON format. API stands for Application Program Interface; it is a standard of communication between data sources (in this case, the location of the shuttle data) and the application that wants that data (in this case, our app). Python's `requests` library contains the functions necessary for making an API call. These are converted to JavaScript Object Notation (JSON) format, a standard for representing information as lists and objects (dictionaries).

### Weather ###

#### special ####
Weather's special function simply gives the format that a user should input to receive weather information for a city.

#### eval ####
The weather service works by doing a Google search on the indicated city. It then scrapes the data from the corresponding HTML.

## Adding Services ##

### What You Need ###

* [Python 2.7](https://www.python.org/downloads/)
* Python packages - install using [`pip install packagename`](http://python-packaging-user-guide.readthedocs.io/en/latest/installing/) in the terminal
    * flask
    * twilio
    * urllib
    * urllib2
    * bs4 (BeautifulSoup)
    * requests
    * datetime
    * api

### What to Do ###

* Make a new folder under `services` (we'll refer to it as `myservice` here)
* In the `myservice` folder add a file called `__init__.py`. It doesn't need to contain anything in it
* Also a add a python file in `myservice` with the same name as the folder (`myservice.py`)
    * It should contain a variable `special` that stores a string. If a new user wants to use your service but isn't sure what to text, what message would you want to show them as an overview or demo?
	* It should also contain a function `eval(cmd)` that takes a command as an argument and returns a string representing the result of evaluating that command.
	* Feel free to add any additional functions to help satisfy these requirements
* In the `__init__.py` file directly in the `services` folder, add a line to import your main file from your folder: `from myservice import myservice`. This will make your service accessible from `app.py`
* Add your service to the `eval` function in `app.py`. This function just uses a if-elif-else branch (conditional statement) to delegate a command to its proper service. Just above the `else` statement, add something like the following (we use `'M'` to be the shorthand string representation of your service. It's also `'L'` for laundry and `'S'` for shuttle):

```
elif cmd['service'] == 'M':
    return myservice.eval(cmd['args'])
```

* Add your service to the `special` function in `app.py`, above `elif incoming.upper() == "DEMO": `:

```
elif incoming.upper() == "MYSERVICE":
    body = myservice.special
```

* Add your commands to `box` (the master list of commands) in data.py. Be sure to give each a `service`, any arguments your service needs to know as a dictionary (`args`), and a list of `tags` that uniquely identify the command:

`{'service': 'M', 'args':{'info0':'data0', 'info1':'data1'}, 'tags': ['tag0','tag1','tag3']}`
