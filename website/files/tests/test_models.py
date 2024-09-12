from django.test import TestCase
from files.models import Project, AuthorDetails, Publication, PublicationDetails
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError

class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Using a placeholder 'a' for the URL
        Project.objects.create(project_id=1, url="a")

    def test_url_max_length(self):
        project = Project.objects.get(project_id=1)
        max_length = project._meta.get_field('url').max_length
        self.assertEqual(max_length, 200)


class AuthorDetailsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AuthorDetails.objects.create(
            author_id=1,
            affiliation="Test University",
            latitude=Decimal('12.345678'),
            longitude=Decimal('76.543210'),
            publication_year=2020,
            authorname="John Doe",
            attended_date=2019
        )

    def test_affiliation_max_length(self):
        author = AuthorDetails.objects.get(author_id=1)
        max_length = author._meta.get_field('affiliation').max_length
        self.assertEqual(max_length, 45)

    def test_latitude_field_type(self):
        author = AuthorDetails.objects.get(author_id=1)
        self.assertIsInstance(author.latitude, Decimal)

    def test_longitude_field_type(self):
        author = AuthorDetails.objects.get(author_id=1)
        self.assertIsInstance(author.longitude, Decimal)

    def test_latitude_range(self):
        author = AuthorDetails.objects.get(author_id=1)
        self.assertGreaterEqual(author.latitude, Decimal('-90.000000'))
        self.assertLessEqual(author.latitude, Decimal('90.000000'))

    def test_longitude_range(self):
        author = AuthorDetails.objects.get(author_id=1)
        self.assertGreaterEqual(author.longitude, Decimal('-180.000000'))
        self.assertLessEqual(author.longitude, Decimal('180.000000'))

    def test_publication_year_type(self):
        author = AuthorDetails.objects.get(author_id=1)
        self.assertIsInstance(author.publication_year, int)

    def test_authorname_max_length(self):
        author = AuthorDetails.objects.get(author_id=1)
        max_length = author._meta.get_field('authorname').max_length
        self.assertEqual(max_length, 45)

    def test_attended_date_type(self):
        author = AuthorDetails.objects.get(author_id=1)
        self.assertIsInstance(author.attended_date, int)


class PublicationModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(project_id=1, url="a")
        self.author_details = AuthorDetails.objects.create(
            author_id=1, 
            affiliation="Test University", 
            latitude='12.345678', 
            longitude='76.543210', 
            publication_year=2020, 
            authorname="John Doe",
            attended_date=2021
        )
        self.publication = Publication.objects.create(
            publication_id=1,
            title="The Effects of Test Driven Development",
            publication_year=2021,
            authors="John Doe, Jane Smith",
            project=self.project,
            author=self.author_details
        )

    def test_title_max_length(self):
        max_length = self.publication._meta.get_field('title').max_length
        self.assertEqual(max_length, 80)

    def test_publication_year(self):
        self.assertEqual(self.publication.publication_year, 2021)

    def test_authors_max_length(self):
        max_length = self.publication._meta.get_field('authors').max_length
        self.assertEqual(max_length, 50)

    def test_project_foreign_key(self):
        self.assertIsInstance(self.publication.project, Project)

    def test_author_foreign_key(self):
        self.assertIsInstance(self.publication.author, AuthorDetails)


class PublicationDetailsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(project_id=1, url="a")

        cls.author_details = AuthorDetails.objects.create(
            author_id=1,
            affiliation="Test University",
            latitude=Decimal('12.345678'),
            longitude=Decimal('76.543210'),
            publication_year=2020,
            authorname="Jane Doe",
            attended_date=2021
        )

        cls.publication = Publication.objects.create(
            publication_id=1,
            title="The Effects of Test Driven Development",
            publication_year=2021,
            authors="John Doe, Jane Smith",
            project=cls.project,
            author=cls.author_details
        )

        cls.publication_detail = PublicationDetails.objects.create(
            publication=cls.publication,
            abstract="Detailed abstract of the publication",
            journal="Journal of Test Research"
        )

    def test_journal_max_length(self):
        max_length = self.publication_detail._meta.get_field('journal').max_length
        self.assertEqual(max_length, 150)

    def test_abstract_content(self):
        self.assertIsNotNone(self.publication_detail.abstract)

    def test_publication_foreign_key(self):
        self.assertIsInstance(self.publication_detail.publication, Publication)



