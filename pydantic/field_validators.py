# Field validators have 2 major functions -> to validate data according to our personal needs and secondly to apply some
# transformation to any field


from pydantic import BaseModel
from typing import List, Dict, Optional, Annotated
from pydantic import EmailStr, AnyUrl, Field, field_validator

class Patient(BaseModel):
    name : str
    age : int
    weight : float
    married : bool
    email : EmailStr
    linkedin_url : AnyUrl 
    allergies : Optional[List[str]] 
    contact_details : Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['iitb.edu','iitm.edu','iitd.edu']
        
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a Valid One!')

        return value
    
    @field_validator('name') #jis field pe lagana hai validation
    @classmethod
    def name_transform(cls, value):
        return value.upper()
    
    #field validators can be run in two modes : one is before type coercion and other is after type coercion
    @field_validator('age', mode='before') #gives error in mode 'before' cause comparison can't be done between int and str
    @classmethod
    def age_checker(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age is not allowed')


def insert(patient : Patient):
    print(patient.name)
    print(patient.allergies)
    print("Inserted")

def update(patient : Patient):
    print(patient.name) 
    print("Updated")

patient_info = {'name' : 'Tanmay', 'age' : '30', 'weight' : '75', 'married' : True, 'linkedin_url' : 'https://linkedin.com/', 'email' : 'tanmay@iitm.edu',
                 'allergies' : ['pollen','dust','c','v','w'], 'contact_details' : {'email' : 'tanmay@iitd.edu', 'phone' : '9555974189'}}
patient1 = Patient(**patient_info)
insert(patient1)