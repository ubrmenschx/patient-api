from pydantic import BaseModel

class Address(BaseModel):
    pin : str
    city : str
    country : str

class Traveller(BaseModel):
    name : str
    age : int
    weight : float
    married : bool
    address : Address

address_dict = {'pin':'540001', 'city':'Bengaluru', 'country':'India'}
address1 = Address(**address_dict)

traveller_dict = {'name':'Tanmay', 'age':'21', 'weight':'72', 'married':True, 'address':address1}
traveller1 = Traveller(**traveller_dict)

print(traveller1.address.city)
print(traveller1)