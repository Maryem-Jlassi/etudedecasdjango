from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Conference
from users.models import *
from django.db.models import Count
# Register your models here.
class ReservationInline(admin.StackedInline):
    model=Reservation
    extra=1
    readonly_fields=('reservation',)
    can_delete=True
class ConferenceDateFilter(admin.SimpleListFilter):
    title='date conf filter'
    parameter_name='conference_date'
    def lookups(self,request,model_admin):
        return(
            ('past','past conf'),
            ('today','today conf'),
            ('upcoming','upcoming conf'),
        )
    def queryset(self, request, queryset):
        if self.value()=='past':
            return queryset.filter(start_date__lt=timezone.now().date())
        if self.value()=='today':
            return queryset.filter(start_date=timezone.now().date())
        if self.value()=='upcoming':
            return queryset.filter(start_date__gt=timezone.now().date())
        return queryset
        
class ParticipantFilter(admin.SimpleListFilter):
    title='participant filter'
    parameter_name="participants"

    def lookups(self, request, model_admin):
        return(
            ('0',('No participants')),
            ('more',('more participants')),
        )
    def queryset (self, request, queryset):
        if self.value()=='0':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0)
        elif self.value()=='more':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count__gt=0)

        return queryset
        


class Conferenceadmin(admin.ModelAdmin):
    list_display=('title','location','start_date','end_date','price')
    search_fields=('title',)
    list_per_page=2
    ordering=('start_date','title')
    fieldsets=(
        ('Description',{'fields':('title','description','Category','location')}),
        ('horaires',{'fields':('start_date','end_date','created_at','updated_at')}),
        ('documents',{'fields':('program',)})
    )
    readonly_fields=('created_at','updated_at')
    inlines=[ReservationInline]
    autocomplete_fields=('Category',)
    list_filter=('title',ParticipantFilter,ConferenceDateFilter)
admin.site.register(Conference,Conferenceadmin)
