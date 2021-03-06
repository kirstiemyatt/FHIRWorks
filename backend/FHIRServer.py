import requests
import datetime
import time

CLIENT_ID = "4fd5577c-c9a2-4a7b-9a58-575c264254fa"
CLIENT_SECRET = "tup3m3ipxV._-.5a3s-ZtRLJnV2702Qg9B"
BASE_URI = "https://fhirworks.azurehealthcareapis.com"
TOKEN_ENDPOINT = "https://login.microsoftonline.com/a8f4640f-afee-43d6-b594-6c1db2196eca/oauth2/token"


class FHIRServer:
    def __init__(
        self, client_id: str, client_secret: str, token_endpoint: str, base_uri: str
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = token_endpoint
        self.base_uri = base_uri
        self._token_response = None

    def _access_token(self):
        if (
            self._token_response is None
            or int(self._token_response["expires_on"]) <= time.time()
        ):
            self._token_response = requests.post(
                self.token_endpoint,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "resource": self.base_uri,
                    "grant_type": "client_credentials",
                },
            ).json()
        return self._token_response["access_token"]

    def Patient(self):
        r = requests.get(
            f"{self.base_uri}/Patient",
            headers={"Authorization": f"Bearer {self._access_token()}"},
        )
        return r.json()

    def create_appointment(self, staff_id, start_date, end_date):
        appointment = {
            "resourceType": "Appointment",
            "status": "proposed",
            "description": "Please can I book my annual leave.",
            "created": datetime.datetime.now().strftime("%Y-%m-%d"),
            "comment": "Please can I book my annual leave.",
            "participant": [
                {
                    "actor": {
                        "reference": f"Patient/{staff_id}",
                        "display": "Staff member",
                    },
                    "required": "required",
                    "status": "accepted",
                }
            ],
            "requestedPeriod": [{"start": start_date, "end": end_date}],
        }

        r = requests.post(
            f"{self.base_uri}/Appointment",
            json=appointment,
            headers={"Authorization": f"Bearer {self._access_token()}"},
        )
        r.raise_for_status()

    def get_appointments(self, staff_id):
        r = requests.get(
            f"{self.base_uri}/Appointment?Patient={staff_id}",
            headers={"Authorization": f"Bearer {self._access_token()}"},
        )
        r.raise_for_status()
        appointments = {
            "appointments": [
                {
                    "status": e["resource"]["status"],
                    "description": e["resource"]["description"],
                    "start": e["resource"]["requestedPeriod"][0]["start"],
                    "end": e["resource"]["requestedPeriod"][0]["end"],
                }
                for e in r.json()["entry"]
            ]
        }
        return appointments
