# Model validators have 2 major functions -> if we have to apply some feature or checker thst involves multiple fields then
# we'll have to use model_validator for eg if we have to add a feature that every person whose age is >60 must have an emergency
# contact in their contact details then that will be possible only by model validators


from pydantic import BaseModel
from typing import List, Dict, Optional, Annotated
from pydantic import EmailStr, AnyUrl, Field, model_validator

class Patient(BaseModel):
    name : str
    age : int
    weight : float
    married : bool
    email : EmailStr
    linkedin_url : AnyUrl 
    allergies : Optional[List[str]] 
    contact_details : Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('All Members with age greater than 60 must have an emergency contact')
        return model 


def insert(patient : Patient):
    print(patient.name)
    print(patient.allergies)
    print("Inserted")

def update(patient : Patient):
    print(patient.name) 
    print("Updated")

patient_info = {'name' : 'Tanmay', 'age' : '61', 'weight' : '75', 'married' : True, 'linkedin_url' : 'https://linkedin.com/', 'email' : 'tanmay@iitm.edu',
                 'allergies' : ['pollen','dust','c','v','w'], 'contact_details' : {'email' : 'tanmay@iitd.edu', 'phone' : '9555974189'}}
patient1 = Patient(**patient_info)
insert(patient1)