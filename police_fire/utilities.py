# contains helper functions that are useful for both structured and unstructured data.
import os
import re

from simpleaichat import AIChat

from database import IncidentsWithErrors, Incidents, Article


def delete_table_contents(DBsession):
    DBsession.query(IncidentsWithErrors).delete()
    DBsession.query(Incidents).delete()
    DBsession.query(Article).delete()
    DBsession.commit()

    return


def add_incident_with_error_if_not_already_exists(article, DBsession):
    if DBsession.query(IncidentsWithErrors).filter_by(article_id=article.id).count() == 0:
        incidentWithError = IncidentsWithErrors(
            article_id=article.id,
            url=article.url
        )
        DBsession.add(incidentWithError)
        DBsession.commit()

    return


def clean_up_charges_details_and_legal_actions_records(charges_str, details_str, legal_actions_str):
    if charges_str.startswith(': '):
        charges_str = charges_str[2:]
    else:
        charges_str = charges_str.replace('Charges: ', '')
    if details_str.startswith(': '):
        details_str = details_str[2:]
    else:
        details_str = details_str.replace('Details: ', '')
    if legal_actions_str.startswith(': '):
        legal_actions_str = legal_actions_str[2:]
    else:
        legal_actions_str = re.sub(r'Legal [Aa]ctions: ', '', legal_actions_str)

    return charges_str, details_str, legal_actions_str


ai = AIChat(
    console=False,
    save_messages=False,  # with schema I/O, messages are never saved
    model="gpt-4",
    params={"temperature": 0.0},
    api_key=os.getenv('OPENAI_API_KEY'),
)


def search_for_day_of_week_in_details(details_str):
    """if the details contain a day of the week, return the day that matched"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        if day in details_str:
            return day


def get_last_date_of_day_of_week_before_date(day_of_week, date):
    # find the last time that day of the week occurred before the date
    query = "What was the last time that " + day_of_week + " occurred before " + str(
        date) + "? Return only the date. If none, return N/A."
    response = ai(query)
    return response


def check_if_details_references_a_relative_date(details_str, incident_reported_date):
    day_in_incident_details = search_for_day_of_week_in_details(details_str)
    if day_in_incident_details is None:
        return None
    # if day_in_incident_details is not None, find the last time that day of the week occurred before the
    # incident_reported_date.
    response = get_last_date_of_day_of_week_before_date(day_in_incident_details, incident_reported_date)

    return response


def check_if_details_references_an_actual_date(details_str, article_published_date):
    """if the details contain a date, return the date that matched + the year the article was published"""
    query = f"What was the date of the incident: {details_str}? Return only the date as YYYY-MM-DD. Use the year in the article published date as the year: {article_published_date}"
    response = ai(query).split()[-1]
    # if the format of response is not like YYYY-MM-DD, return None
    if len(response) != 10:
        return None

    return response


def update_incident_date_if_necessary(DBsession, incident_date_response, details_str):

    existing_incident = DBsession.query(Incidents).filter_by(details=details_str).first()
    if existing_incident:
        existing_incident.incident_date = incident_date_response
        DBsession.add(existing_incident)
        DBsession.commit()
        print('Incident date updated for ' + existing_incident.url)

    return