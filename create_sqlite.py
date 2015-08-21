__author__ = 'Mensur'

from admin import app
from admin.models import db, Drug


with app.app_context():
    counter = 0
    drugs = db.session.query(Drug).all()

    for drug in drugs:
        if drug.regime is None or drug.shape is None: continue
        counter += 1
        print 'INSERT INTO "Drugs" VALUES ({},"{}", "{}", "{}", "{}", "{}", "{}", {}, "{}", "{}", "{}");'.format(counter,
        drug.protected_name, drug.manufacturer.name, drug.active_substance.name, "NE", drug.shape.farmacological_shape, drug.instructions, 0, drug.regime.description, drug.indication, drug.counterindication)
