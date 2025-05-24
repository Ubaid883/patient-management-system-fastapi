from fastapi import FastAPI
import json
app = FastAPI()

# Read data from json file
def load_data():
    with open('json_data.json', 'r') as f:
        data = json.load(f)
    return data

# define Route/ URL
@app.get('/')
def Home():
    return {'Message: Patient Management System Record'}

# To View Patients data
@app.get('/view')
def View():
    data = load_data()
    return data
