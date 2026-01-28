from faker import Faker
import random

def generate_patients(n: int = 246945) -> dict:
    data = []
    fake = Faker()
    
    for patient_id in range(1, n + 1):
        gender = random.choice(["M", "F"])
        if gender == "M":
            first_name = fake.first_name_male()
        else:
            first_name = fake.first_name_female()
        data.append({
            "patient_id" : patient_id,
            "gender" : gender,
            "first_name" : first_name,
            "last_name" : fake.last_name(),
            "age" : random.randint(15, 80)
        })
    
    return data