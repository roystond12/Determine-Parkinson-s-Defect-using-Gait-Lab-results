from flask import Blueprint, render_template,jsonify,request
import pickle
import numpy as np

second = Blueprint("second",__name__,static_folder="static",template_folder="templates")
with open('pd2.pkl', 'rb') as file:
    model = pickle.load(file)

@second.route('/results', methods=['POST'])
def results():
    data = request.form.to_dict(flat=False)  
    step_length = float(data['step_length'][0] or 0)
    velocity = float(data['velocity'][0] or 0)
    cadence = float(data['cadence'][0] or 0)
    Mean_eGVI = float(data['Mean eGVI'][0] or 0)
    Left_eGVI = float(data['Left eGVI'][0] or 0)
    Right_eGVI = float(data['Right eGVI'][0] or 0)
    Ambulation_Time = float(data['Ambulation Time'][0] or 0)
    Stride_Time = float(data['Stride Time'][0] or 0)
    Double_Support_Time = float(data['Double Support Time'][0] or 0)
    Swing_Time = float(data['Swing Time'][0] or 0)
    Step_Time = float(data['Step Time'][0] or 0)
    Step_Width = float(data['Step Width'][0] or 0)
    stride_length = float(data['Stride Length'][0] or 0)
    Gait_Asymmetry = float(data['Gait Asymmetry'][0] or 0)
    Gait_Variability = float(data['Gait Variability'][0] or 0)   
    Postural = 1 if 'Postural' in data else 0
    Tremor = 1 if 'Tremor' in data else 0
    Rigidity = 1 if 'Rigidity' in data else 0
    instability = 1 if 'instability' in data else 0
    Bradykinesia = 1 if 'Bradykinesia' in data else 0
    dict = {
        52:Step_Width,
        43:step_length,
        42:velocity,
        18:stride_length,
        51:Step_Time,
        180:Stride_Time,
        101:Gait_Asymmetry,
        52:Swing_Time,
        35:Double_Support_Time,
        83:Ambulation_Time,
        51:cadence,
        93:Mean_eGVI,
        181:Left_eGVI,
        63:Right_eGVI,
        193:Postural,
        194:instability,
        195:Bradykinesia,
        196:Rigidity,
        197:Tremor,
        
    }
    data = [step_length,velocity,cadence,Mean_eGVI,Left_eGVI,Right_eGVI,Ambulation_Time,Stride_Time,Double_Support_Time,Swing_Time,Step_Time,Step_Width,stride_length,Gait_Asymmetry,Gait_Variability,Postural,Tremor,Rigidity,instability,Bradykinesia]
    arr = []
    for i in range(0,198):
        if i in dict.keys():
            arr.append(dict[i])
        else:
            arr.append(0)
    data = np.asarray(arr)        
    prediction = model.predict([data])[0]
    percprediction = model.predict_proba([data])[0][1]
    print(percprediction)
    return render_template('results.html',prediction = prediction,percprediction = percprediction * 100)

@second.route('/dashboard', methods=['POST'])
def dashboard():
    return render_template('index.html')

