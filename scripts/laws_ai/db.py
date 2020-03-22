# Projeto IALEIS
# Author: Antonio M. Ferreira, Feb/2020
# amfcode@gmail.com

from pymongo import MongoClient
from datetime import date
import laws_ai.helpers as helpers

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(
    "mongodb://localhost:27017/laws?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
db = client.laws_ai


def last_unread_link():
    return db.links.find(
        {'visited_count': 0, "url": {"$regex": ".*Lei.*"}}
    ).sort("law_code")[0]


def base():
    return db


def unread_links(limit):
    return db.links.aggregate([
        #{"$match": {'visited_count': 0, "url": {"$regex": ".*Lei.*"}}},
        {"$match": {'visited_count': 0}},
        {"$sample": {"size": limit}}
    ])


def remove_links_by(i):
    reset_link(i)
    db.links.delete_many({"url":  {"$regex": ".*" + i + ".*"}})


def add_law(law):
    exist = db.laws.find_one(law)
    if not exist:
        result = db.laws.insert_one(law)
        return result.inserted_id


def add_date(date):
    exist = db.dates.find_one(date)
    if not exist:
        result = db.dates.insert_one(date)
        return result.inserted_id


def add_published_fact(published_fact):
    exist = db.published_laws.find_one(published_fact)
    if not exist:
        db.published_laws.insert_one(published_fact)


def add_tables(tables):
    exist = db.tables.find_one(tables)
    if not exist:
        result = db.tables.insert_one(tables) 
        return result.inserted_id


def add_current_fact(current_fact):
    exist = db.published_laws.find_one(current_fact)
    if not exist:
        db.published_laws.insert_one(current_fact)


def add_text(text):
    exist = db.texts.find_one(text)
    if not exist:
        result = db.texts.insert_one(text)
        return result.inserted_id


def link_readed(link, law_code, time_used):
    link_law_code = link_to_law_code(link)
    exist = link_exist(link)
    visited_at = date.today().strftime("%d/%m/%Y")
    visited_count = 1
    if not exist:
        return add_link(link, law_code, visited_count, visited_at, time_used)
    else:
        db.links.update_one(
            {'law_code': link_law_code},
            {"$set": {'visited_at': visited_at, 'visited_count': 1,
                      'time_used': time_used}}
        )
        return exist["_id"]


def link_readed_with_error(link, error):
    link_law_code = link_to_law_code(link)
    db.links.update_one(
        {'law_code': link_law_code},
        {"$set": {'visited_at': date.today().strftime("%d/%m/%Y"),
                  'error':  str(error),
                  'visited_count': 1}}
    )


def add_link(link, law_code, visited_count=0, visited_at=None, time_used=None):
    referenced_in = []
    link_law_code = link_to_law_code(link)
    exist = link_exist(link)
    if not exist:
        referenced_in = [law_code]
        data_link = {
            'law_code': link_law_code, 'url': link, 'visited_at': None,
            'visited_count': 0, 'referenced_in': referenced_in,
            'time_used': time_used
        }
        result = db.links.insert_one(data_link)
        return result.inserted_id

# Helpers


def link_to_law_code(link):
    link_arr = link.split("/")[-1]
    if link_arr:
        link_arr = link_arr.replace(".htm", "")
        link_arr = link_arr.replace("_", "")
        return link_arr

    return ''


def link_exist(link):
    law_code = link_to_law_code(link)
    return link_by_law_code(law_code)


def link_visited(link):
    exist = link_exist(link)
    return (exist and exist['visited_count'] > 0)


def link_by_law_code(law_code):
    return db.links.find_one({"law_code": law_code})


def reset_links():
    db.links.update_many(
        {}, {"$set": {"visited_at": "", "visited_count": 0, "error": ''}})
    db.laws.drop()
    db.published_laws.drop()
    db.texts.drop()
    db.dates.drop()


def reset_reads():
    db.laws.drop()
    db.published_laws.drop()
    db.texts.drop()
    db.dates.drop()
    db.tables.drop()


def reset_link(link):
    link_law_code = link_to_law_code(link)
    db.links.update({"law_code": link_law_code},
                    {"$set": {"visited_at": "", "visited_count": 0}})

    laws_id = db.laws.find_one({"law_code": link_law_code})
    if laws_id:
        db.laws.delete_many({"law_code": link_law_code})
        db.published_laws.delete_many({"law": laws_id["_id"]})
        db.texts.delete_many({"law_code": link_law_code})
