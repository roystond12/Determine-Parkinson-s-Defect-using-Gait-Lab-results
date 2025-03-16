from flask import Blueprint, render_template,jsonify,request
import pickle
import numpy as np
import jsonpickle

second = Blueprint("second",__name__,static_folder="static",template_folder="templates")
with open('pd2.pkl', 'rb') as file:
    model = pickle.load(file)

@second.route('/after_entry', methods=['POST'])
def after_entry():
    data = request.form.to_dict(flat=False)  
    step_length = float(data['step_length'][0])
    velocity = float(data['velocity'][0])
    cadence = float(data['cadence'][0])
    Mean_eGVI = float(data['Mean eGVI'][0])
    Left_eGVI = float(data['Left eGVI'][0])
    Right_eGVI = float(data['Right eGVI'][0])
    Ambulation_Time = float(data['Ambulation Time'][0])
    Stride_Time = float(data['Stride Time'][0])
    Double_Support_Time = float(data['Double Support Time'][0])
    Swing_Time = float(data['Swing Time'][0])
    Step_Time = float(data['Step Time'][0])
    Step_Width = float(data['Step Width'][0])
    stride_length = float(data['Stride Length'][0])
    Gait_Asymmetry = float(data['Gait Asymmetry'][0])
    Gait_Variability = float(data['Gait Variability'][0])   
    Postural = 1 if 'Postural' in data else 0
    Tremor = 1 if 'Tremor' in data else 0
    Rigidity = 1 if 'Rigidity' in data else 0
    instability = 1 if 'instability' in data else 0
    Bradykinesia = 1 if 'Bradykinesia' in data else 0
    dict = {
        2:step_length,
        8:velocity,
        9:stride_length,
        21:Step_Time,
        27:Stride_Time,
        75:Gait_Asymmetry,
        93:Swing_Time,
        111:Double_Support_Time,
        189:Ambulation_Time,
        190:cadence,
        191:Mean_eGVI,
        192:Left_eGVI,
        193:Right_eGVI,
        194:Postural,
        195:instability,
        196:Bradykinesia,
        197:Rigidity,
        198:Tremor
        
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
    
    return str(prediction)

