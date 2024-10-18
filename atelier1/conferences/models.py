from django.db import models
from categories.models import Category
from django.core.validators import MaxValueValidator,FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Conference(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    start_date=models.DateField(default=timezone.now().date())
    end_date=models.DateField()
    location=models.CharField(max_length=255)
    price=models.FloatField()
    capacity=models.IntegerField(validators=[MaxValueValidator(limit_value=900,message='capacity must be under 900')])
    program=models.FileField(upload_to='files/',validators=[FileExtensionValidator(allowed_extensions=['pdf','png','jpeg','jpg'],message='only pdf,png,jpg,jpeg are allowed')])
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    Category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='conferences')

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError('end date must be after start date')

    class Meta:
        verbose_name_plural="Conferences"
        constraints=[models.CheckConstraint(check=models.Q(start_date__gte=timezone.now().date()),
                                            name="start_date_must_be_today_or_future")]
        
    def __str__(self):
        return f"title conference: {self.title} location :{self.location}"