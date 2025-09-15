from pydantic import BaseModel

class Patient(BaseModel):
    name : str
    age : int

def insert(patient : Patient):
    print(patient.name)
    print(patient.age)
    print('Inserted')

def update(patient : Patient):
    print(patient.name)
    print(patient.age)
    print('Updated')

patient_info = {'name' : 'Tanmay', 'age' : 21}
patient1 = Patient(**patient_info)
update(patient1)