from flask import Flask, render_template, request
from FHIRServer import FHIRServer

app = Flask(__name__)

CLIENT_ID = "4fd5577c-c9a2-4a7b-9a58-575c264254fa"
CLIENT_SECRET = "tup3m3ipxV._-.5a3s-ZtRLJnV2702Qg9B"
BASE_URI = "https://fhirworks.azurehealthcareapis.com"
TOKEN_ENDPOINT = "https://login.microsoftonline.com/a8f4640f-afee-43d6-b594-6c1db2196eca/oauth2/token"

fs = FHIRServer(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    token_endpoint=TOKEN_ENDPOINT,
    base_uri=BASE_URI,
)

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/create_appointment", methods=["POST"])
def create_appointment():
    staff_id = request.args.get("staff_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    fs.create_appointment(staff_id=staff_id, start_date=start_date, end_date=end_date)


@app.route("/appointments")
def return_appointment():
    staff_id = request.args.get("staff_id")
    return fs.get_appointments(staff_id=staff_id)

if __name__ == "__main__":
    app.run()
