import requests
from django.core.management.base import BaseCommand
from django.db.models.functions import Now
from server.schools.models import ImportedSchool


class Command(BaseCommand):
    help = "Fetch schools from gov site and load to db"

    def handle(self, *args, **options):
        self.fetch()

    def fetch(self):
        school_data = {}
        grades_letter_to_number = {
            "גן": 0,
            "א": 1,
            "ב": 2,
            "ג": 3,
            "ד": 4,
            "ה": 5,
            "ו": 6,
            "ז": 7,
            "ח": 8,
            "ט": 9,
            "י": 10,
            "יא": 11,
            "יב": 12,
            "יג": 13,
            "יד": 14,
        }

        all_schools = requests.get(
            r"https://shkifut.education.gov.il/api/data/lists"
        ).json()

        schools_codes = [
            school["s"] for school in all_schools["infoLists"] if school["m"] == 3
        ]

        for school_code in schools_codes:
            raw_school = requests.get(
                f"https://shkifut.education.gov.il/api/data/mosad/?semelMosad={school_code}&year=2019"
            ).json()
            school_data["name"] = raw_school["mosadGenaralData"]["SHEM_MOSAD"]
            address, address_city = raw_school["mosadGenaralData"][
                "KTOVET_MOSAD"
            ].split(",")
            school_data["address"] = address.strip()
            school_data["address_city"] = address_city.strip()
            school_data["school_code"] = school_code

            raw_grades = raw_school["mosadYearData"]["SHICHVA_AD_SHICHVA"]
            start_grade, end_grade = raw_grades.split(" - ")
            grades = list(
                range(
                    grades_letter_to_number[start_grade],
                    grades_letter_to_number[end_grade] + 1,
                )
            )

            school_data["grade_levels"] = grades
            school_data["longtitude"] = raw_school["mosadGenaralData"]["LONGITUDE"]
            school_data["latitude"] = raw_school["mosadGenaralData"]["LATITUDE"]

            # additional
            school_data["region"] = raw_school["mosadGenaralData"]["MACHOZ_MEFAK"]
            school_data["status"] = raw_school["mosadGenaralData"]["STATUS_MOSAD"]

            # ammounts
            school_data["boys"] = raw_school["mosadYearData"]["BANIM"]
            school_data["girls"] = raw_school["mosadYearData"]["BANOT"]
            school_data["male_teachers"] = raw_school["mosadYearData"]["MORIM"]
            school_data["female_teachers"] = raw_school["mosadYearData"]["MOROT"]

            # school type
            school_data["migzar"] = raw_school["mosadYearData"]["MIGZAR_YY"]
            school_data["school_type"] = raw_school["mosadYearData"]["PIKOH_YY"]
            school_data["school_stages"] = raw_school["mosadYearData"][
                "SHLAVE_CHINUCH_MOSAD_YY"
            ]
            school_data["authority_city"] = raw_school["mosadYearData"][
                "SHEM_RASHUT_YY"
            ]

            # school metadata
            school_data["is_bagrut"] = bool(
                raw_school["mosadGenaralData"]["MEGISH_LE_BAGRUT"]
            )
            school_data["immigrants_percent"] = raw_school["mosadYearData"][
                "TALMIDIM_OLIM"
            ]
            school_data["tech_students_percent"] = raw_school["mosadYearData"][
                "TALMIDIM_TECHNOLOGI"
            ]
            school_data["tech_diploma_eligible_percent"] = raw_school["mosadYearData"][
                "Zakaut_Tech_Achuz_Zakaim"
            ]
            school_data["special_education_percent"] = raw_school["mosadYearData"][
                "MADAD_CHINUCH_MEYUCHAD"
            ]
            school_data["social_economic_status"] = raw_school["mosadYearData"][
                "MATSAV_SOTSYOEKONOMI"
            ]
            school_data["decile_tipuah_hativa_benaim"] = raw_school["mosadYearData"][
                "ASIRON_HTB"
            ]
            school_data["decile_tipuah_hativa_eliona"] = raw_school["mosadYearData"][
                "ASIRON_HTE"
            ]
            school_data["decile_tipuah_yesodi"] = raw_school["mosadYearData"][
                "ASIRON_YES"
            ]
            school_data["ivhun_percent"] = raw_school["mosadYearData"][
                "ACHUZ_MECHOZI_IM_IVCHUN_ARTZI"
            ]

            # education picture
            education_picture = requests.get(
                f"https://shkifut.education.gov.il/api/data/mosadEduPic/?semelMosad={school_code}"
            )
            if education_picture.status_code == 200:
                # TODO: there is much more to get here
                education_picture = education_picture.json()
                for picture in education_picture["groups"]:
                    if picture["Id"] == 5 and picture["Classes"]:
                        for class_data in picture["Classes"]:
                            if class_data["Id"] == 12:
                                for zacaut in class_data["Indexes"]:
                                    if zacaut["Id"] == "ACHUZ_ZAKAIM":
                                        school_data["bagrut_eligible_percent"] = zacaut[
                                            "Value"
                                        ]
                                    elif zacaut["Id"] == "ACHUZ_ZAKAIM_MITZTYEN":
                                        school_data[
                                            "bagrut_excelent_eligible_percent"
                                        ] = zacaut["Value"]
                                    elif zacaut["Id"] == "ACHUZ_ANGLIT_5YL":
                                        school_data[
                                            "bagrut_english_5u_percent"
                                        ] = zacaut["Value"]
                                    elif zacaut["Id"] == "ACHUZ_MATEM_5YL":
                                        school_data["bagrut_math_5u_percent"] = zacaut[
                                            "Value"
                                        ]
                    elif picture["Id"] == 2 and picture["Classes"]:
                        class_data = picture["Classes"][0]
                        for index in class_data["Indexes"]:
                            if index["Id"] == "ACHUZ_MATMID":
                                school_data["hatmada_percent"] = index["Value"]
                            elif index["Id"] == "ACHUZ_NESHIRA":
                                school_data["drop_rate"] = index["Value"]

                    elif picture["Id"] == 1 and picture["Classes"]:
                        class_data = picture["Classes"][0]
                        for index in class_data["Indexes"]:
                            if index["Id"] == "GIUS_BANIM_LEZAVA":
                                school_data["boys_army_enlist_rate"] = index["Value"]
                            elif index["Id"] == "GIUS_BANOT_LEZAVA":
                                school_data["girls_army_enlist_rate"] = index["Value"]

            school_data["last_updated"] = Now()
            ImportedSchool.objects.update_or_create(
                defaults=school_data, school_code=school_code
            )
