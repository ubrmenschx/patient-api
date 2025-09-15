#fields which are computed themselves (not given by the user) for eg BMI calculation based on the height and weight


from pydantic import BaseModel
from typing import List, Dict, Optional, Annotated
from pydantic import EmailStr, AnyUrl, Field, computed_field

class Patient(BaseModel):
    name : str
    age : int
    weight : float
    height : float
    married : bool
    email : EmailStr
    linkedin_url : AnyUrl 
    allergies : Optional[List[str]] 
    contact_details : Dict[str, str]

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight/self.height**2, 2)
        return bmi


def insert(patient : Patient):
    print(patient.name)
    print(patient.calculate_bmi)
    print(patient.allergies)
    print("Inserted")

def update(patient : Patient):
    print(patient.name) 
    print("Updated")

patient_info = {'name' : 'Tanmay', 'age' : '30', 'weight' : '72', 'height':'1.65', 'married' : True, 'linkedin_url' : 'https://linkedin.com/', 'email' : 'tanmay@iitm.edu',
                 'allergies' : ['pollen','dust','c','v','w'], 'contact_details' : {'email' : 'tanmay@iitd.edu', 'phone' : '9555974189'}}
patient1 = Patient(**patient_info)
insert(patient1)