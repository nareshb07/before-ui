import random
from faker import Faker
from .models import User

fake = Faker()

def create_fake_user(n):
        
    for i in range(n):

        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        password = fake.password()
                                         
        user = User.objects.create_user(email = email, password = password,first_name = first_name,last_name = last_name)
        
        user.save()

    
