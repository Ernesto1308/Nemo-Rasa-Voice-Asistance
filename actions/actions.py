# This files contains your custom actions which can be used to run
# custom Python code.
from datetime import datetime, timedelta
from typing import Any, Text, Dict, List

import spacy
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from acces_data_layer.services.medicine_service import select_by_name
from acces_data_layer.services.r_old_person_medicine_service import select_by_ids_hour, select_by_op_id
from actions import numbers


def tell_time(hour_to_convert: datetime) -> str:
    """
    Converts a datetime object to a string describing the time in Spanish.

    Args:
        hour_to_convert: The datetime object with the hour to convert.

    Returns:
        A string expressing the time in Spanish using common conventions.
    """

    # handle hours mayor than 12
    if hour_to_convert.hour > 12:
        current_hour = hour_to_convert.hour - 12
    # handle hour 0
    elif hour_to_convert.hour == 0:
        current_hour = 12
    else:
        current_hour = hour_to_convert.hour

    current_minute = hour_to_convert.minute
    meridiem = hour_to_convert.strftime('%p')
    time_of_day = 'mañana' if meridiem == 'AM' and current_hour != 12 else 'tarde' if current_hour < 7 else 'noche'

    # handle edge cases for hours 1 and o'clock
    if current_hour == 1 and current_minute == 0:
        hour_to_string = f'la una de la {time_of_day}'
    elif current_hour == 1:
        hour_to_string = f'la una y {numbers[current_minute]} de la {time_of_day}'
    # handle case for o'clock
    elif current_minute == 0:
        hour_to_string = f'las {numbers[current_hour]} de la {time_of_day}'
    # handle cases for minutes past the hour
    else:
        hour_to_string = f'las {numbers[current_hour]} y {numbers[current_minute]} de la {time_of_day}'

    return hour_to_string


def get_gender(noun: str) -> str:
    """
    Determines the grammatical gender of the given Spanish noun.

    Args:
        noun: The noun to analyze.

    Returns:
        A list containing the identified grammatical gender of the noun,
        either 'Masc' for masculine or 'Fem' for feminine.
        Returns an empty list if unable to determine gender.
    """

    nlp = spacy.load("es_core_news_sm")
    doc = nlp(noun)
    token = doc[0]

    gender = token.morph.get("Gender")

    return gender


def sentence_builder(medicine: str, medication_hour: datetime, message: str) -> str:
    """
    Constructs a phrase in Spanish mentioning a medicine and when to take it.

    Args:
        medicine: The name of the medicine.
        medication_hour: The date and time when the medicine should be taken.
        message: The initial message string.

    Returns:
        The initial message string with an additional phrase appended
        mentioning the medicine name, time to take it, and proper Spanish
        gender article.
    """

    gender = get_gender(medicine)
    article = "" if not gender else "la" if gender == "Fem" else "el"
    message += f"Tienes que tomar {article} {medicine} a {tell_time(medication_hour)}. "

    return message


class ActionTellTime(Action):
    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f"Son {tell_time(hour_to_convert=datetime.now())}")

        return []


class ActionSpecificMedication(Action):
    def name(self) -> Text:
        return "action_consult_an_specific_medication"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id_old_person = int(tracker.sender_id)
        current_medicines = tracker.get_slot("medicines")
        message = ""

        if current_medicines:
            for medicine in current_medicines:
                id_medicine = select_by_name(medicine=medicine)

                if id_medicine:
                    current_hour = datetime.now()
                    medication_hour = select_by_ids_hour(id_op=id_old_person, id_med=id_medicine, hour=current_hour)

                    if medication_hour:
                        message = sentence_builder(medicine=medicine, medication_hour=medication_hour, message=message)
                    else:
                        message += f"No tienes que tomar {medicine} hoy. "
                else:
                    message += f"No conozco la medicina {medicine}. "
        else:
            message += f"No conozco esa medicina."

        dispatcher.utter_message(text=message)

        return [SlotSet("medicines", None)]


class ActionConsultMedications(Action):
    def name(self) -> Text:
        return "action_consult_medications"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id_old_person = int(tracker.sender_id)
        message = ""
        current_hour = datetime.now()
        end_hour = current_hour + timedelta(hours=12)
        current_medicines = select_by_op_id(
            id_op=id_old_person, start_hour=current_hour, end_hour=end_hour
        )

        for medicine_name, medicine_hour in current_medicines:
            message = sentence_builder(medicine=medicine_name, medication_hour=medicine_hour, message=message)

        dispatcher.utter_message(text=message)

        return []
