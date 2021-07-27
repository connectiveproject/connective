import csv
import json
import logging
import re

import requests
from django.core.management.base import BaseCommand

import server.organizations.management.commands.config as config
from server.organizations.models import ImportedOrganization

logger = logging.getLogger(__name__)

ajax_data = {
    "Content-Type": "application/json",
    "action": "GSTAR_Ctrl",
    "data": ["580430767"],
    "method": "getMalkarDetails",
    "tid": 14,
    "type": "rpc",
    "ctx": {
        "csrf": "VmpFPSxNakF5TVMwd055MHlORlF3T0RvMU16b3dOeTQ1TkRKYSw4M0d2OGVKZVEzNnJ4M0dTLWxucmZYLE9EaG1aV0ky",
        "ns": "",
        "ver": 43,
        "vid": "06624000000VGgM",
    },
}

ajax_headers = {
    "Referer": "https://www.guidestar.org.il/search-malkars?Sug_Hitagdut=%D7%A2%D7%9E%D7%95%D7%AA%D7%94"
}

ajax_get_ids = {
    "action": "GSTAR_Ctrl",
    "method": "searchMalkars",
    "data": [{}, {"apiName": "Name", "sortDesc": False}],
    "type": "rpc",
    "tid": 10,
    "ctx": {
        "csrf": "VmpFPSxNakF5TVMwd055MHlORlF4TkRveE9Eb3hPUzQ0TWpoYSw1c3ZmVmRnRDN1ZW5XdjB1bTY3TnFHLE9XUmpOV1F6",
        "vid": "06624000000VGgM",
        "ns": "",
        "ver": 43,
    },
}

ajax_amount_of_results = {
    "action": "GSTAR_Ctrl",
    "method": "getSeachMalkarCount",
    "data": [
        {"Sug_Hitagdut": ["עמותה"], "CLSS_Main_Classification_Num": ["21"]},
        {"apiName": "Name", "sortDesc": False},
    ],
    "type": "rpc",
    "tid": 13,
    "ctx": {
        "csrf": "VmpFPSxNakF5TVMwd055MHlORlF4TkRveE9Eb3hPUzQ0TWpkYSxac3pJMGJfV3p0akhMUFh5aEtiQy16LFpXTXhPV1Js",
        "vid": "06624000000VGgM",
        "ns": "",
        "ver": 43,
    },
}

AJAX_URL = "https://www.guidestar.org.il/apexremote"
ROOT_URL = "https://www.guidestar.org.il"


