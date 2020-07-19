from django.db import models
from django.contrib.auth.models import User
from mapbox_location_field.models import LocationField, AddressAutoHiddenField


# Create your models here.
class Admin_Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    profile_photo = models.ImageField(upload_to = 'profilepics/', blank=True)
    full_name= models.CharField(max_length = 50)    
    bio = models.TextField()
    this_user = models.ForeignKey(User,on_delete=models.CASCADE)    

    def __str__(self):
        return self.full_name 


    
class Neighbourhood(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    hood_name = models.CharField(max_length = 50)   
    location = LocationField(map_attrs={"center": [36.82, -1.29], "marker_color": "blue"})
    address = AddressAutoHiddenField(blank=True)
    occupants_count = models.IntegerField(default=0)
    admin = models.ForeignKey(Admin_Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.hood_name 

    def create_hood(self):
        self.save()

    def delete_hood(self):
        self.delete()

    def update_hood(self):
        self.save()


    @classmethod
    def find_neigborhood(cls, neigborhood_id):
        pass

    @classmethod
    def update_occupants(cls):
        pass

    

        