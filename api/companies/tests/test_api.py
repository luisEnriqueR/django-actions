# Django
from django.urls import reverse
from django.test import Client

# Models
from companies.models import Company

# Test and utilities
from unittest import TestCase
import pytest
import json

# DRF
from rest_framework import status

@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):
    def setUp(self) -> None:
        # function that runs before every test
        self.client = Client()
        self.companies_url = reverse("companies-list")
    
    def tearDown(self) -> None:
        pass

class TestGetCompanies(BasicCompanyAPITestCase):
    # Name implies test state
    # Sufix implies assertion
    def test_zero_companies_should_return_empty_list(self) -> None:
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [])

    def test_one_copmpany_exists_should_succeed(self) -> None:
        amazon = Company.objects.create(name="Amazon", notes="Hola :)")
        response = self.client.get(self.companies_url)
        respose_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(respose_content.get("name"), "Amazon")
        self.assertEqual(respose_content.get("status"), "Hiring")

class TestPostCompanies(BasicCompanyAPITestCase):
    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        respose_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(respose_content, {"name": ["This field is required."]})

    def test_create_existing_company_should_fail(self) -> None:
        Company.objects.create(name="Apple")
        response = self.client.post(path=self.companies_url, data={"name": "Apple"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"name": ["company with this name already exists."]})

    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "Que ondita"})
        respose_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(respose_content.get("name"), "Que ondita")
        self.assertEqual(respose_content.get("status"), "Hiring")
        self.assertEqual(respose_content.get("notes"), "")

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "Que ondita", "status": "Layoffs"})
        respose_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(respose_content.get("status"), "Layoffs")

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "Que ondita", "status": "layoffs"})
        respose_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("is not a valid choice", str(respose_content))

    @pytest.mark.xfail
    def test_its_ok_if_fails(self) -> None:
        # It's ok if it fails because something that its going to be fixed later
        pass

    @pytest.mark.skip
    def test_should_be_skiped(self) -> None:
        pass