class Command(BaseCommand):
    help = "Fetch schools from gov site and load to db"

    def add_arguments(self, parser):
        parser.add_argument("--csv", action="store_true")

    def get_csrf(self):
        """
        This function should get from the site the csrf in order to send the request.
        :return string
        """

        _response = requests.get(ROOT_URL)
        _response.raise_for_status()
        _response = _response.text
        _csrf = re.findall(r'csrf":"([\w\d]+)"', _response)

        # if csrf is in the page else return default value
        if _csrf:
            return _csrf[0]
        return "VmpFPSxNakF5TVMwd055MHlORlF3T0RvMU16b3dOeTQ1TkRKYSw4M0d2OGVKZVEzNnJ4M0dTLWxucmZYLE9EaG1aV0ky"

    def get_total_results_from_guidestar(self):
        """
        This function returns the total results to save into the DB.
        :return: int
        """
        ajax_amount_of_results["ctx"]["csrf"] = self.get_csrf()
        post_response = requests.post(
            AJAX_URL, json=ajax_amount_of_results, headers=ajax_headers
        )
        post_response.raise_for_status()
        post_response = json.loads(post_response.text)
        amount_of_results = post_response[0]["result"]

        # In case their are more than 999 results
        if "," in amount_of_results:
            amount_of_results = int(amount_of_results.replace(",", ""))
        else:
            amount_of_results = int(amount_of_results)
        return amount_of_results

    def collect_ids_from_guidestar(self, amount_of_pages):
        """
        This function should collect all the relevant ids in order to gather information about each company.
        :param amount_of_pages: the number of pages should be collected
        :return: list
        """
        ids_collection = set()
        last_company_name = ""

        # Run for each iteration
        for page_number in range(1, amount_of_pages):
            logger.info("complete {}/{}".format(page_number, amount_of_pages))
            # Set the requested page
            ajax_get_ids["data"][0]["pageNumber"] = page_number
            ajax_get_ids["ctx"]["csrf"] = self.get_csrf()
            if page_number > 1:
                ajax_get_ids["data"][1]["value"] = last_company_name

            # Request for 50 more companies
            post_response = requests.post(
                AJAX_URL, json=ajax_get_ids, headers=ajax_headers
            )
            post_response.raise_for_status()
            post_response = json.loads(post_response.text)

            # Run for each company and saves the company's id
            for company_json in post_response[0]["result"]["result"]:
                ids_collection.add(company_json["regNum"])
            last_company_name = company_json["Name"]
        return list(ids_collection)

    def collect_company_information(self, _id):
        """
        This function should collect company information and return dictionary with
        all the relevant data about the company.

        :param _id: string represents the ID for a company
        :return: Dictionary
        """

        company_information = {}

        # Set the requested ID
        ajax_data["data"][0] = _id
        ajax_data["ctx"]["csrf"] = self.get_csrf()

        # Sending post request to collect the data
        response = requests.post(AJAX_URL, json=ajax_data, headers=ajax_headers)
        response.raise_for_status()

        # Load the results
        try:
            results = json.loads(response.text)
        except json.JSONDecodeError:
            logger.info("failed to parse server response")

        company = results[0]["result"]["result"]

        # Check if organization object contains number field
        for key in config.FIELDS.keys():
            field = config.FIELDS[key]
            if field == config.ORG_DESCRIPTION_FIELD:
                if config.ORG_DESCRIPTION_FIELD in company.keys():
                    company_information[key] = company[
                        config.ORG_DESCRIPTION_FIELD
                    ].get("description", None)
            else:
                company_information[key] = company.get(field, None)
        return company_information

    def handle(self, *args, **options):
        self.fetch(options["csv"])

    def fetch(self, should_write_csv):
        """
        :bool should_write_csv: wheather to write to a csv file or not (i.e., dump to DB)
        """
        # Calculates the amount of queries should be done in order to collect all IDs
        total_results = self.get_total_results_from_guidestar()
        logger.info("{} results found".format(total_results))
        num_of_iterations = int(total_results / config.RESULTS_PER_PAGE + 1)

        # Run for each page between 1, (total_iteration / per_page_results) + 1
        logger.info("total iterations: {}".format(num_of_iterations))
        companies_ids = self.collect_ids_from_guidestar(num_of_iterations)

        # In case the user asked to write results to local csv
        if should_write_csv:
            fieldnames = [
                "organization_number",
                "email",
                "description",
                "website_url",
                "name",
                "goal",
                "year_founded",
                "status",
                "target_audience",
                "number_of_employees",
                "number_of_members",
                "number_of_volunteers",
                "location_lon",
                "location_lat",
                "address_city",
                "address_street",
                "address_house_num",
                "address_zipcode",
                "cities",
                "districts",
                "union_type",
            ]
            csv_file = open("organizations.csv", "w", encoding="UTF-8")
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

        # For each IP create the object
        for _id in companies_ids:
            org_data = self.collect_company_information(_id)
            if org_data["cities"] is not None:
                org_data["cities"] = ",".join(org_data["cities"])
            if org_data["districts"] is not None:
                districts = org_data["districts"]
                districts = districts.replace('"', "").replace("'", "")
                districts = districts.replace("[", "").replace("]", "").split(",")
                org_data["districts"] = districts

            if should_write_csv:
                csv_writer.writerow(org_data)
                csv_file.flush()

            else:
                ImportedOrganization.objects.update_or_create(
                    defaults=org_data,
                    organization_number=org_data["organization_number"],
                )
