# This files contains your custom actions which can be used to run
# custom Python code.
import base64
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
from actions import numbers
from acces_data_layer.services.r_old_person_medicine_service import select_by_ids_hour
from acces_data_layer.services.medicine_service import select_by_name
import spacy


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
        current_medicine = next(tracker.get_latest_entity_values("medication"), None)

        if current_medicine:
            id_medicine = select_by_name(medicine=current_medicine)
            gender = get_gender(current_medicine)
            current_hour = datetime.now()
            medication_hour = select_by_ids_hour(op_id=id_old_person, med_id=id_medicine, hour=current_hour)
            print(gender)

            if medication_hour:
                article = "" if not gender else "la" if gender == "Fem" else "el"
                message = f"Tienes que tomar {article} {current_medicine} a {tell_time(medication_hour)}"
            else:
                message = f"No tienes que tomar {current_medicine} hoy"
        else:
            message = "No conozco esa medicina"

        dispatcher.utter_message(text=message)

        return []


class ActionConsultMedications(Action):
    def name(self) -> Text:
        return "action_consult_medications"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # medication = next(tracker.get_latest_entity_values("medication"), None)
        # medication = tracker.get_slot("medicines")
        current_medicine = tracker.get_latest_entity_values("medicine")

        # dispatcher.utter_message(text=f"A las {medication}")

        return []
