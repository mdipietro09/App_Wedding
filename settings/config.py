
import os

ENV = "DEV"
#ENV = "PROD"


## server
host = "0.0.0.0"
port = int(os.environ.get("PORT", 5000))


## info
app_name = "Wedding Planner"
contacts = "https://www.linkedin.com/in/mauro-di-pietro-56a1366b/"
code = "https://github.com/mdipietro09/App_Wedding"
fontawesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'

about = "Load your guest list or try random simulation"

## fs
#root = os.path.dirname(os.path.dirname(__file__)) + "/"


'''
1. draw with plotly
2. use bootstrap within dash
3. change inputs based on events
4. upload and download files
'''