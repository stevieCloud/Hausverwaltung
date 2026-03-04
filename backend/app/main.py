from fastapi import FastAPI

app = FastAPI(title='Hausverwaltung MVP')

@app.get('/')
def read_root():
    return {'status': 'ok', 'app': 'Hausverwaltung MVP'}
