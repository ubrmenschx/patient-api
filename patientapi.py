from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
import json

class Patient(BaseModel):
    id : Annotated[str, Field(..., description='Write your id')]
    name : Annotated[str, Field(..., description='Write your full name')]
    city : Annotated[str, Field(..., description='Which city do you reside in?')]
    age : Annotated[int, Field(..., gt=0, lt=120, description='How old are you?')]
    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description='Pick one of them')]
    height : Annotated[float, Field(..., description='Put height in mtrs')]
    weight : Annotated[float, Field(..., description='Put weight in kgs')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round((self.weight)/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return 'Under Weight'
        elif (18.5 < bmi < 24.9):
            return 'Normal Weight'
        elif (25 < bmi < 29.9):
            return 'Over Weight'
        elif (30 < bmi < 34.9):
            return 'Obese'
        else :
            return 'Extremely Obese'
        

class updatePatient(BaseModel):
    name : Annotated[Optional[str], Field(default=None, description='Write Patient Name')]
    city : Annotated[Optional[str], Field(default=None, description='Which city do you reside in?')]
    age : Annotated[Optional[int], Field(default=None, gt=0, lt=120, description='How old are you?')]
    gender : Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None, description='Pick one of them')]
    height : Annotated[Optional[float], Field(default=None, description='Put height in mtrs')]
    weight : Annotated[Optional[float], Field(default=None, description='Put weight in kgs')]

        
app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data, f) #dump kr rhe hai data ko into the file

@app.get('/') #endpoint1
def hello():
    return {'message' : 'Patient Management System API'}

@app.get('/about') #endpoint2
def about():
    return {'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(..., description = 'ID of the Patient', examples = 'P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    # return {'error' : 'patient not found'}
    raise HTTPException(status_code = 404, detail = 'Patient Not Found')

@app.get('/sort') # http://127.0.0.1:8000/sort?sort_by=bmi&order=desc - way to access data
def sort_patients(sort_by : str = Query(..., description = 'sort on the basis of height, weight or BMI'), order : str = Query('asc', description = 'sort by asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key= lambda x: x.get(sort_by, 0), reverse= sort_order)
    return sorted_data


@app.post('/create')
def create_patient(patient : Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='The patient is already in the database') 
    
    data[patient.id] = patient.model_dump(exclude=['id']) #adding the data to our database

    save_data(data)

    return JSONResponse(status_code=201, content={'message' : 'Patient Added Successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id : str, patient_update : updatePatient):

    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient is not in the database')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value

    
    #existing_patient_info ko banana hai -> pydantic object -> jo calculate krega updated bmi +verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    #then convert pydantic obj -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude={'id'})

    #add this dict to data
    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Patient updated successfully'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id : str):
    data = load_data()

    if patient_id not in data:
        return HTTPException(status_code=200, detail='Patient Not Found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Patient Deleted'})