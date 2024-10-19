from django.contrib import admin
from .models import Participant, Reservation 

class ReservationInline(admin.TabularInline):
    model=Reservation
    extra=1
    can_delete=True
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('cin', 'email', 'first_name', 'last_name', 'username','created_at','update_at')
    list_filter = ('cin','username','last_name',)
    search_fields = ('cin', 'first_name','last_name','username')
    autocomplete_fields = ('reservations',)
    list_per_page = 2
    readonly_fields = ('created_at', 'update_at')
    exclude = ('created_at', 'update_at',) 
    fieldsets = (
        ('Login Information', {
            'fields': ('username', 'email'),
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'cin'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'update_at'),
        }),
    )
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        print(queryset)
        return queryset.order_by('-is_superuser', 'username')

    #ajouter une reservation au niveau du modele participant
    inlines = [ReservationInline]

class ReservationAdmin(admin.ModelAdmin):
        list_display=('reservation','conference','Participant','confirmed')
        actions=['confirmed','unconfirmed']
        def confirmed(self,request,queryset):
            queryset.update(confirmed=True)
            self.message_user("Les réservations sont confirmées ")
        confirmed.short_description="Reservation à confirmer"
        def unconfirmed(self,request,queryset):
             queryset.update(confirmed=False)
             self.message_user(request,"les réservations sont non confirmés")
        unconfirmed.short_description="Reservation à non confirmer"

admin.site.register(Participant,ParticipantAdmin)
admin.site.register(Reservation,ReservationAdmin)

