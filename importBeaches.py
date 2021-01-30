import json

import os

from cs50 import SQL


# ONLY USED TO IMPORT BEACH LOCATIONS INTO SQL DATABASE


# with open('bnlocationsMaster(noNYnoCA).json') as json_file:
#     data = json.load(json_file)


# db = SQL("sqlite:///beaches.db")
# for row in data:
#     name = row['Location']
#     state = row['State']
#     lat = row['Latitude']
#     lon = row['Longitude']
#     notes = row['Primary Funding Source']
#     db.execute("INSERT INTO beaches2 (name, latitude, longitude, state, notes) VALUES (?, ?, ?, ?, ?);",
#         name, lat, lon, state, notes)