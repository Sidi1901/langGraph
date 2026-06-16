from pydantic import BaseModel 

class PydanticPatient(BaseModel):
    name : str 
    age : int 


def insert_patient_data(patient : PydanticPatient):
    # Some operations
    print(patient.name, patient.age)


patient_info = {"name":"sidi","age":40} # Try giving "forty"

patient1 = PydanticPatient(**patient_info)

insert_patient_data(patient1)

