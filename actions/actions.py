# This files contains your custom actions which can be used to run
# custom Python code.
from datetime import datetime, timedelta
from typing import Any, Text, Dict, List, Union

import spacy
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from acces_data_layer.models.models import RelOldPersonMedicine
from acces_data_layer.services.medicine_service import select_by_name
from acces_data_layer.services.r_old_person_medicine_service import (select_by_ids_hour, select_by_id_op_hour,
                                                                     insert, update)
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


def sentence_builder(
        dict_message: dict,
        index_value: str,
        medicine: str,
        medication_hour: List = None
) -> dict:
    """
    Constructs a phrase in Spanish mentioning a medicine and when to take it.

    Args:
        dict_message: The name of the medicine.
        index_value: The name of the medicine.
        medicine: The name of the medicine.
        medication_hour: The date and time when the medicine should be taken.

    Returns:
        The initial message string with an additional phrase appended
        mentioning the medicine name, time to take it, and proper Spanish
        gender article.
    """
    gender = get_gender(medicine)
    article = "" if not gender else "la " if gender == "Fem" else "el "
    amount_medicines = len(medication_hour)

    if index_value == "take":
        for i, med in enumerate(medication_hour, start=1):
            if 1 < i < amount_medicines:
                dict_message[index_value][medicine] += f", a {tell_time(med)}"
            elif i == 1:
                if dict_message[index_value]:
                    dict_message[index_value][medicine] = f"{article}{medicine} a {tell_time(med)}"
                else:
                    dict_message[index_value][medicine] = f"Tienes que tomar {article}{medicine} a {tell_time(med)}"
            else:
                dict_message[index_value][medicine] += f" y a {tell_time(med)}"
    else:
        if dict_message[index_value]:
            dict_message[index_value] += f", ni {medicine}"
        elif index_value == "not_take":
            dict_message[index_value] = f"No tines que tomar {medicine}"
        else:
            dict_message[index_value] = f"No conozco la medicina {medicine}"

    return dict_message


def sentence_finisher(sentences: Union[dict, str]) -> str:
    message = ""
    length = len(sentences)

    for i, sentence in enumerate(iterable=sentences.values(), start=1):
        if i != length:
            message += f"{sentence}, "
        elif length == 1:
            message = f"{sentence}."
        else:
            message += f"y {sentence}"

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
        return "action_consult_an_specific_medicine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id_old_person = int(tracker.sender_id)
        current_medicines = tracker.get_slot("medicines")
        dict_message = {
            "take": {},
            "not_take": '',
            "unknown": ''
        }

        if current_medicines:
            for medicine in current_medicines:
                id_medicine = select_by_name(medicine_name=medicine)

                if id_medicine:
                    current_hour = datetime.now()
                    medication_hour = select_by_ids_hour(id_op=id_old_person, id_med=id_medicine, hour=current_hour)

                    if medication_hour:
                        dict_message = sentence_builder(
                            dict_message=dict_message,
                            index_value="take",
                            medicine=medicine,
                            medication_hour=medication_hour
                        )
                    else:
                        dict_message = sentence_builder(
                            dict_message=dict_message,
                            index_value="not_take",
                            medicine=medicine
                        )
                else:
                    dict_message = sentence_builder(
                        dict_message=dict_message,
                        index_value="unknown",
                        medicine=medicine
                    )

            message = sentence_finisher(sentences=dict_message["take"])

            message += dict_message["not_take"]
            message += dict_message["unknown"]
        else:
            message = f"No conozco esa medicina."

        dispatcher.utter_message(text=message)

        return [SlotSet("medicines", None)]


class ActionConsultMedications(Action):
    def name(self) -> Text:
        return "action_consult_medicines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id_old_person = int(tracker.sender_id)
        dict_message = {
            "take": {}
        }
        current_hour = datetime.now()
        end_hour = current_hour + timedelta(hours=12)
        current_medicines = select_by_id_op_hour(
            id_op=id_old_person, start_hour=current_hour, end_hour=end_hour
        )

        for medicine, medication_hour in current_medicines:
            dict_message = sentence_builder(
                dict_message=dict_message,
                index_value="take",
                medicine=medicine,
                medication_hour=[medication_hour]
            )

        message = sentence_finisher(sentences=dict_message["take"])

        dispatcher.utter_message(text=message)

        return []


class ActionSaveMedication(Action):
    def name(self) -> Text:
        return "action_save_medication_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id_old_person = int(tracker.sender_id)
        medicines = tracker.get_slot("medicines")
        times = tracker.get_slot("time")

        for i, medicine in enumerate(iterable=medicines):
            id_medication = select_by_name(medicine_name=medicine)
            time_object = datetime.strptime(times[i], "%Y-%m-%dT%H:%M:%S")

            insert(
                op_med_data=RelOldPersonMedicine(
                    id_old_person=id_old_person,
                    id_medicine=id_medication,
                    medicine_hour=time_object
                )
            )

        dispatcher.utter_message(text="Te lo recordaré")

        return [SlotSet("medicines", None), SlotSet("time", None)]


class ActionHandleReminder(Action):
    def name(self) -> Text:
        return "action_handle_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Action Handle Reminder")
        medicine = next(tracker.get_latest_entity_values("medicine"), "algo")
        medicine_hour_str = next(tracker.get_latest_entity_values("medicine_hour"), "en algun momento")
        medicine_hour = datetime.strptime(medicine_hour_str, "%Y-%m-%dT%H:%M:%S")

        dispatcher.utter_message(text=f"Recuerda tomar {medicine} a {tell_time(hour_to_convert=medicine_hour)}")

        return [SlotSet("medicines", None), SlotSet("medicine", None), SlotSet("medicine_hour", None)]


class ActionHandleVerifier(Action):
    def name(self) -> Text:
        return "action_set_medicine_taken_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Action Set Slots")
        medicine_hour_str = next(tracker.get_latest_entity_values("medicine_hour"), "en algun momento")
        medicine_name = next(tracker.get_latest_entity_values("medicine"), "algo")
        medicine_hour = datetime.strptime(medicine_hour_str, "%Y-%m-%dT%H:%M:%S")
        medicine_hour_tts = tell_time(medicine_hour)

        return [
            SlotSet("medicine", medicine_name),
            SlotSet("medicine_hour_tts", medicine_hour_tts),
            SlotSet("medicine_hour", medicine_hour_str)
        ]


class ActionUpdateStatus(Action):
    def name(self) -> Text:
        return "action_update_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Action Update Status")
        id_old_person = int(tracker.sender_id)
        medicine_hour_str = tracker.get_slot("medicine_hour")
        medicine_hour = datetime.strptime(medicine_hour_str, "%Y-%m-%dT%H:%M:%S")
        medicine_name = tracker.get_slot("medicine")
        id_medicine = select_by_name(medicine_name=medicine_name)
        relation = {
            "current_state": {
                "id_old_person": id_old_person,
                "id_medicine": id_medicine,
                "medicine_hour": medicine_hour
            },
            "next_state": {
                "id_old_person": id_old_person,
                "id_medicine": id_medicine,
                "medicine_hour": medicine_hour,
                "status": "completado"
            }
        }

        update(op_med=relation)

        return [
            SlotSet("medicine", None),
            SlotSet("medicine_hour_tts", None),
            SlotSet("medicine_hour", None)
        ]
