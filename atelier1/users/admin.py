from django.contrib import admin
from .models import Participant, Reservation 
admin.site.register(Reservation)

class TagInline(admin.TabularInline):
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
    inlines = [TagInline]
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        print(queryset)
        return queryset.order_by('-is_superuser', 'username')
    
admin.site.register(Participant,ParticipantAdmin)
