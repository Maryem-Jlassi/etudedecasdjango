from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re


def validate_letters_only(value):
        if not re.match(r'^[A-Za-z\s]+$',value):
             raise ValidationError('this field should only contain letters')


class Category(models.Model):
    letters_only=RegexValidator((r'^[A-Za-z\s]+$'),'only letters are allowed')
    title=models.CharField(unique=True,max_length=255,validators=[validate_letters_only])
    created_app=models.DateField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural="Categories"
 
    def __str__(self):
         return f"title category {self.title}"