import requests
from django.core.management.base import BaseCommand
from django.db.models.functions import Now
from server.organizations.models import ImportedActivity

class Command(BaseCommand):
    help = "Fetch activities from gov site and load to db"
    def handle(self, *args, **options):
        self.fetch()
    def fetch(self):
        BASE_URL = "https://apps.education.gov.il"
        ACTIVITIES_API_URL = f"{BASE_URL}/TyhNet/ClientWs/TochnitCh.asmx/IturTochnitChByMeafyenim"  # noqa
        ACTIVITIES_DEFAULT_PAGE_SIZE = 100
        ACTIVITY_FIELD_MAPPING = {
            "name": "ShemTochnit",
            "target_audience": "ShichvatLomdim",
            "activity_website_url": None,
            "activity_email": None,
            "description": "TaktsirTochnit",
            "activity_code": "MisparTochnit",
            "contact_name": None,
            "phone_number": None,
            "is_active": "CodeStatusTochnit",
            "longtitude": None,
            "latitude": None,
            # New fields
            "goal": "MataraMerkazit",
            "raw_name": "ShemTochnit_Raw",
        }



        total_records = None
        activities = []
        page_number = 1
        while total_records is None or len(activities) < total_records:
            response = requests.post(ACTIVITIES_API_URL,
                                    headers={
                                        "Accept": "application/json",
                                        "Content-Type": "application/json",
                                        "Accept-Language": "en-US,en;q=0.9"
                                    },
                                    json={"MeafyeneiTochnit": "",
                                        "strTchumMerkazi": "",
                                        "strMakorTochnit": "",
                                        "strStatusTochnit": "",
                                        "CodeYechidaAchrayit": -1,
                                        "Cipuschofshi": "",
                                        "MisparTochnit": -1,
                                        "TochnitBelivuiMisrad": -1,
                                        "kyamDerugMenahalim": -1,
                                        "KyemotChavotDaatMefakchim": -1,
                                        "Natsig": "",
                                        "ShemTochnit": "",
                                        "Taagid": "",
                                        "TaagidMishtamesh": "",
                                        "TochnitActive": False,
                                        "NidrashAlut": -1,
                                        "PageNumber": page_number,
                                        "PageSize": ACTIVITIES_DEFAULT_PAGE_SIZE,
                                        "OrderBy": "",
                                        "IncludeYechidotBat": True,
                                        "TochnitLeumit": -1}
                                    )
            response.raise_for_status()

            content = response.json()["d"]

            for raw_activity in content["Data"]:
                activity_code = raw_activity['MisparTochnit']
                contact_info = requests.post('https://apps.education.gov.il/TyhNet/ClientWs/TochnitCh.asmx/GetDataAc6', json={'MisparTochnit':activity_code})
                raw_contact_info = contact_info.json()['d']
                
                activity = {
                    "name":raw_activity[ACTIVITY_FIELD_MAPPING["name"]],
                    "target_audience":raw_activity[ACTIVITY_FIELD_MAPPING["target_audience"]].replace("'", "").split(" | "), # noqa
                    "activity_website_url":raw_contact_info['ktovet_kishur_atar_taagid'],
                    "activity_email":raw_contact_info['EMAIL'],
                    "description":raw_activity[ACTIVITY_FIELD_MAPPING["description"]],
                    "activity_code":activity_code,
                    "contact_name":raw_contact_info['GOREM_KESHER_BATAAGID'],
                    "phone_number":raw_contact_info['NAYAD'],
                    "is_active":raw_activity[ACTIVITY_FIELD_MAPPING["activity_code"]] == 4, # Check all status codes

                    # New fields
                    "goal":raw_activity[ACTIVITY_FIELD_MAPPING["goal"]],
                    "raw_name":raw_activity[ACTIVITY_FIELD_MAPPING["raw_name"]],
                }
                ImportedActivity.objects.update_or_create(defaults=activity, activity_code=activity_code)
        

