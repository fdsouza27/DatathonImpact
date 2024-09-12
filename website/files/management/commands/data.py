import pandas as pd
from django.core.management.base import BaseCommand
from files.models import Project, AuthorDetails, Publication, PublicationDetails

class Command(BaseCommand):
    help = 'Import data from CSV files into the Django models'

    def handle(self, *args, **kwargs):
        # Importing Project data
        project_df = pd.read_csv('files/static/project.csv')
        for index, row in project_df.iterrows():
            Project.objects.create(
                project_id=row['Project_Id'],
                url=row['Url']
            )

        # Importing AuthorDetails data
        author_details_df = pd.read_csv('files/static/Author_details.csv')
        author_details_df['Year'].fillna(2021, inplace=True)  
        for index, row in author_details_df.iterrows():
            AuthorDetails.objects.create(
                author_id=row['Author_Id'],
                affiliation=row['Affiliation'],
                latitude=row['Latitude'],
                longitude=row['Longitude'],
                publication_year=int(row['Year']),  # Convert to integer
                authorname=row['Author Name'],
                attended_date=row['Attended_date'] 
            )

        # Importing Publications data
        publications_df = pd.read_csv('files/static/Publications.csv')
        publications_df['Year'].fillna(2021, inplace=True) 
        for index, row in publications_df.iterrows():
            project = Project.objects.get(project_id=row['Project_Id'])
            author = AuthorDetails.objects.get(author_id=row['Author_Id'])
            Publication.objects.create(
                publication_id=row['Id'],
                title=row['Title'],
                publication_year=int(row['Year']),  # Convert to integer
                authors=row['Authors'],
                project=project,
                author=author
            )

        # Importing PublicationDetails data
        publication_details_df = pd.read_csv('files/static/Publication_details.csv')
        for index, row in publication_details_df.iterrows():
            publication = Publication.objects.get(publication_id=row['Id'])
            PublicationDetails.objects.create(
                publication=publication,
                abstract=row['Abstract'],
                journal=row['Journal']
            )

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV files'))
