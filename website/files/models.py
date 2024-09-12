from django.db import models

class Project(models.Model):
    project_id = models.IntegerField(primary_key=True)  
    url = models.URLField(max_length=200)

class AuthorDetails(models.Model):
    author_id = models.IntegerField(primary_key=True)  
    affiliation = models.CharField(max_length=45)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    publication_year = models.IntegerField()
    authorname = models.CharField(max_length=45)
    attended_date = models.IntegerField(null=True)

class Publication(models.Model):
    publication_id = models.IntegerField(primary_key=True)  
    title = models.CharField(max_length=80)
    publication_year = models.IntegerField()
    authors = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  
    author = models.ForeignKey(AuthorDetails, on_delete=models.CASCADE)  

class PublicationDetails(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE) 
    abstract = models.TextField()
    journal = models.CharField(max_length=150)

