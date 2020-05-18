from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from .models import Customer

# To Bind signals to the application it is important the this files be imported in the app.py config class inside ready function
def customer_profile(sender,instance,created,**kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(    # Create a User Profile Along with new user
            user=instance,
            name=instance.username
        )        
        print('Profile Created!')
    
post_save.connect(customer_profile,sender=User)