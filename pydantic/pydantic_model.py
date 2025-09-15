from pydantic import BaseModel
from typing import List, Dict, Optional, Annotated
from pydantic import EmailStr, AnyUrl, Field
#we cana dd metadata using combo of Annotated and Field


class Patient(BaseModel):
    name : Annotated[str, Field(max_length = 50, title = 'Enter the Name', description= 'Write your name here', examples= ['Raj', 'Tanmay'])]
    age : int
    weight : float = Field(gt = 0, lt = 120, strict = True) #Field puts a constraint or we can set a range
    #strict = True yeh krega ki '75' pe error dega cause it is a string

    # email : EmailStr #EmailStr is additional datatype provided by pydantic (not in python inherently)
    married : bool = False #by default set to false
    linkedin_url : AnyUrl #AnyUrl provided by pydantic to check valid URLs
    allergies : Optional[List[str]] = Field(default= None, max_items=5) 
    # allergies : Optional[List[str]] = None #Other way to set default None
    contact_details : Dict[str, str]

def insert(patient : Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print("Inserted")

def update(patient : Patient):
    print(patient.name)
    print(patient.age)
    print("Updated")

patient_info = {'name' : 'Tanmay', 'age' : 21, 'weight' : '75', 'married' : True, 'linkedin_url' : 'https://linkedin.com/',
                 'allergies' : ['pollen','dust','c','v','w'], 'contact_details' : {'email' : 'tanmay@gmail.com', 'phone' : '9555974189'}}
patient1 = Patient(**patient_info)
insert(patient1)