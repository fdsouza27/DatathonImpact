from django.test import TestCase, Client
from files.models import Project, AuthorDetails, Publication, PublicationDetails

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(
            project_id=2, 
            url="http://example.com"
        )
        self.author = AuthorDetails.objects.create(
            author_id=1,
            authorname="John Doe",
            affiliation="Test University",
            latitude='12.345678',
            longitude='76.543210',
            publication_year=2020,
            attended_date=2019
        )
        self.publication = Publication.objects.create(
            publication_id=1,
            title="Sample Publication",
            publication_year=2021,
            authors="John Doe, Jane Smith",
            project=self.project,
            author=self.author
        )
        PublicationDetails.objects.create(
            publication=self.publication,
            abstract="Sample abstract",
            journal="Sample Journal"
        )

    # Test methods
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_CN_view(self):
        response = self.client.get('/CN')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CN.html')

    def test_SG_view_html(self):
        response = self.client.get('/SG/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'SG.html')

    def test_SG_view_ajax(self):
        response = self.client.get('/SG/', {'author': 'John Doe', 'position': 'First Author'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())  # Check that some JSON is returned

    def test_TE_view_get(self):
        response = self.client.get('/TE/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'TE.html')

    def test_TE_view_post(self):
        response = self.client.post('/TE/', {'selected_author': 'Jane Doe'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())  # Check that some JSON is returned
