from django.contrib import admin
from .models import Event, Event_Attendee, Event_Socials, Event_Users,Event_Host
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
  list = ('title', 'description', 'completed')

admin.site.register(Todo, TodoAdmin)
admin.site.register(Event_Users)
admin.site.register(Event_Host)
admin.site.register(Event)
admin.site.register(Event_Attendee)
admin.site.register(Event_Socials)
