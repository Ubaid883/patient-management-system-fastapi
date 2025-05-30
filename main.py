from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, computed_field, Field
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
import json

app = FastAPI()

class PatientValidation(BaseModel):
    id: Annotated[str, Field(...,description='ID of Patient', example='P001')]
    name: Annotated[str, Field(...,description='Name of Patient')]
    age: Annotated[int, Field(...,description='Age of Patient',gt=0, le=120)]
    gender: Annotated[Literal['male','female','other'], Field(...,description='Gender of Patient')]
    city: Annotated[str, Field(...,description='City of Patient wher Live')]
    height: Annotated[int, Field(...,description='Height of Patient in cm')]
    weight: Annotated[int, Field(...,description='Weight of Patient in Kg')]
    blood_group: Annotated[Literal['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'], Field(...,description='Blood Group of Patient ')]
     
    # Calculate BMI
    @computed_field
    @property
    def BMI(self) -> float:
        bmi  = round(self.weight / (self.height**2),2)
        return bmi
    # Status of Patient
    @computed_field
    @property
    def status(self) -> str:
        bmi = self.BMI
        if bmi < 18:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        elif bmi < 30:
            return 'Overweight'
        else:
            return 'Obesity'
     
# Read data from json file
def load_data():
    with open('json_data.json', 'r') as f:
        data = json.load(f)
    return data

# save data
def save_data(data):
    with open('json_data.json', 'w') as f:
        json.dump(data,f)
        
# define Route/ URL
@app.get('/')
def Home():
    return {'Message: Patient Management System Record'}

# To View Patients data
@app.get('/view')
def View():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def View_Patient(patient_id:str = Path(description='Search Patient data by ID', example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return {'error:Patient data not found!'}

@app.post('/create')
def create(patient:PatientValidation):
    
    # Load Data
    data = load_data()
    
    # check patient if already exit
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exit')
    
    # new patient add into data
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    # save data into json
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message':'Patient create successfully'})