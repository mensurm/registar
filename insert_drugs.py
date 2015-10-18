# -*- coding: utf-8 -*-
__author__ = 'mmensur'


import csv, codecs, cStringIO
from flask import Flask
from admin.models import db, AgencyDrug
from config import SECRET_KEY
import re


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8", errors='ignore') for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        data_list = data.split('|')

        drug = AgencyDrug()
        drug.atc_classification = data_list[0]
        drug.substance_name = data_list[1]
        drug.protected_name = data_list[2]

        if ';' in data_list[3]:
            print data_list[3]
            data_list[3].replace(';', ' ')
        manufacturer_info = data_list[3].split(',')
        drug.manufacturer_name = manufacturer_info[0]

        try:
            drug.manufacturer_address = manufacturer_info[1]
        except IndexError:
            drug.manufacturer_address = None

        try:
            drug.manufacturer_city = manufacturer_info[2]
        except IndexError:
            drug.manufacturer_city = None
        try:
            drug.manufacturer_country = manufacturer_info[3]
        except IndexError:
            drug.manufacturer_country = None

        drug.shape = data_list[5]
        drug.dosage = data_list[6]
        drug.packaging = data_list[7]
        regime = data_list[12].replace('–', '-') #different hyphen like characters
        drug.regime_code = regime.split('-')[0].strip()
        if '"' in drug.regime_code:
            print drug.regime_code
            drug.regime_code.replace('"', '')

        try:
            drug.regime_description = regime.split('-')[1]
        except IndexError:
            drug.regime_description = 'nepoznato'

        db.session.add(drug)
        db.session.commit()

        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        counter = 0
        for row in rows:
            self.writerow(row)
            print "Uneseno {} lijekova".format(counter+1)



app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config.from_object('config')

db.init_app(app)

with app.app_context():

    db.drop_all()
    db.create_all()

    with open('lijekovi.csv','rb') as fin, open('unicode_lijekovi.csv','wb') as fout:
        reader = UnicodeReader(fin)
        writer = UnicodeWriter(fout)
        for line in reader:
            writer.writerow(line)




