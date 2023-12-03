from datetime import datetime
from typing import List

import spacy

from actions.actions import numbers


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


if __name__ == "__main__":
    paracetamol = create_single_medicine_phrase('Ibuprofeno', [
        datetime(2022, 6, 1, 0),
        datetime(2022, 6, 1, 10),
        datetime(2022, 6, 1, 12),
        datetime(2022, 6, 1, 12, 20),
        datetime(2022, 6, 1, 13),
        datetime(2022, 6, 1, 13, 20),
        datetime(2022, 6, 1, 16, 20),
        datetime(2022, 6, 1, 19, 20),
    ])

    print(create_combined_medicine_phrase([paracetamol]))
