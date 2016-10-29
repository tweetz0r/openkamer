from django.contrib import admin

from parliament.models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fullname',
        'forename',
        'surname',
        'surname_prefix',
        'initials',
        'slug',
        'birthdate',
        'wikidata_id',
        'parlement_and_politiek_id',
    )


admin.site.register(Person, PersonAdmin)