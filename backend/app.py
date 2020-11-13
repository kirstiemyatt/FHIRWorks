from flask import Flask, render_template, request
import datetime
import json
import requests
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/create_appointment',methods = ['POST'])
def create_appointment():
    print(request.args)
    staff_id = request.args.get('staff_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

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



'''

Hit FHIR server and return response
Obtain response and and trim down to :

{
  "appointments": [
    {
      "status": "booked",
      "description": "Some description",
      "start": "2021-02-01T00:00:00+00:00",
      "end": "2021-02-02T00:00:00+00:00"
    },
    {
      "status": "booked",
      "description": "Some description",
      "start": "2021-02-01T00:00:00+00:00",
      "end": "2021-02-02T00:00:00+00:00"
    }
  ]
}
'''


def hit_fhir () :
    endpoint = "https://fhirworks.azurehealthcareapis.com/Appointment?Patient/cfe4ccf9-1b57-4c79-8350-38363c252ac2"
    headers = {'Content-type': 'application/json', "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCIsImtpZCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCJ9.eyJhdWQiOiJodHRwczovL2ZoaXJ3b3Jrcy5henVyZWhlYWx0aGNhcmVhcGlzLmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0L2E4ZjQ2NDBmLWFmZWUtNDNkNi1iNTk0LTZjMWRiMjE5NmVjYS8iLCJpYXQiOjE2MDUyNjgyMjYsIm5iZiI6MTYwNTI2ODIyNiwiZXhwIjoxNjA1MjcyMTI2LCJhY3IiOiIxIiwiYWlvIjoiQVNRQTIvOFJBQUFBU3pEOVhJbitydmV2Z2VnN2tKKzhPcGwrSElyWkl4djZ5ZVRBd2R4OWhtST0iLCJhbXIiOlsicHdkIl0sImFwcGlkIjoiYWRlMjAyYmYtNTRhMS00MmYyLTlmODItMjFlYmRjZTMxMWY1IiwiYXBwaWRhY3IiOiIxIiwiaXBhZGRyIjoiOTIuNDAuMjAyLjE3IiwibmFtZSI6IkZoaXJ3b3JrcyIsIm9pZCI6IjVhMGJmN2EwLTVmMzItNGM3MC1iZGRkLWM4N2Q3OGU0YTEwZiIsInB1aWQiOiIxMDAzMjAwMEY3QjVDNkUzIiwicmgiOiIwLkFUb0FEMlQwcU82djFrTzFsR3dkc2hsdXlyOEM0cTJoVlBKQ240SWg2OXpqRWZVNkFLcy4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzdWIiOiJmVEdERGx4LVRFdzd2a0FjaV9lMGxiV3RSS1d2dW1FZ3Q1OHZPUmpCS0dRIiwidGlkIjoiYThmNDY0MGYtYWZlZS00M2Q2LWI1OTQtNmMxZGIyMTk2ZWNhIiwidW5pcXVlX25hbWUiOiJmaGlyd29ya3NAYWxleGhhd2Rvbmdvb2dsZW1haWwub25taWNyb3NvZnQuY29tIiwidXBuIjoiZmhpcndvcmtzQGFsZXhoYXdkb25nb29nbGVtYWlsLm9ubWljcm9zb2Z0LmNvbSIsInV0aSI6Ilp3eWNnQjN3elVXUU9FUGdZT2t2QVEiLCJ2ZXIiOiIxLjAifQ.h5T7k_JKu1fWDnmkzgxutG8W1_-jd2OvpEWjqymCpaVs_JNOD4BpRujco6EB_GHyIUjqFuif0cx37mPUTPhHXj8brsa7VXbMk18BfXfOS5Epd60va1RocQHseG1yim3NWJoDucu8HVEAnLQztVSyUfcmk8Zywqjtp6jdfpLqBQmoxtiFMP1fyAyeQMMc87VpdVVUI5k7KTsGwj-D5IeCRFR1z-yxwCY4x8E_9T_KyU-XFnY9OMtKIDGditULZj1HJWBsKU0DLhNJOtf07TsDDAzkgmdALT_IUor_n0dWa6SrD2bEywcg3siq249naNcYl_245zYIheob_v8PK_BY6g"}
    response = requests.get(endpoint, headers=headers)
    # print(json.loads(response.content))


    data = json.loads(response.content)
    print(data)





if __name__ == '__main__':
  hit_fhir()
