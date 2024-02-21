from flask import Flask, request, jsonify,json
import pickle
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

app = Flask(__name__)

mapping = {
    0: '',
    1: 'P0133',
    2: 'C0300',
    3: 'P0079',
    4: 'P0078',
    5: 'P007E',
    6: 'P007F',
    7: 'P2004',
    8: 'U1004',
    9: 'C1004',
    10: 'B0004',
    11: 'P3000',
    12: 'P18F0',
    13: 'P18D0',
    14: 'P18E0',
    15: 'P2036',
    16: 'P1004'
}


@app.route('/test', methods=['POST'])
def post_json():
    # Check if the request contains JSON data
    
    if request.is_json:
        json_data = request.get_json()  # Get JSON data from the request
        # print(json_data)

        df = pd.DataFrame.from_dict(json_data, orient='index').T
        # print(df)
        # values_array = [value for value in json_data.values()]
        # print(values_array)
        output = mlprocess(df)
        # print('output',output)

        faultcodes = mappingFaultCodes(output)

        # print('faultcodes = ',faultcodes)

        output_json = json.dumps(faultcodes)  # Convert output array to list and then to JSON string

        

        return output_json  # Return JSON string as response
        # Return JSON data as response
    else:
        return jsonify({'error': 'Request data is not in JSON format'}), 400  # Return error response if data is not JSON
    



def mlprocess(df):
    with open('C:\\Users\\welcome\\Desktop\\DataSciencePro\\testingflaskthroughpostman\\scaler.pkl','rb')as f:
        scaler=pickle.load(f)

        

    # trainData = [inputArr]   
    print('traindata',df) 
    normalizedData = scaler.transform(df)
    print('normalized data = ',normalizedData)
    output = mlOutputPred(normalizedData) 

    return output




def mlOutputPred(input_data):
   
    
    # Loading the model
    with open('C:\\Users\\welcome\\Desktop\\DataSciencePro\\testingflaskthroughpostman\\multi_output_model.pkl', 'rb') as model_file:
        loaded_svm_model = pickle.load(model_file)
        output = loaded_svm_model.predict(input_data) 

    return output    
       


def mappingFaultCodes(outputArr):
    value1 = outputArr[0][0]
    value2 = outputArr[0][1]
    value3 = outputArr[0][2]
    
    faultcodes = []

    for key, value in mapping.items():  
        if key == value1 or key == value2 or key == value3:
            faultcodes.append(value)

    return faultcodes       



if __name__ == '__main__':
    app.run(debug=True,port=9090)
