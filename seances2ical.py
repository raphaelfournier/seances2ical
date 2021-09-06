import os
import argparse
import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime


def transformDate(adate, heure):
    day, month, year = map(int, adate.split("/"))
    heures, minutes = map(int, heure.split("h"))
    dt = datetime(year, month, day, heures, minutes)
    return dt


class TeachingCal(object):
    def __init__(self):
        pass

    def createIcal(self, filename):
        cal = Calendar()
        cal.add('version', '2.0')

        df = pd.read_csv(filename, skiprows=[0])
        for index, row in df.iterrows():

            # skip lines with no date
            if pd.isna(row["date"]):
                continue

            # skip le 2nd header si le cours est sur deux semestres
            if row["date"] == "date":
                continue

            event = Event()

            # transformer la date
            date_debut = transformDate(row["date"], row["début"])
            date_fin = transformDate(row["date"], row["fin"])
            event.add('dtstart', date_debut)
            event.add('dtend', date_fin)

            # titre evenement
            titre = row["code UE"]+" "+row["type"]
            if not pd.isna(row["n"]):
                titre += " " + str(int(row["n"]))

            event["summary"] = titre

            # autres détails en description
            description = ""
            if not pd.isna(row["salle"]):
                description += "Salle : " + row["salle"]
            if not pd.isna(row["sujet"]):
                description += "\r\nSujet : " + row["sujet"]
            if not pd.isna(row["enseignant"]):
                description += "\r\nEnseignant : " + row["enseignant"]

            event["description"] = description

            cal.add_component(event)
        return cal.to_ical()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate ical calendars')
    parser.add_argument(
        '--csvfile',
        type=str,
        help='TODO')
    args = parser.parse_args()

    if not args.csvfile:
        csvfile = "charge.csv"  # default
    else:
        csvfile = args.csvfile

    if os.path.exists(csvfile):
        c = TeachingCal()
        moncal = c.createIcal(csvfile)
        print(moncal.decode('UTF-8'))
