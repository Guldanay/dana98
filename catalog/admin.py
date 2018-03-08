from django.contrib import admin

# Register your models here.

from .models import Mugalim,Kafedra, Mamandyk, Kurs

#admin.site.register(Book)
#admin.site.register(Author)
# Define the admin class
class MugalimsInstanceInline(admin.TabularInline):
    model =Mamandyk

class MugalimAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    inlines = [MugalimsInstanceInline]
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
  
# Register the admin class with the associated model
admin.site.register(Mugalim, MugalimAdmin)

admin.site.register(Kafedra)
#admin.site.register(BookInstance)
# Register the Admin classes for Book using the decorator

class KursInline(admin.TabularInline):
    model = Kurs

@admin.register(Mamandyk)
class MamandykAdmin(admin.ModelAdmin):
    list_display = ('title', 'mugalim', 'display_genre')
    inlines = [KursInline]

# Register the Admin classes for BookInstance using the decorator

@admin.register(Kurs)
class KursAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )