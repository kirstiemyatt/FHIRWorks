from flask import Flask, render_template, request
import datetime
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/create_appointment',methods = ['POST'])
def create_appointment():
    print(request.method)
    appointment_dict = {
        "resourceType": "Appointment",
        "status": "proposed",
        "created": datetime.datetime.now().strftime('%Y-%m-%d'),
        "comment": "Please can I book my annual leave.",
        "participant": [
            {
                "actor": {
                    "reference": "Patient/" + staff_id,
                    "display": "Staff member"
                },
                "required": "required",
                "status": "accepted"
            }
        ],
        "requestedPeriod": [
            {
                "start": start_date,
                "end": end_date
            }
        ]
    }
    return json.dumps(appointment_dict)



if __name__ == '__main__':
    app.run()
