import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from database import Base, Incidents
from police_fire.scrape_structured_police_fire_details import scrape_structured_incident_details
from scrape_articles_by_section import scrape_article

from database import get_database_session, Article, AlreadyScrapedUrls
from utilities import login

database_username = os.getenv('DATABASE_USERNAME')
database_password = os.getenv('DATABASE_PASSWORD')


@pytest.fixture(scope="function")
def setup_database():
    # Connect to your test database
    engine = create_engine(
        f'postgresql+psycopg2://{database_username}:{database_password}@localhost:5432/cortlandstandard_test')
    Base.metadata.create_all(engine)  # Create tables

    # Create a new session for testing
    db_session = scoped_session(sessionmaker(bind=engine))

    yield db_session  # Provide the session for testing

    db_session.close()
    Base.metadata.drop_all(engine)  # Drop tables after tests are done


def test_add_structured_incident_with_multiple_people(setup_database):
    DBsession = setup_database
    article_url = "https://www.cortlandstandard.com/stories/motorcyclist-dies-on-i-81,60601?"
    logged_in_session = login()
    scrape_article(article_url, logged_in_session, section='Police/Fire', DBsession=DBsession)
    article_object = DBsession.query(Article).filter(Article.url == article_url).first()
    scrape_structured_incident_details(article_object, DBsession)

    incidents = DBsession.query(Incidents).all()

    last_incident = incidents[-1]
    assert last_incident.accused_name == 'Samuel J. Swan,Adrianne L. Wagoner'
    assert last_incident.accused_age == '47,40'
    assert last_incident.accused_location == 'N/A,Nye Road, Virgil'

