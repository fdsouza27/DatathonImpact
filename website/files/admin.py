from django.contrib import admin

# Register your models here.

from files.models import Project, AuthorDetails, Publication, PublicationDetails

admin.site.register(Project)
admin.site.register(AuthorDetails)
admin.site.register(Publication)
admin.site.register(PublicationDetails)
