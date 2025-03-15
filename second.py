from flask import Blueprint, render_template,jsonify,request
second = Blueprint("second",__name__,static_folder="static",template_folder="templates")

@second.route('/after_entry', methods=['POST'])
def after_entry():
    data = request.form.to_dict(flat=False)  
    return jsonify({'received_data': data})

