from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route('/test',methods=['POST'])
def test():
    if request.method == 'POST':
        reqData = request.json
        name = reqData['name']
        return jsonify({'response':'Hello '+name})

if __name__=='__main__':
    app.run(debug=True,port=9090)