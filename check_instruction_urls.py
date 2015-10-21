__author__ = 'Mensur'

from urllib import urlopen

from admin import app
from admin.models import db, AgencyDrug

with app.app_context():
    broken_links = []
    drugs = db.session.query(AgencyDrug).filter(AgencyDrug.instructions_link != None).all()
    for drug in drugs:
        try:
            if urlopen(drug.instructions_link).getcode() == 200:
                print "{} : OK".format(drug.protected_name)
            else:
                broken_links.append(drug)
        except Exception as e:
            broken_links.append(drug)

    print '#############################################################'
    for drug in broken_links:
        print '{} link: {}, LINK BROKEN'.format(drug.protected_name, drug.instructions_link)
