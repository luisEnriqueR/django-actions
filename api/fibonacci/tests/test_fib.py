# Django
from django.urls import reverse
from django.test import Client

# Test and utilities
import pytest
import json

# DRF
from rest_framework import status

@pytest.mark.parametrize("n, expected", [(0,0), (1,1), (2,1), (20, 6765)])
def test_fibonaccio_correct_values_should_succed(client, n, expected) -> None:
    response = client.get("/fibonacci", {"n": n})
    response_content = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert response_content["value"] == expected

def test_fibonacci_negative_value(client):
    response = client.get("/fibonacci", {"n": -5})
    response_content = json.loads(response.content)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Ensure this value is greater than or equal to 0." in response_content.get("n")[0]

def test_fibonacci_string_value(client):
    response = client.get("/fibonacci", {"n": "hola"})
    response_content = json.loads(response.content)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "A valid integer is required." in response_content.get("n")[0]