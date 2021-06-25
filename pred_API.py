from flask import Flask
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
api = Api(app)
import h2o
import pandas as pd
h2o.init()

## load trained model
model_path = r'C:\Users\annan\OneDrive - Seneca\Desktop\REA\DeepLearning_model_python_1624162362692_17'
uploaded_model = h2o.load_model(model_path)

# argument parsing
parser = reqparse.RequestParser(bundle_errors=True) # if there are 2 errors, both of their msgs will be printed
parser.add_argument('Having_IP_Address')
parser.add_argument('URL_Length')
parser.add_argument('Shortening_Service')
parser.add_argument('Having_At_Symbol')
parser.add_argument('Domain_Registration_Length')
parser.add_argument('Prefix_Suffix')
parser.add_argument('Having_Sub_Domain')
parser.add_argument('URL_of_Anchor')
parser.add_argument('HTTPS_Token')
parser.add_argument('SFH')
parser.add_argument('Abnormal_URL')
parser.add_argument('Redirect')
parser.add_argument('PopUpWidnow')
parser.add_argument('DNSRecord')
parser.add_argument('Web_Traffic')
parser.add_argument('Links_Pointing_to_Page')

#params={"Having_IP_Address":"0","URL_Length":"0","Shortining_Service":"0","Having_At_Symbol":"0","Domain_registeration_length":"0","Prefix_Suffix":"0","Having_Sub_Domain":"0","URL_of_Anchor":"1","HTTPS_token":"0","SFH":"0","Abnormal_URL":"0","Redirect":"0","PopUpWidnow":"0","DNSRecord":"0","Web_Traffic":"1","Links_pointing_to_page":"1"}

#Categorical Columns - enum
#Numerical Columns - real
col_dict = {"Having_IP_Address":"int",
            "URL_Length":"int",
            "Shortening_Service":"int",
            "Having_At_Symbol":"int",
            "Domain_Registration_Length":"int",
            "Prefix_Suffix":"int",
            "Having_Sub_Domain":"int",
            "URL_of_Anchor":"int",
            "HTTPS_Token":"int",
            "SFH":"int",
            "Abnormal_URL":"int",
            "Redirect":"int",
            "PopUpWidnow":"int",
            "DNSRecord":"int",
            "Web_Traffic":"int",
            "Links_Pointing_to_Page":"int"}
# prepare empty test data frame to be fed to the model
data = {}
# results dict
item_dict = {}
#class NumpyEncoder(json.JSONEncoder):
#    def default(self, obj):
#        if isinstance(obj, np.ndarray):
#            return obj.tolist()
#        return json.JSONEncoder.default(self, obj)

class URL_Detection(Resource):
    def get(self):
        args = parser.parse_args()
        Having_IP_Address = args['Having_IP_Address']
        URL_Length = args['URL_Length']
        Shortening_Service = args['Shortening_Service']
        Having_At_Symbol = args['Having_At_Symbol']
        Domain_Registration_Length = args['Domain_Registration_Length']
        Prefix_Suffix = args['Prefix_Suffix']
        Having_Sub_Domain = args['Having_Sub_Domain']
        URL_of_Anchor = args['URL_of_Anchor']
        HTTPS_Token = args['HTTPS_Token']
        SFH = args['SFH']
        Abnormal_URL = args['Abnormal_URL']
        Redirect = args['Redirect']
        PopUpWidnow = args['PopUpWidnow']
        DNSRecord = args['DNSRecord']
        Web_Traffic = args['Web_Traffic']
        Links_Pointing_to_Page = args['Links_Pointing_to_Page']
        Result = '1' #setting as default to declined (can set it as 'approved' as well, doesn't matter)
         
        # put key:value pairs in empty dict called data
        data['Having_IP_Address'] = Having_IP_Address
        data['URL_Length'] = URL_Length
        data['Shortening_Service'] = Shortening_Service
        data['Having_At_Symbol'] = Having_At_Symbol
        data['Domain_Registration_Length'] = Domain_Registration_Length
        data['Prefix_Suffix'] = Prefix_Suffix
        data['Having_Sub_Domain'] = Having_Sub_Domain
        data['URL_of_Anchor'] = URL_of_Anchor
        data['HTTPS_Token'] = HTTPS_Token
        data['SFH'] = SFH
        data['Abnormal_URL'] = Abnormal_URL
        data['Redirect'] = Redirect
        data['PopUpWidnow'] = PopUpWidnow
        data['DNSRecord'] = DNSRecord
        data['Web_Traffic'] = Web_Traffic
        data['Links_Pointing_to_Page'] = Links_Pointing_to_Page
        data['Result'] = Result
         
        # creating dataframe from dict
        testing = pd.DataFrame(data, index=[0])
         
        # converting pandas to h2o dataframe
        test = h2o.H2OFrame(testing, column_types = col_dict)
        
        # making predictions
        pred_ans = uploaded_model.predict(test).as_data_frame()
         
        # put key:value pairs in empty dict called item_dict
        item_dict['Prediction'] = str(pred_ans.predict.values[0])
        item_dict['Benign'] = str(pred_ans.p0.values[0])
        item_dict['Malicous'] = str(pred_ans.p1.values[0])
       
        return{'ans': item_dict}
         
api.add_resource(URL_Detection, '/')

if __name__ == '__main__':
    app.run(debug=True, port= 1234)
