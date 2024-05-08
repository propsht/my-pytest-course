import json
from typing import List

import pytest
from django.urls import reverse

from api.coronavstech.companies.models import Company

companies_url = reverse("companies-list")
pytestmark = pytest.mark.django_db


# -------------------- Test GET Companies --------------------


def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


@pytest.fixture
def amazon() -> Company:
    return Company.objects.create(name="Amazon")


def test_one_company_exist_should_succeed(client, amazon) -> None:

    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == amazon.name
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


# -------------------- Test POST Companies --------------------


def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_exist_company_should_fail(client) -> None:
    Company.objects.create(name="Netflix")
    response = client.post(
        path=companies_url,
        data={
            "name": "Netflix",
        },
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this name already exists."]
    }


def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:

    response = client.post(
        path=companies_url,
        data={"name": "test company name"},
    )
    assert response.status_code == 201
    response_content = response.json()
    assert response_content.get("name") == "test company name"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    response = client.post(
        path=companies_url,
        data={"name": "test company name", "status": "Layoffs"},
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    # assert response_content.get("name") == "test company name"
    assert response_content.get("status") == "Layoffs"
    # assert response_content.get("application_link") == ""
    # assert response_content.get("notes") == ""


def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(
        path=companies_url,
        data={"name": "test company name", "status": "WrongStatus"},
    )
    assert response.status_code == 400
    assert "WrongStatus" in str(response.content)
    assert "is not a valid choice." in str(response.content)


@pytest.mark.xfail
def test_should_be_ok_if_fails() -> None:
    assert 1 == 2


@pytest.mark.skip
def test_should_be_skipped() -> None:
    assert 1 == 2


# -------------------- Learn about fixtures tests --------------------


@pytest.fixture
def companies(request, company) -> List[Company]:
    companies = []
    names = request.param
    for name in names:
        companies.append(company(name=name))

    return companies


@pytest.fixture()
def company(**kwargs):
    def _company_factory(**kwargs) -> Company:
        company_name = kwargs.pop("name", "Test Company LLC")
        return Company.objects.create(name=company_name, **kwargs)

    return _company_factory


@pytest.mark.parametrize(
    "companies", [["Twitch", "TikTok", "Test Company LLC"], ["Facebook", "Instagram"]],
    ids=["3 T companies", "Zuckerberg's companies"],
    indirect=True
)
def test_multiple_companies_exist_should_succeed(client, companies) -> None:

    company_names = set(map(lambda x: x.name, companies))
    print(company_names)
    response_companies = client.get(companies_url).json()
    assert len(company_names) == len(response_companies)
    response_company_names = set(
        map(lambda company: company.get("name"), response_companies)
    )
    assert company_names == response_company_names


# def test_multiple_companies_exist_should_succeed(client) -> None:
#     twitch = Company.objects.create(name="Twitch")
#     tiktok = Company.objects.create(name="TikTok")
#     test_company = Company.objects.create(name="Test Company LLC")
#     company_names = {twitch.name, tiktok.name, test_company.name}
#     response_companies = client.get(companies_url).json()
#     assert len(company_names) == len(response_companies)
#     response_company_names = set(
#         map(lambda company: company.get("name"), response_companies)
#     )
#     assert company_names == response_company_names
