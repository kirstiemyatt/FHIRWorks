from flask import Flask
import datetime
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hackairethon wooooo!'


def create_appointment(staff_id, start_date, end_date):
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
