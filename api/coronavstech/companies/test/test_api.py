import json
from unittest import TestCase

import pytest
from django.urls import reverse
from django.test import Client

from api.coronavstech.companies.models import Company


@pytest.mark.django_db
class TestGetCompanies(TestCase):

    def test_zero_companies_should_return_empty_list(self) -> None:
        client = Client()
        companies_url = reverse("companies-list")
        response = client.get(companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exist_should_succeed(self) -> None:
        client = Client()
        test_company = Company.objects.create(name="Amazon")
        # the same url
        companies_url = reverse("companies-list")
        # the same request
        response = client.get(companies_url)
        # print(response.content)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), test_company.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

        test_company.delete()