from django.db import models
from django.contrib.auth.models import AbstractUser
from conferences.models import Conference
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def email_validator (value):
     if not value.endswith('@esprit.tn'):
          raise ValidationError('Email Invalid ,only @esprit.tn domain are allowed') 

class Participant(AbstractUser):
    cin_validator=RegexValidator(regex=r'^\d{8}$',message='this field must contains exactly 8 digits')
    cin=models.CharField(primary_key=True,max_length=8,validators=[cin_validator])
    email=models.EmailField(unique=True,max_length=255,validators=[email_validator])
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    username=models.CharField(unique=True,max_length=255)
    USERNAME_FIELD='username'
    CHOICES=[
        ('etudiant','etudiant'),
        ('chercheur','chercheur'),
        ('docteur','docteur'),
        ('enseignant','enseignant')

    ]
    Participant_category=models.CharField(max_length=255,choices=CHOICES)
    reservations=models.ManyToManyField(Conference,through='Reservation',related_name='reservations')
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    update_at=models.DateTimeField(auto_now=True,null=True)

    class Meta:
         verbose_name_plural = "Participants"


class Reservation(models.Model):
        reservation=models.DateTimeField(auto_now_add=True)
        conference=models.ForeignKey(Conference,on_delete=models.CASCADE)
        Participant=models.ForeignKey(Participant,on_delete=models.CASCADE)
        confirmed=models.BooleanField(default=False)
        def clean(self):
             if self.conference.start_date < timezone.now().date():
              raise ValidationError('you can only reserve for upcoming conference')
              reservation_count=Reservation.objects.filter(Participant=self.Participant,reservation=timezone.now().date())
              if len(reservation_count) >= 2:
                   raise ValidationError("you can only make up to 3 reservations per day")
              
        class Meta:
            unique_together=('conference','Participant')
            verbose_name_plural="Reservations"
        def __str__(self):
             return f"reservation : {self.reservation}"