from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        """Set up a superuser and a user for the tests."""
        self.client = Client()
        self.superuser = get_user_model().objects.create_superuser(
            email='superuser@example.com', password='password123'
        )
        self.client.force_login(self.superuser)
        self.normal_user = get_user_model().objects.create_user(
            email='user@example.com', password='password123', name='Normal User'
        )

    def test_user_list(self):
        """Test that users are listed on the user page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.normal_user.name)
        self.assertContains(res, self.normal_user.email)

    def test_user_change_page(self):
        """Test that the user edit page works."""
        url = reverse('admin:core_user_change', args=[self.normal_user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        
    
    def test_create_user_page(self):
        """Test that the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

