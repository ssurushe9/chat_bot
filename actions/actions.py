# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from twilio.rest import Client
from rasa_sdk.events import SlotSet
import random
from database import insert_data


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionExtractName(Action):
    def name(self) -> Text:
        return "action_extract_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List:
        metadata = tracker.get_slot("name")


        # name = next(tracker.get_latest_entity_values("name"), None)
        # if name:
        #     return [("name", name)]
        # else:
        dispatcher.utter_message(template=f"Hi {metadata}, how can i help you")
        return []


class ActionExtractNumber(Action):
    def name(self) -> Text:
        return "action_extract_number"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List:
        phone_number = next(tracker.get_latest_entity_values("phone_number"), None)

        if phone_number:
            return [("user_contact_no", phone_number)]
        else:
            dispatcher.utter_message(template="utter_not_extract_number")
            return []


class ActionSendOTP(Action):

    def name(self) -> Text:
        return "action_send_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the user's phone number from the tracker
        phone_number = tracker.get_slot("user_contact_no")
        if phone_number is None:
            return [SlotSet("user_contact_no", None),SlotSet("otp", None)]


        # Generate the OTP
        global otp1
        otp1 = generate_otp()
        print(otp1)

        # Send the OTP to the user's phone number via Twilio SMS API
        account_sid = 'AC99d07aa2c50036d5d7a94c7cac155838'
        auth_token = '31bfec3dec3d2e9065b188f8c2aaeedf'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f'Your OTP is {otp1}',
            from_='+18104840680',
            to=phone_number
        )
        print(message.sid)

        # Set the OTP in the tracker
        # tracker.slots["otp1"] = otp

        # Ask the user to input the OTP
        message = "An OTP has been sent to your mobile number. Please input the OTP to proceed."
        dispatcher.utter_message(text=message)

        return []

def generate_otp():
    return random.randint(100000, 999999)

class ActionVerifyOTP(Action):

    def name(self) -> Text:
        return "action_verify_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the user's input for the OTP
        user_otp = tracker.get_slot("otp")
        print(type(user_otp))

        # Get the OTP that was sent
        # sent_otp = tracker.get_slot("otp1")
        print(type(otp1))

        # Compare the user's input to the sent OTP
        if int(user_otp) == otp1:
            insert_data(tracker.get_slot("name"),tracker.get_slot("user_contact_no"))
            message = "Your mobile number verified successfully."
            dispatcher.utter_message(text=message)
        else:
            message = "The OTP is incorrect. Please input the correct OTP to proceed."
            dispatcher.utter_message(text=message)

        return []

class ActionAskLoanType(Action):

    def name(self):
        return "action_save_type_loan"

    def run(self, dispatcher, tracker, domain):
        user_loan = tracker.get_slot("user_loan")

        user_name = tracker.get_slot("name")
        loan_type = tracker.get_slot("loan_type")
        if user_name == 'Car_loan':
            message = f"Please Fill above form : https://www.axisbank.com/retail/calculators/car-loan-emi-calculator" \
                      f" \nOur agent will connect you shortly : {user_name} for request of {loan_type}"
            # dispatcher.utter_message(text=message)
        if user_name == 'Home_loan':
            message = f"Please Fill above form : https://www.bankbazaar.com/home-loan-interest-rate.html \nO" \
                      f"ur agent will connect you shortly : {user_name} for request of {loan_type}"
            # dispatcher.utter_message(text=message)
        if user_name == 'Personal_loan':
            message = f"Please Fill above form : https://www.bankbazaar.com/personal-loan-interest-rate.html" \
                      f" \nOur agent will connect you shortly : {user_name} for request of {loan_type}"
            # dispatcher.utter_message(text=message)

        message = f"Please Fill above form : https://www.bankbazaar.com/personal-loan-interest-rate.html" \
                  f" \nOur agent will connect you shortly : {user_name} for request of {loan_type}"
        # dispatcher.utter_message(text=message)
        dispatcher.utter_message(text="Thanks for confirmation..")

        # dispatcher.utter_message(response='utter_reply_loan')
        return [SlotSet("loan_type", value=loan_type)]

# class ActionSaveProfession(Action):
#     def name(self) -> Text:
#         return "action_save_profession"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         profession = tracker.get_slot("profession")
#
#         return [SlotSet("profession", value=profession)]

class ActionSaveEmployed(Action):
    def name(self) -> Text:
        return "action_save_employed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        employed = tracker.get_slot("employed")

        return [SlotSet("employed", value=employed)]