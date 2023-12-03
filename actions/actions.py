# This files contains your custom actions which can be used to run
# custom Python code.
from datetime import datetime
from datetime import timedelta
from typing import Any, Text, Dict
from typing import List

import spacy
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, ReminderScheduled
from rasa_sdk.executor import CollectingDispatcher

from acces_data_layer.models.models import RelOlderPersonMedicine
from acces_data_layer.services.medicine_service import select_by_name
from acces_data_layer.services.r_older_person_medicine_service import (select_by_ids_major_hour,
                                                                       get_medicine_schedule,
                                                                       select_by_ids_hour,
                                                                       insert, update)
from utils import numbers


def tell_time(hour_to_convert: datetime) -> str:
    """
    Converts a datetime object to a string describing the time in Spanish.

    Args:
        hour_to_convert: The datetime object with the hour to convert.

    Returns:
        A string expressing the time in Spanish using common conventions.
    """
    part_of_day = get_part_of_day(hour_to_convert)
    current_hour = int(hour_to_convert.strftime('%I'))
    current_minute = hour_to_convert.minute
    current_minutes_str = ''

    if current_minute != 0:
        current_minutes_str = f' y {numbers[current_minute]}'

    if current_hour != 1:
        current_hour_str = f'las {numbers[current_hour]}'
    else:
        current_hour_str = 'la una'

    return f'{current_hour_str}{current_minutes_str}{part_of_day}'


def get_part_of_day(hour: datetime) -> str:
    """
        Get the time of day in Spanish based on the hour of the day.
        Args:
            hour: The datetime object with the hour to convert.
        Returns:
            A string expressing the time of day in Spanish.
    """
    current_hour = hour.hour

    # Determine the time of day based on the hour
    if 0 < current_hour < 12:
        part_of_day = ' de la mañana'
    elif 12 < current_hour < 19:
        part_of_day = ' de la tarde'
    elif current_hour >= 19 or current_hour == 0:
        part_of_day = ' de la noche'
    else:
        part_of_day = ' del mediodia'

    return part_of_day


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
    result = token.morph.get("Gender")
    gender = result[0] if result else None

    return gender


def article_to_medicine(medicine: str) -> str:
    """
    Prefix the article for a given medicine name.

    Args:
        medicine: The name of the medicine.

    Returns:
        The article and medicine name concatenated.
    """
    if get_gender(medicine) == 'Fem':
        article = 'la '
    elif get_gender(medicine) == 'Masc':
        article = 'el '
    else:
        article = ''

    return f'{article}{medicine}'


def format_list_naturally(list_items: List[str]) -> str:
    """
    Formats a list of strings to a string where the items are naturally joined with commas and 'y'.

    Args:
        list_items: A list of strings to be formatted.

    Returns:
        A string with joined list items in a naturally readable format in Spanish.

    Usage:
        format_list_naturally(['8 de la mañana', '2 de la tarde', '6 de la tarde'])
        '8 de la mañana, 2 de la tarde y 6 de la tarde'
    """
    length = len(list_items)

    if length > 2:
        formatted_string = f"{', '.join(list_items[:-1])} y {list_items[-1]}"
    elif length == 2:
        formatted_string = ' y '.join(list_items)
    else:
        formatted_string = list_items[0]

    return formatted_string


def create_single_medicine_phrase(medicine: str, hours: List[datetime]) -> str:
    """
    Constructs a natural language phrase in Spanish stating when to take a specific medicine.

    Args:
        medicine: The name of the medicine.
        hours: A list of datetime objects indicating when the medicine should be taken.

    Returns:
        A string formatted in a human-like style in Spanish telling when to take the given medicine.

    Usage:
        create_take_medicine_phrase('Paracetamol', [datetime(2022,6,1,8), datetime(2022,6,1,14), datetime(2022,6,1,18)])
        "Tienes que tomar el Paracetamol a las 8 de la mañana, a las 2 de la tarde y a las 6 de la tarde."
    """
    medicine = article_to_medicine(medicine)
    formatted_hours = [f'a {tell_time(hour)}' for hour in hours]
    formatted_hours_string = format_list_naturally(formatted_hours)
    phrase = f'{medicine} {formatted_hours_string}'

    return phrase


def create_combined_medicine_phrase(single_medicine_phrases: List[str]) -> str:
    """
    Constructs a natural language phrase in Spanish stating when to take multiple medicines.

    Args:
        single_medicine_phrases: A list of string with all the information.

    Returns:
        A string formatted in a human-like style in Spanish telling when to take the given medicines.

    Usage: create_combined_medicine_phrase([ 'el Paracetamol a las 8 de la mañana, a las 2 de la tarde y a las 6 de
    la tarde', 'la Duralgina a las 8 de la día, a las 2 de la tarde y a las 6 de la tarde']) "Tienes que tomar el
    Paracetamol a las 8 de la mañana, a las 2 de la tarde y a las 6 de la tarde y Duralgina a las 8 de la mañana,
    a las 2 de la tarde y a las 6 de la tarde."
    """
    phrase = f'Tienes que tomar {format_list_naturally(single_medicine_phrases)}'
    return phrase


