from django.template.loader import render_to_string
import re
from bs4 import BeautifulSoup
from django.conf import settings
from django.test import TestCase
import os
import unittest
from django.urls import reverse
from django.test import Client
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from map.models import Event
from django.contrib.auth.models import User
from django.utils import timezone


"""
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
MAPS_KEY = os.environ.get("MAPS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

class NavigationBarTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()  # Initialize the Selenium WebDriver (Chrome in this case)
        cls.selenium.implicitly_wait(10)  # Set a default wait time for elements to appear

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()  # Close the Selenium WebDriver
        super().tearDownClass()

    def test_navigation_links(self):
        
        self.selenium.get(f'{self.live_server_url}/')  # Open the homepage

        google_login_link = self.selenium.find_element(By.LINK_TEXT, "Login with Google")
        google_login_link.click()
        time.sleep(30)
     
        email_field = self.selenium.find_element("identifierId")
        email_field.send_keys("mthomas.number8@gmail.com")  # Replace with your email

        # Click the "Next" button to proceed to the password page
        next_button = self.selenium.find_element("identifierNext")
        next_button.click()

        # Wait for a short period for the next page to load
        time.sleep(2)

        # Fill in the password field
        password_field = self.selenium.find_element("password")
        password_field.send_keys("Iamironman3")  # Replace with your password

        # Click the "Next" button to submit the login credentials
        password_next_button = self.selenium.find_element("passwordNext")
        password_next_button.click()

        # Wait for a few seconds to allow the login process to complete
        time.sleep(5)

        # Find and click on the 'createEvent' link in the navigation bar
        # create_link = self.selenium.find_element_by_link_text(' | Create Event')
        create_event_link = self.selenium.find_element(By.PARTIAL_LINK_TEXT, 'Create Event')
        create_event_link.click()

        # Check if the browser navigated to the correct URL (change this URL to your 'createEvent' page)
        self.assertEqual(self.selenium.current_url, f'{self.live_server_url}/createEvent/')
"""

class MapViewTestCase(TestCase):
    def test_map_page(self):
        response = self.client.get(reverse('map'))  # Replace 'map-page' with the actual URL pattern name for your map page
        self.assertEqual(response.status_code, 200)  # Check that the page loads successfully
        
    def test_map_page(self):
        response = self.client.get(reverse('map'))  # Replace 'map-page' with the actual URL pattern name for your map page
        self.assertContains(response, "initMap")  # Check that the initMap function is present in the HTML response

    def test_map_page(self):
        response = self.client.get(reverse('map'))  # Replace 'map-page' with the actual URL pattern name for your map page
        self.assertContains(response, "maps.googleapis.com/maps/api/js?key=")  # Check that the Google Maps API script is includ

class CreateViewTestCase(TestCase):
    def test_map_page(self):
        response = self.client.get(reverse('map'))  # Replace 'map-page' with the actual URL pattern name for your map page
        self.assertEqual(response.status_code, 200)  # Check that the page loads successfully
        
    def test_map_page(self):
        response = self.client.get(reverse('map')) 
        self.assertContains(response, "initMap")

    def test_map_page(self):
        response = self.client.get(reverse('map'))  # Replace 'map-page' with the actual URL pattern name for your map page
        self.assertContains(response, "maps.googleapis.com/maps/api/js?key=")  # Check that the Google Maps API script is includ


class EventModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample User instance for testing
        test_user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a sample Event instance for testing
        cls.event = Event.objects.create(
            user=test_user,
            event_name='Sample Event',
            event_description='Description of the sample event',
            location_name='Sample Location',
            event_address='123 Sample St',
            event_date_and_time=timezone.now(),
            point_of_contact='Sample Contact',
            latitude='40.7128',
            longitude='-74.0060',
            category='academic',
            requirements='Sample requirements',
            approved=False,
            deny_reason=None
        )

    def test_event_str_representation(self):
        event = EventModelTest.event
        self.assertEqual(str(event), 'Sample Event')

    def test_event_fields(self):
        event = EventModelTest.event
        self.assertEqual(event.user.username, 'testuser')
        self.assertEqual(event.event_name, 'Sample Event')
        self.assertEqual(event.event_description, 'Description of the sample event')
        # ... test other fields similarly

    def test_event_category_choices(self):
        event = EventModelTest.event
        # Check if the category of the event belongs to the given choices
        self.assertTrue(any(event.category == choice[0] for choice in Event.CATEGORY_CHOICES))

    def test_event_default_values(self):
        event = EventModelTest.event
        self.assertEqual(event.approved, False)
        self.assertEqual(event.deny_reason, None)




class DeleteEventsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample User instance for testing
        cls.test_user = User.objects.create_user(username='testuser', password='testpassword')

        # Create sample Event instances for testing
        cls.event1 = Event.objects.create(
            user=cls.test_user,
            event_name='Event 1',
            event_description='Description for Event 1',
            location_name='Location 1',
            event_address='123 Event St',
            event_date_and_time='2023-12-01 12:00:00',
            point_of_contact='Contact 1',
            latitude='40.7128',
            longitude='-74.0060',
            category='academic',
            requirements='Requirements for Event 1',
            approved=True,
            deny_reason=None
        )

        cls.event2 = Event.objects.create(
            user=cls.test_user,
            event_name='Event 2',
            event_description='Description for Event 2',
            location_name='Location 2',
            event_address='456 Event St',
            event_date_and_time='2023-12-02 13:00:00',
            point_of_contact='Contact 2',
            latitude='41.8781',
            longitude='-87.6298',
            category='social',
            requirements='Requirements for Event 2',
            approved=False,
            deny_reason='Not approved for Event 2'
        )
    def setUp(self):
        self.client = Client()


    def test_delete_events_template(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('delete-event'), follow=True)
        
    def test_delete_event_view(self):
        # Assuming 'delete-event' is the view name for deleting events
        response = self.client.post(reverse('delete-event'), {'event_id': self.event1.id})

        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Event.objects.filter(id=self.event1.id).exists())

class MapTemplateTest(TestCase):
    def test_map_template_contains_navigation_links(self):
        # Replace 'your_url_name' with the name of the URL associated with this template
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('home'))
        # print("Response: ", response)

        self.assertContains(response, 'map')  # Check if 'View Events' link is present
        
    def test_map_template_contains_images(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('home'))

        #self.assertContains(response, '<img src="{% static \'rotunda.png\' %}"')  # Check for the presence of the 'rotunda.png' image
