"""
Unittest way to do testing
Is the email service testing
"""
# Django
from django.urls import reverse
from django.test import Client
from django.core import mail

# Models
from companies.models import Company

# Test and utilities
from django.test import TestCase
import pytest
import json
from unittest.mock import patch
import unittest

# DRF
from rest_framework import status

class EmailUnitTesting(TestCase): 
    def test_send_email_should_succed(self) -> None:
        with self.settings(
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
        ):
            mail.send_mail(
                subject="Test Subject here",
                message="Test message here",
                from_email="testmail@gmail.com",
                recipient_list=["testemail2@gmail.com"],
                fail_silently=False
            )
            # Test that one message has been sent
            self.assertEqual(len(mail.outbox), 1)
            # Verify that the subject of the first message is correct
            self.assertEqual(mail.outbox[0].subject, "Test Subject here")

    def test_send_email_without_arguments_should_send_empty_email(self) -> None:
        client = Client()
        with patch(
            "companies.views.send_mail"
        ) as mocked_send_mail_function:
            response = client.post(path="/send-email")
            response_content = json.loads(response.content)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response_content["status"], "SUCCESS")
            self.assertEqual(response_content["info"], "Email sent successfully")
            mocked_send_mail_function.assert_called_with(
                subject=None,
                message=None,
                from_email="luis.e.3194@gmail.com",
                recipient_list=["luis.e.3194@gmail.com"]
            )

    def test_send_email_with_get_verb_should_fail(self) -> None:
        client = Client()
        response = client.get(path="/send-email")
        assert response.status_code == 405
        assert json.loads(response.content) == {"detail": 'Method "GET" not allowed.'}