from django.db import models
from django.contrib.auth.models import User

#CUSTOM USER PROFILE, IF YOU CHECK IN THE DJANGO ADMIN PANEL ON THE WEBSITE
#THE FIELDS ARE THERE. IT JUST DOESN'T SAVE CORRECTLY FOR SOME REASON
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_question = models.CharField(max_length=10000)
    security_answer = models.CharField(max_length=10000)

    def __str__(self):
        return self.user.username
