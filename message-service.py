import flask

app = flask.Flask(__name__) #creating instance of Flask class 
app.config["DEBUG"] = True # 


@app.route('/messages', methods=['POST','GET'])
def message():
    return "This is sample static test message from message-service"

app.run(host='0.0.0.0', port='8002')
