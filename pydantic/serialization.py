# Pydantic models can be exported in two formats : one is dictionary and other one is json

from pydantic import BaseModel

class Address(BaseModel):
    pin : str
    city : str
    country : str

class Traveller(BaseModel):
    name : str = 'Tanmay'
    age : int
    weight : float
    married : bool
    address : Address

address_dict = {'pin':'540001', 'city':'Bengaluru', 'country':'India'}
address1 = Address(**address_dict)

traveller_dict = {'age':'21', 'weight':'72', 'married':True, 'address':address1} #if name is not set by default we have given tanmay
traveller1 = Traveller(**traveller_dict)

# temp = traveller1.model_dump(exclude=['name'])
temp = traveller1.model_dump(exclude={'address' : ['city']})
# temp = traveller1.model_dump(include=['name'])
temp = traveller1.model_dump(exclude_unset=True) #jo cheeze object banate samay set nahi ki gyi hai vo cheeze export nhi hongi for eg here name
print(temp)

# traveller1.model_dump_json export krega in form of json data
# traveller1.model_dump export krega in form of dictionary