from django.contrib import admin

from .models import Artist, Ensemble, WorkCatalogue, Work, Key, Instrument, \
    Category, Recording, Catalogue, Movement

class ArtistAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Name', {
            'fields': ('surname', 'forenames')
        }),
        ('Dates', {
            'fields': ('born', 'born_question', 'died', 'died_question')
        }),
        ('Cultural', {
            'fields': ('nationality',),
        }),
        ('Original names', {
            'description':
                "These fields specify the artist's name in their native alphabet",
            'fields': ('original_surname', 'original_forenames',)
        }),
    )
    search_fields = ('surname', 'forenames')
admin.site.register(Artist, ArtistAdmin)

class EnsembleAdmin(admin.ModelAdmin):
    fields = ('name', 'nationality')
    search_fields = ('name',)
admin.site.register(Ensemble, EnsembleAdmin)

class WorkCatalogueInline(admin.TabularInline):
    model = WorkCatalogue
    ordering = ('artist__surname',)

class WorkAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('composer', 'title', 'key', 'nickname', 'category'),
        }),
        ('Dates', {
            'fields': ('year', 'year_question'),
        }),
    )
    raw_id_fields = ('composer',)
    search_fields = ('title',)
    inlines = (WorkCatalogueInline,)
admin.site.register(Work, WorkAdmin)

class CatalogueAdmin(admin.ModelAdmin):
    fields = ('artist', 'prefix', 'num')
admin.site.register(Catalogue, CatalogueAdmin)

class RecordingAdmin(admin.ModelAdmin):
    raw_id_fields = ('work',)
    search_fields = ('work__title',)
admin.site.register(Recording, RecordingAdmin)

class MovementAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title',),
        }),
        (None, {
            'fields': ('recording',),
        }),
        ('Other', {
            'fields': ('section_title', 'num'),
        }),
    )
admin.site.register(Movement, MovementAdmin)

admin.site.register(Category)
admin.site.register(Instrument)
admin.site.register(Key)
