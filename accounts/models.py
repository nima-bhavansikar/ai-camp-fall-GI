from django.db import models
#from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

from django.conf import settings
User = settings.AUTH_USER_MODEL

from django.apps import apps

import uuid

# Create your models here.

class SecurityQuestion(models.Model):
    question = models.CharField(max_length=255)
    #answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question
    
    
    class Meta:
        db_table = 'securityquestion'
    

class CustomUser(AbstractUser):
    security_question = models.CharField(max_length=50, default='')
    security_answer = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.username
 
    class Meta:
        db_table = 'accounts_customuser'
 

#AUTH_USER_MODEL =  'accounts.CustomUser'



# when changing this, you may have to change stuff in admin.py too
class UserData(models.Model):
    from community.models import SharedLink

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #nickname = models.CharField(max_length=50)

    #active = models.BooleanField(default=True)

    darkmode = models.BooleanField(default=False)

    #progress = models.FloatField(default=0)
    #score = models.IntegerField(default=0)
    saved_code = models.TextField(default="""{}""")
    saved_code_course_one = models.TextField(default="""{}""")
    saved_code_course_two = models.TextField(default="""{}""")
    saved_code_course_three = models.TextField(default="""{}""")
    saved_code_course_four = models.TextField(default="""{}""")
    
    saved_code_shared_link = models.ForeignKey(SharedLink, on_delete=models.CASCADE, related_name="zero", null=True)
    saved_code_course_one_shared_link = models.ForeignKey(SharedLink, on_delete=models.CASCADE, related_name="one", null=True)
    saved_code_course_two_shared_link = models.ForeignKey(SharedLink, on_delete=models.CASCADE, related_name="two", null=True)
    saved_code_course_three_shared_link = models.ForeignKey(SharedLink, on_delete=models.CASCADE, related_name="three", null=True)
    saved_code_course_four_shared_link = models.ForeignKey(SharedLink, on_delete=models.CASCADE, related_name="four", null=True)
    
    # saved_code_shared_link = models.ForeignKey("community.SharedLink", on_delete=models.CASCADE, related_name="zero")
    # saved_code_course_one_shared_link = models.ForeignKey("community.SharedLink", on_delete=models.CASCADE, related_name="one")
    # saved_code_course_two_shared_link = models.ForeignKey("community.SharedLink", on_delete=models.CASCADE, related_name="two")
    # saved_code_course_three_shared_link = models.ForeignKey("community.SharedLink", on_delete=models.CASCADE, related_name="three")
    # saved_code_course_four_shared_link = models.ForeignKey("community.SharedLink", on_delete=models.CASCADE, related_name="four")
    

    #saved_code_course_one

    class Meta:
        db_table = 'accounts_userdata'

"""
def create_shared_link():
    #SharedLink = apps.get_model("community", "SharedLink")
    return SharedLink.objects.create()
    #return SharedLink.objects.create(id=str(uuid.uuid4()), code="{}")
"""
@receiver(post_save, sender=User)
def create_user_data(sender, instance, created, **kwags):
    from community.models import SharedLink

    if created:
        saved_code_shared_link = SharedLink.objects.create(author=instance, course_number=0)
        saved_code_course_one_shared_link = SharedLink.objects.create(author=instance, course_number=1)
        saved_code_course_two_shared_link = SharedLink.objects.create(author=instance, course_number=2)
        saved_code_course_three_shared_link = SharedLink.objects.create(author=instance, course_number=3)
        saved_code_course_four_shared_link = SharedLink.objects.create(author=instance, course_number=4)

        UserData.objects.create(
            user=instance,
            #nickname=instance.username,
            #progress=0,
            #score=0,
            # saved_code="{}",
            # saved_code_course_one="{}",
            # saved_code_course_two="{}",
            # saved_code_course_three="{}",
            # saved_code_course_four="{}",
            saved_code_shared_link = saved_code_shared_link,
            saved_code_course_one_shared_link = saved_code_course_one_shared_link,
            saved_code_course_two_shared_link = saved_code_course_two_shared_link,
            saved_code_course_three_shared_link = saved_code_course_three_shared_link,
            saved_code_course_four_shared_link = saved_code_course_four_shared_link,
        )
"""
saved_code_shared_link = create_shared_link(),
saved_code_course_one_shared_link = create_shared_link(),
saved_code_course_two_shared_link = create_shared_link(),
saved_code_course_three_shared_link = create_shared_link(),
saved_code_course_four_shared_link = create_shared_link(),
"""
