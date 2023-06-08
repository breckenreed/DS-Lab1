import json
import flask
import requests 
import uuid

def forward_get(): #sends GET request 
    print("...Sending GET to logging service...")

    uuid_make = {                               #creates dictionary conntaining UUID/msg values to send them via JSON
            "uuid":str(uuid.uuid4()),           #creates random UUID value and assignes it to 'uuid' key inside dictionary
            "msg":flask.request.json.get('msg') #retrieves the 'msg' value from the JSON payload of the request and adds it to dictionary
        } 
    logs_response = requests.get(                #takes the response object returned by the requests.get() method which is instance of the Response class from the requests lib
        "{msg}/logging".format(msg=logs_url), #{msg}/logging is a string that contains a placeholder {msg}. The .format() method is used to replace this placeholder with the value of the logserv_url variable.
        json = uuid_make                        #placing uuid_make dictionary into json
    )
    print('1. Received response from logging service:', logs_response.text) #Prints the content of the response from logS

    msg_response = requests.get(                 #response object = instansce of Request class from requests 
        "{msg}/messages".format(msg=messag_url) #?string variable recieved from mess messerv_url
    )
    print('2. Received response from message service:', msg_response.text) #Prints the content of the response from mesS
    
    messages_dict = logs_response.json() #defines dictionary containing JSON content of response from logS
    return json.dumps(messages_dict)    #Serialises dictionary into JSON-formatted string and returns it, allowing to send it over network connections that expect string datф

def forward_post(): #sends POST request
    print("...Sending POST to logging service...") 

    try: 
        uuid_make = {
            "uuid":str(uuid.uuid4()),
            "msg":flask.request.json.get('msg') #retrieves the 'msg' value from the JSON payload of the request and adds it to dictionary
        } 
        
        logs_resp = requests.post(
            "{msg}/logging".format(msg=logs_url), #packs response from logS in the form of sring variable 
           json = uuid_make  
        )

        msg_resp = requests.get(           #response object = instansce of Request class from requests lib
        "{msg}/messages".format(msg=messag_url) #string variable recieved from mess messerv_url
    )
        
        stat_code = logs_resp.status_code #Returns the code that indicates the status 
        print('Response code from logging services:', stat_code)  #prints status code
        print('Communicated by message service:', msg_resp.text) #prints message server response content 
        return app.response_class(status=stat_code) #returns an instance of flask.Response class with the HTTP status code obtained from the logging service.
    except Exception as ex:
        raise(ex)
        flask.abort(400)  #server will not process the request due to malformed request syntax,
                          #invalid request message framint, deceptive request routing or othek kinds of client error

logs_url = "http://127.0.0.1:8001" #hardcoding the sockets of neighboruing services
messag_url = "http://127.0.0.1:8002" 

app = flask.Flask(__name__)  #creating instance of Flask class 
app.config["DEBUG"] = True   #enable the debug mode for the application

@app.route('/', methods=['GET','POST']) 
def facade_serv():
    if flask.request.method == 'GET':
        return forward_get()
    elif flask.request.method == 'POST':
        return forward_post()
    else:
        flask.abort(405)

app.run(host='0.0.0.0', port='8000')