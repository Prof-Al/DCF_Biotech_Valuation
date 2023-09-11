import pymongo
import pandas as pd
import time
from dash.dash_table import FormatTemplate

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(1)

default_regions = ["US", "Europe", "Rest of World"]
default_db = None


def refresh_db():
    global default_db
    start = time.time()
    client = pymongo.MongoClient(
        "mongodb+srv://dcf_admin:DnP3vf0EUD81mzHx@dcf-webapp.xsqti7v.mongodb.net/?retryWrites=true&w=majority")
    default_db = client["dcf_valuation"]
    print("Time taken: ", time.time() - start)


def format_to_millions(value):
    if type(value) in (int, float):
        if value == 0:
            return "-"
        return f"${value / 1_000_000:.1f}M"
    else:
        return value


def get_collection_as_df(name):
    collection = get_collection(name)
    df = pd.DataFrame(list(collection.find()))
    if not df.empty:
        df['_id'] = df['_id'].astype(str)
    return df


def get_collection(name):
    global default_db
    if default_db is None:
        refresh_db()

    collection = default_db[name]
    return collection

