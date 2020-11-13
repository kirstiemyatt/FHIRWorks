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


def return_appointment(patient_id):
    endpoint = "https://fhirworks.azurehealthcareapis.com/Appointment?Patient/"+patient_id
    headers = {'Content-type': 'application/json', "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCIsImtpZCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCJ9.eyJhdWQiOiJodHRwczovL2ZoaXJ3b3Jrcy5henVyZWhlYWx0aGNhcmVhcGlzLmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0L2E4ZjQ2NDBmLWFmZWUtNDNkNi1iNTk0LTZjMWRiMjE5NmVjYS8iLCJpYXQiOjE2MDUyNzMxMDMsIm5iZiI6MTYwNTI3MzEwMywiZXhwIjoxNjA1Mjc3MDAzLCJhY3IiOiIxIiwiYWlvIjoiQVNRQTIvOFJBQUFBZHd2SERMdEdicVh1dUpKbTNHeUZZRHlWOUh2TUhjeWtWWVNydFlrV0Nlcz0iLCJhbXIiOlsicHdkIl0sImFwcGlkIjoiYWRlMjAyYmYtNTRhMS00MmYyLTlmODItMjFlYmRjZTMxMWY1IiwiYXBwaWRhY3IiOiIxIiwiaXBhZGRyIjoiOTIuNDAuMjAyLjg3IiwibmFtZSI6IkZoaXJ3b3JrcyIsIm9pZCI6IjVhMGJmN2EwLTVmMzItNGM3MC1iZGRkLWM4N2Q3OGU0YTEwZiIsInB1aWQiOiIxMDAzMjAwMEY3QjVDNkUzIiwicmgiOiIwLkFUb0FEMlQwcU82djFrTzFsR3dkc2hsdXlyOEM0cTJoVlBKQ240SWg2OXpqRWZVNkFLcy4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzdWIiOiJmVEdERGx4LVRFdzd2a0FjaV9lMGxiV3RSS1d2dW1FZ3Q1OHZPUmpCS0dRIiwidGlkIjoiYThmNDY0MGYtYWZlZS00M2Q2LWI1OTQtNmMxZGIyMTk2ZWNhIiwidW5pcXVlX25hbWUiOiJmaGlyd29ya3NAYWxleGhhd2Rvbmdvb2dsZW1haWwub25taWNyb3NvZnQuY29tIiwidXBuIjoiZmhpcndvcmtzQGFsZXhoYXdkb25nb29nbGVtYWlsLm9ubWljcm9zb2Z0LmNvbSIsInV0aSI6ImNCOXJYYW05UmtTaUMtNWpFM1FkQWciLCJ2ZXIiOiIxLjAifQ.aY89_BacaH0eXIA-mSmZZT1gPaVVsfDRKpswLFjSPXwei8T19Q5e12ROjA0nP-Uas-6WD6fvCzrHV4vLoC2yHGD67fqc7Zy7UFU1hy6E_8nz-ekvNgHdlr_j6eq7zRCwGh70xOS49RcPTPdNYvh7iisoKE1y7Pw8s6aKt7_H5XlZjIrXlUL5RYLprcHmQT5ZW4l1haT6VwVmD2K3VAejhyxZygk7n9ZmU0j1gza25qlb3FqIRAREb5AKlCIGYLNhbke3TxJQzIn-YdJ3G_fun3-gR3klXVZU5gaVQMr7UGFkfRToK83FzKJobUyZH8ejMirIaH_0cj9jsM9BJhRRXw"}
    response = requests.get(endpoint, headers=headers)
    response_dict = json.loads(response.content)

    new_dict = {"appointments": [
        {"status": e["resource"]["status"], "description": e["resource"]["description"], "start": e["resource"]["start"],"end": e["resource"]["end"]} for e in
        response_dict["entry"]]}

    return new_dict


if __name__ == '__main__':
  app.run()