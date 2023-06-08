import flask
import json

app = flask.Flask(__name__) #creating instance of Flask class 
app.config["DEBUG"] = True #enable DEBUG mode for more info in reports 

messages_dict = {} 

@app.route('/logging', methods=['GET', 'POST']) #app logic for different type of request 
def facade_serv():
    if flask.request.method == 'GET':
        return forward_get()
    else:
        return forward_post()

def forward_post(): #the function that retrieves data forwarded via post  
    data=flask.request.json
    print('Received request with following content: ', data)
    messages_dict.update({data["uuid"]: data["msg"]})
    print('POST content saved to logs')
    return "OK"

def forward_get():
    data=flask.request.json
    print('Received request with following content: ', data)
    print('Returned messages: ', messages_dict.values())
    return json.dumps([msg for msg in messages_dict.values()])

@app.route('/messages') #logic for accessing messaging-service
def messages():
    return 'Sample service message placeholder'

if __name__ == '__main__': 
      app.run(host='0.0.0.0', port='8001')