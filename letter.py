import sys, os
import argparse

import lob
from lob.error import InvalidRequestError
from apiclient.discovery import build
from googleapiclient.errors import HttpError

class LetterGenerator(object):
    # static class error constants

    OK = 0
    LEGISLATOR_NO_ADDRESS = 400
    LEGISLATOR_NOT_FOUND = 404

    def __init__(self, args_dict):
        self.from_name = args_dict["name"]
        self.from_addr1 = args_dict["addr1"]
        self.from_addr2 = args_dict["addr2"]
        self.from_city = args_dict["city"]
        self.from_state = args_dict["state"]
        self.from_zip = args_dict["zip"]

        self.message = args_dict["message"]

        with open(args_dict["html"]) as html_file:
            self.html_string = html_file.read()

        self.lob_api_key = args_dict["lobkey"]
        lob.api_key = self.lob_api_key

        self.google_api_key = args_dict["googlekey"]
        self.civic_service = build('civicinfo', 'v2', developerKey=self.google_api_key)

    def generate_letter(self):
        from_address = self.create_address(name=self.from_name, address_line1=self.from_addr1, \
                            address_line2=self.from_addr2, address_city=self.from_city, \
                            address_state=self.from_state, address_zip=self.from_zip,
                            address_country="US")
        official = self.access_legislator_info()
        if(official is not None):
            self.to_name = official["name"]
            self.to_addr1 = official["address"][0]["line1"]
            self.to_addr2 = official["address"][0]["line2"] if "line2" in official["address"][0] else ""
            self.to_addr2 += (", " + official["address"][0]["line3"]) if "line3" in official["address"][0] else ""
            self.to_city = official["address"][0]["city"]
            self.to_state = official["address"][0]["state"]
            self.to_zip = official["address"][0]["zip"]

            to_address = self.create_address(name=self.to_name, address_line1=self.to_addr1, \
                                address_line2=self.to_addr2, address_city=self.to_city, \
                                address_state=self.to_state, address_zip=self.to_zip,
                                address_country="US")

            letter = self.create_letter(from_address, to_address)
            return letter["url"]
        elif(len(official["address"])):
            return LetterGenerator.LEGISLATOR_NO_ADDRESS
        else:
            return LetterGenerator.LEGISLATOR_NOT_FOUND

    def access_legislator_info(self):
        full_from_address = ""
        full_from_address += self.from_addr1 if self.from_addr1 else ""
        full_from_address += (", " + self.from_addr2) if self.from_addr2 else ""
        full_from_address += ", " + self.from_city
        full_from_address += ", " + self.from_state
        full_from_address += " " + self.from_zip
        # print "full_from_address:", full_from_address
        request = self.civic_service.representatives().representativeInfoByAddress(
                levels=["country"], roles=["legislatorLowerBody", "legislatorUpperBody"], \
                address=full_from_address, includeOffices=None)
        try:
            response = request.execute()
            if(len(response['officials']) > 0):
                official = response['officials'][0]
            else:
                official = None

            return official

        except HttpError as e:
            # print "Error,", e.resp.status
            # print "Reason:", e._get_reason().strip()
            return None

    def create_address(self, name, address_line1, address_line2, address_city, address_state, address_zip, address_country="US", description=None):
        # Creating an Address Object
        address = lob.Address.create(
            name = name,
            description = description,
            address_line1 = address_line1,
            address_line2 = address_line2,
            address_city = address_city,
            address_state = address_state,
            address_country = address_country,
            address_zip = address_zip
        )

        return address

    def create_letter(self, from_address, to_address):
        # Creating a Letter
        letter = lob.Letter.create(
            description = 'Letter to legislator',
            to_address = to_address,
            from_address = from_address,
            file = self.html_string,
            data = {
                "message": self.message,
                "your_name": self.from_name,
                "official_name": self.to_name
            },
            color = True
        )

        return letter


if __name__ == "__main__":
    program_name = sys.argv[0]

    parser = argparse.ArgumentParser(description='Generate a letter PDF using Lob API')
    parser.add_argument("-name", required=True, help='Your name')
    parser.add_argument("-addr1", required=True, help='Your address line 1')
    parser.add_argument("-addr2", help='Your address line 2')
    parser.add_argument("-city", required=True, help='Your city')
    parser.add_argument("-state", required=True, help='Your state')
    parser.add_argument("-zip", required=True, help='Your address zip code')
    parser.add_argument("-message", required=True, help='Your message to legislator')
    parser.add_argument("-html", default="index.html", help='The html template for the letter, default to be index.html')
    parser.add_argument("-lobkey", default="test_a1418fba3569832462d2c08d24cf03248b8", help='Lob API key, default to be Simon\'s key')
    parser.add_argument("-googlekey", default="AIzaSyBqrexHwjVA2hgS81GyqjU8vzRMiesc8vU", help='Google Civic API key, default to be Simon\'s key')

    args_dict = vars(parser.parse_args())

    letter_gen = LetterGenerator(args_dict)
    result = letter_gen.generate_letter()
    if(type(result) is unicode or type(result) is str):
        print "The PDF file of the letter is at:", result
    elif(result == LetterGenerator.LEGISLATOR_NO_ADDRESS):
        print "The legislator has no address"
    elif(result == LetterGenerator.LEGISLATOR_NOT_FOUND):
        print "No legislator is found given the information"










