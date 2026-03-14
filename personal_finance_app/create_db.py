import runpy

# Run the app file to get the `app` object in its globals
globals_dict = runpy.run_path('finance-app.py')
app = globals_dict.get('app')
if app is None:
    raise RuntimeError('`app` object not found in finance-app.py')

from database.db import db

with app.app_context():
    db.create_all()

print('Tables created')
