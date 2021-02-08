"""
Pytest way to do testing
will be a second way with unittest
"""
# Django
from django.urls import reverse
from django.test import Client

# Models
from companies.models import Company

# Test and utilities
import pytest
import json

# DRF
from rest_framework import status

companies_url = reverse("companies-list")

# Pytest has a predfined client fixtures wich is send to the function test
""" Module level fixture, every function after this declaration
will have the @pytest.mark.django_db decorator """
pytestmark = pytest.mark.django_db

# ---- Test GET Companies ------
def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == []

def test_one_copmpany_exists_should_succeed(client) -> None:
    amazon = Company.objects.create(name="Amazon", notes="Hola :)")
    response = client.get(companies_url)
    respose_content = json.loads(response.content)[0]
    assert response.status_code == status.HTTP_200_OK
    assert respose_content.get("name") == "Amazon"
    assert respose_content.get("status") == "Hiring"

# --------- Test POST Companies
def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(path=companies_url)
    respose_content = json.loads(response.content)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert respose_content == {"name": ["This field is required."]}

def test_create_existing_company_should_fail(client) -> None:
    Company.objects.create(name="Apple")
    response = client.post(path=companies_url, data={"name": "Apple"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert json.loads(response.content) == {"name": ["company with this name already exists."]}

def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(path=companies_url, data={"name": "Que ondita"})
    respose_content = json.loads(response.content)
    assert response.status_code == status.HTTP_201_CREATED
    assert respose_content.get("name") == "Que ondita"
    assert respose_content.get("status") == "Hiring"
    assert respose_content.get("notes") == ""

def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    response = client.post(path=companies_url, data={"name": "Que ondita", "status": "Layoffs"})
    respose_content = json.loads(response.content)
    assert response.status_code == status.HTTP_201_CREATED
    assert respose_content.get("status") == "Layoffs"

def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(path=companies_url, data={"name": "Que ondita", "status": "layoffs"})
    respose_content = json.loads(response.content)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "is not a valid choice" in str(respose_content)