def create_not_take_phrase(medicines: List[str]) -> str:
    """
        Formats a list of strings to a string where the items are naturally joined with commas and 'ni'.

        Args:
            medicines: A list with the names of the medicines.

        Returns:
            A string with joined list items in a naturally readable format in Spanish.

        Usage:
            format_list_naturally(['Paracetamol', 'Duralgina', 'Ibuprofeno'])
            'No tienes que tomar Paracetamol, ni Duralgina, ni Ibuprofeno'
        """
    length = len(medicines)

    message = f"No tienes que tomar {medicines[0]}"

    if length > 1:
        message += f"{', ni '.join(medicines[1:])}"

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
        id_older_person = int(tracker.sender_id)
        current_medicines = tracker.get_slot("medicines")
        messages_list = []
        message_not_take = []
        message = ''

        if current_medicines:
            for medicine in current_medicines:
                id_medicine = select_by_name(medicine_name=medicine)

                if id_medicine:
                    current_hour = datetime.now()
                    medication_hour = select_by_ids_major_hour(id_op=id_older_person, id_med=id_medicine,
                                                               hour=current_hour)
                    if medication_hour:
                        messages_list.append(
                            create_single_medicine_phrase(medicine=medicine, hours=medication_hour)
                        )
                    else:
                        message_not_take.append(medicine)
                else:
                    message = 'No conozco esa medicina'

        else:
            message = "No conozco esa medicina."

        if messages_list:
            message = create_combined_medicine_phrase(messages_list)

        if message_not_take:
            message += create_not_take_phrase(message_not_take)

        dispatcher.utter_message(text=message)

        return []


class ActionConsultMedications(Action):
    def name(self) -> Text:
        return "action_consult_medicines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id_older_person = int(tracker.sender_id)
        current_hour = datetime.now()
        end_hour = current_hour + timedelta(hours=12)
        current_medicines = get_medicine_schedule(
            id_op=id_older_person, start_hour=current_hour, end_hour=end_hour
        )
        message_list = []

        for medicine, medication_hour in current_medicines.items():
            message_list.append(create_single_medicine_phrase(medicine=medicine, hours=medication_hour))

        message = create_combined_medicine_phrase(message_list)

        dispatcher.utter_message(text=message)

        return []


class ActionSaveMedication(Action):
    def name(self) -> Text:
        return "action_save_medicine_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id_older_person = int(tracker.sender_id)
        medicines = tracker.get_slot("medicines")
        times = tracker.get_slot("time")
        before_reminder = {}
        in_time_reminder = {}
        verifier = {}

        for i, medicine in enumerate(iterable=medicines):
            id_medicine = select_by_name(medicine_name=medicine)
            time_object = datetime.strptime(times[i], '%Y-%m-%dT%H:%M:%S.%f%z').replace(microsecond=0, tzinfo=None)
            time_object_str = time_object.isoformat()
            time_object_tts = tell_time(hour_to_convert=time_object)

            insert(
                RelOlderPersonMedicine(
                    id_older_person=id_older_person,
                    id_medicine=id_medicine,
                    medicine_hour=time_object
                )
            )

            before_reminder = ReminderScheduled(
                intent_name="EXTERNAL_reminder",
                entities={
                    "medicine_name": medicine,
                    "medicine_hour_tts": time_object_tts,
                },
                trigger_date_time=time_object - timedelta(seconds=10),
                name=f'reminder {id_older_person}-{medicine}-{time_object_str}',
                kill_on_user_message=False,
            )

            in_time_reminder = ReminderScheduled(
                intent_name="EXTERNAL_reminder",
                entities={
                    "medicine_name": medicine,
                },
                trigger_date_time=time_object,
                name=f'reminder {id_older_person}-{medicine}',
                kill_on_user_message=False,
            )

            verifier = ReminderScheduled(
                intent_name="EXTERNAL_verifier",
                entities={
                    "medicine_name": medicine,
                    "medicine_hour": time_object_str,
                    "medicine_hour_tts": time_object_tts,
                },
                trigger_date_time=time_object + timedelta(seconds=10),
                name=f'verifier {id_older_person}-{medicine}-{time_object_str}',
                kill_on_user_message=False,
            )

        dispatcher.utter_message(text="Te lo recordaré")

        return [before_reminder, in_time_reminder, verifier]


class ActionHandleReminder(Action):
    def name(self) -> Text:
        return "action_handle_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Action Handle Reminder")
        print(tracker.slots)
        medicine_name = tracker.get_slot("medicine_name")
        medicine_hour_tts = tracker.get_slot("medicine_hour_tts")

        if medicine_hour_tts:
            message = f"Recuerda tomar {medicine_name} a {medicine_hour_tts}"
        else:
            message = f"Recuerda tomar {medicine_name} ahora"

        dispatcher.utter_message(text=message)

        return [SlotSet("medicine_hour_tts", None)]


class ActionUpdateStatus(Action):
    def name(self) -> Text:
        return "action_update_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Action Update Status")
        id_older_person = int(tracker.sender_id)
        medicine_taken = tracker.get_slot("medicine_taken")
        medicine_hour_str = tracker.get_slot("medicine_hour")
        medicine_hour = datetime.strptime(medicine_hour_str, "%Y-%m-%dT%H:%M:%S")
        medicine_name = tracker.get_slot("medicine_name")
        id_medicine = select_by_name(medicine_name=medicine_name)
        status = "Completado" if medicine_taken else "No completado"
        print(id_older_person, medicine_taken, medicine_name, medicine_hour)
        relation = select_by_ids_hour(id_op=id_older_person, id_med=id_medicine, hour=medicine_hour)
        relation.status = status

        update(relation)

        return [
            SlotSet("medicine_name", None),
            SlotSet("medicine_hour_tts", None),
            SlotSet("medicine_hour", None),
            SlotSet("medicine_taken", None)
        ]
