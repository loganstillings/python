from __future__ import unicode_literals
from ..first_app.models import User
from django.db import models
import datetime
from datetime import date
today = datetime.datetime.today()
# Create your models here.
class AppointmentManager(models.Manager):
    def add_appointment(self, postData, user_id):
        errors = []
        if not postData['date']:
            errors.append('Date is a required field')
        if not postData['time']:
            errors.append('Time is a required field')
        if not postData['tasks']:
            errors.append('Task is a required field')
        # if postData['date'] < today:
        #     errors.append('Date must not be in the past')
        modelsResponse = {}

        if errors:
            modelsResponse['isAppointment'] = False
            modelsResponse['errors'] = errors
        else:
            current_user = User.objects.get(id=user_id)
            modelsResponse['isAppointment'] = True
            appointment = self.create(user=current_user, task=postData['tasks'], time=postData['time'], status="Pending", dated=postData['date'])
            modelsResponse['appointment'] = appointment

        return modelsResponse

    def edit_appointment(self, postData, user_id, appointment_id):
        errors = []
        if not postData['date']:
            errors.append('Date is a required field')
        if not postData['time']:
            errors.append('Time is a required field')
        if not postData['tasks']:
            errors.append('Task is a required field')
        # if postData['date'] < today:
        #     errors.append('Date must not be in the past')
        modelsResponse = {}

        if errors:
            modelsResponse['isUpdate'] = False
            modelsResponse['errors'] = errors
        else:
            modelsResponse['isUpdate'] = True
            current_user = User.objects.get(id=user_id)
            delete = self.get(id=appointment_id).delete()
            appointment = self.create(id=appointment_id, user=current_user, task=postData['tasks'], time=postData['time'], status=postData['status'], dated=postData['date'])
            modelsResponse['appointment'] = appointment

        return modelsResponse

class Appointment(models.Model):
    user = models.ForeignKey(User)
    task = models.CharField(max_length=200)
    time = models.IntegerField()
    status = models.CharField(max_length=50)
    dated = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = AppointmentManager()
