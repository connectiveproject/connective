import csv

import requests
from django.core.management.base import BaseCommand

from server.schools.models import ImportedSchool


class Command(BaseCommand):
    help = "Fetch schools from gov site and load to db or csv"

    def handle(self, *args, **options):
        self.fetch(options["csv"])

    def add_arguments(self, parser):
        parser.add_argument("--csv", action="store_true")

    def fetch(self, write_csv):
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
        if write_csv:
            fieldnames = [
                "name",
                "address",
                "address_city",
                "school_code",
                "grade_levels",
                "longtitude",
                "latitude",
                "region",
                "status",
                "boys",
                "girls",
                "male_teachers",
                "female_teachers",
                "migzar",
                "school_type",
                "school_stages",
                "authority_city",
                "is_bagrut",
                "immigrants_percent",
                "tech_students_percent",
                "tech_diploma_eligible_percent",
                "special_education_percent",
                "social_economic_status",
                "decile_tipuah_hativa_benaim",
                "decile_tipuah_hativa_eliona",
                "decile_tipuah_yesodi",
                "ivhun_percent",
                "hatmada_percent",
                "drop_rate",
                "bagrut_eligible_percent",
                "bagrut_excelent_eligible_percent",
                "bagrut_english_5u_percent",
                "bagrut_math_5u_percent",
                "boys_army_enlist_rate",
                "girls_army_enlist_rate",
                "last_updated",
            ]
            csv_file = open("schools.csv", "w", encoding="UTF-8")
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

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

            address, address_city = raw_school["mosadGenaralData"][
                "KTOVET_MOSAD"
            ].split(",")

            raw_grades = raw_school["mosadYearData"]["SHICHVA_AD_SHICHVA"]
            start_grade, end_grade = raw_grades.split(" - ")
            grades = list(
                range(
                    grades_letter_to_number[start_grade],
                    grades_letter_to_number[end_grade] + 1,
                )
            )

            education_picture = requests.get(
                f"https://shkifut.education.gov.il/api/data/mosadEduPic/?semelMosad={school_code}"
            )
            girls_army_enlist_rate = None
            boys_army_enlist_rate = None
            bagrut_eligible_percent = None
            bagrut_excelent_eligible_percent = None
            bagrut_english_5u_percent = None
            bagrut_math_5u_percent = None
            if education_picture.status_code == 200:
                education_picture = education_picture.json()
                for picture in education_picture["groups"]:
                    if picture["Id"] == 5 and picture["Classes"]:
                        for class_data in picture["Classes"]:
                            if class_data["Id"] == 12:
                                for zacaut in class_data["Indexes"]:
                                    if zacaut["Id"] == "ACHUZ_ZAKAIM":
                                        bagrut_eligible_percent = zacaut["Value"]
                                    elif zacaut["Id"] == "ACHUZ_ZAKAIM_MITZTYEN":
                                        bagrut_excelent_eligible_percent = zacaut[
                                            "Value"
                                        ]
                                    elif zacaut["Id"] == "ACHUZ_ANGLIT_5YL":
                                        bagrut_english_5u_percent = zacaut["Value"]
                                    elif zacaut["Id"] == "ACHUZ_MATEM_5YL":
                                        bagrut_math_5u_percent = zacaut["Value"]
                    elif picture["Id"] == 2 and picture["Classes"]:
                        class_data = picture["Classes"][0]
                        for index in class_data["Indexes"]:
                            if index["Id"] == "ACHUZ_MATMID":
                                hatmada_percent = index["Value"]
                            elif index["Id"] == "ACHUZ_NESHIRA":
                                drop_rate = index["Value"]

                    elif picture["Id"] == 1 and picture["Classes"]:
                        class_data = picture["Classes"][0]
                        for index in class_data["Indexes"]:
                            if index["Id"] == "GIUS_BANIM_LEZAVA":
                                boys_army_enlist_rate = index["Value"]
                            elif index["Id"] == "GIUS_BANOT_LEZAVA":
                                girls_army_enlist_rate = index["Value"]

            school_data = {
                "name": raw_school["mosadGenaralData"]["SHEM_MOSAD"],
                "address": address.strip(),
                "address_city": address_city.strip(),
                "school_code": school_code,
                "grade_levels": grades,
                "longtitude": raw_school["mosadGenaralData"]["LONGITUDE"],
                "latitude": raw_school["mosadGenaralData"]["LATITUDE"],
                "region": raw_school["mosadGenaralData"]["MACHOZ_MEFAK"],
                "status": raw_school["mosadGenaralData"]["STATUS_MOSAD"],
                "boys": raw_school["mosadYearData"]["BANIM"],
                "girls": raw_school["mosadYearData"]["BANOT"],
                "male_teachers": raw_school["mosadYearData"]["MORIM"],
                "female_teachers": raw_school["mosadYearData"]["MOROT"],
                "migzar": raw_school["mosadYearData"]["MIGZAR_YY"],
                "school_type": raw_school["mosadYearData"]["PIKOH_YY"],
                "school_stages": raw_school["mosadYearData"]["SHLAVE_CHINUCH_MOSAD_YY"],
                "authority_city": raw_school["mosadYearData"]["SHEM_RASHUT_YY"],
                "is_bagrut": bool(raw_school["mosadGenaralData"]["MEGISH_LE_BAGRUT"]),
                "immigrants_percent": raw_school["mosadYearData"]["TALMIDIM_OLIM"],
                "tech_students_percent": raw_school["mosadYearData"][
                    "TALMIDIM_TECHNOLOGI"
                ],
                "tech_diploma_eligible_percent": raw_school["mosadYearData"][
                    "Zakaut_Tech_Achuz_Zakaim"
                ],
                "special_education_percent": raw_school["mosadYearData"][
                    "MADAD_CHINUCH_MEYUCHAD"
                ],
                "social_economic_status": raw_school["mosadYearData"][
                    "MATSAV_SOTSYOEKONOMI"
                ],
                "decile_tipuah_hativa_benaim": raw_school["mosadYearData"][
                    "ASIRON_HTB"
                ],
                "decile_tipuah_hativa_eliona": raw_school["mosadYearData"][
                    "ASIRON_HTE"
                ],
                "decile_tipuah_yesodi": raw_school["mosadYearData"]["ASIRON_YES"],
                "ivhun_percent": raw_school["mosadYearData"][
                    "ACHUZ_MECHOZI_IM_IVCHUN_ARTZI"
                ],
                "bagrut_eligible_percent": bagrut_eligible_percent,
                "girls_army_enlist_rate": girls_army_enlist_rate,
                "boys_army_enlist_rate": boys_army_enlist_rate,
                "drop_rate": drop_rate,
                "hatmada_percent": hatmada_percent,
                "bagrut_math_5u_percent": bagrut_math_5u_percent,
                "bagrut_english_5u_percent": bagrut_english_5u_percent,
                "bagrut_excelent_eligible_percent": bagrut_excelent_eligible_percent,
            }

            if write_csv:
                csv_writer.writerow(school_data)
                csv_file.flush()
            else:
                ImportedSchool.objects.update_or_create(
                    defaults=school_data, school_code=school_code
                )
