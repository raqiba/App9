import requests
import selectorlib
import time
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    "User-Agent": 'Mozilla/5.0 '
                  '(Macintosh;'
                  ' Intel Mac OS X 10_10_1)'
                  ' AppleWebKit/537.36 '
                  '(KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 '
                  'Safari/537.36'}

connection = sqlite3.connect(("data.db"))

def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def extracted(source):
    extractor =\
        selectorlib.Extractor.from_yaml_file\
            ("source.yaml")
    value= extractor.extract(source)["tours"]
    return value

def write_text(extract):
    row = extract.split(",")
    row = [item.strip() for item in row]
    cursor=connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)",row)
    connection.commit()

def read_text(extract):
    row =extract.split(",")
    row=[item.strip() for item in row]
    band,city,date=row
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",(band,city,date))
    rows=cursor.fetchall()
    return rows

def sent_email():
    print("Email was sent")

if __name__ == "__main__":
    while True:
        scraped=scrape(URL)
        extract=extracted(scraped)
        print(extract)
        if extract != "No upcoming tours":
            row = read_text(extract)
            if not row:
                write_text(extract)
                sent_email()
        time.sleep(2)
