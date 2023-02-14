import numpy as np
import pandas as pd
from flask import Flask,request,render_template
import joblib

app = Flask(__name__)
model = joblib.load("Student_Mark_Predictor_Model.pkl")
df = pd.DataFrame()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['post'])
def predict():
    global df

    input_features = [x for x in request.form.values()]
    print("Input Feature : ",input_features[0])
    if(input_features[0].isnumeric()):
        input_features = [int(x) for x in request.form.values()]
        features_value = np.array(input_features)
    else:
        if(input_features[0]=="Pass" or input_features[0]=="pass"):
            print("Entered\n")
            for i in range(1,10):
                print("I : ",i)
                tmp = model.predict([[i]])[0][0].round(2)
                print("Temp : ",tmp)
                if(tmp>=50):
                    return render_template('index.html',
                                           prediction_text="You Will get [{}%] ,marks, when you do study [{}] hours per day".format(
                                               tmp, i))

    if input_features[0]<0 or input_features[0]>24:
        return render_template('index.html',prediction_text="Please input the value between 1 to 24 if you live on earth")

    if(input_features[0]==0):
        return render_template('index.html',
                               prediction_text="Fail Thai Jais Baka!\n Shanti thi besi ne Vach!!")
    output = model.predict([features_value])[0][0].round(2)
    if(output>=100):
        output = 100
    df = pd.concat([df,pd.DataFrame({'Study Hours':input_features,'Predicted Output':[output]})],ignore_index=True)
    print(df)
    print("Input Value : ",input_features[0])
    print("Direct Data : ",request.form.values())
    df.to_csv('smp_data_from_app.csv')

    return render_template('index.html',prediction_text="You Will get [{}%] ,marks, when you do study [{}] hours per day".format(output,int(features_value[0])))

if __name__ == "__main__":
    app.run()