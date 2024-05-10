import pytest
import requests
import json



testing_env_companies_url = "http://127.0.0.1:8000/companies/"

# -------------------- Test GET Companies --------------------


@pytest.mark.skip_in_ci
def test_zero_companies_django_agnostic() -> None:
    response = requests.get(url=testing_env_companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


# -------------------- Test POST Companies --------------------
@pytest.mark.skip_in_ci
def test_create_company_with_layoffs_django_agnostic() -> None:
    response = requests.post(
        url=testing_env_companies_url,
        json={"name": "test company name", "status": "Layoffs"},
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("status") == "Layoffs"

    cleanup_company(company_id=response_content["id"])


def cleanup_company(company_id: str) -> None:
    response = requests.delete(url=f"http://127.0.0.1:8000/companies/{company_id}")
    assert response.status_code == 204


@pytest.mark.restful
def test_apple7_api() -> None:
    response = requests.get(url="https://api.restful-api.dev/objects/7")

    assert response.status_code == 200
    print(response.content)
    response_content = json.loads(response.content)
    assert response_content["id"] == "7"
    assert response_content["name"] == "Apple MacBook Pro 16"
    assert response_content["data"]["year"] == 2019
    assert response_content["data"]["price"] == 1849.99
    assert response_content["data"]["CPU model"] == "Intel Core i9"
    assert response_content["data"]["Hard disk size"] == "1 TB"


import responses


@pytest.mark.restful
@responses.activate
def test_mocked_apple7_api() -> None:
    responses.add(
        method=responses.GET,
        url="https://api.restful-api.dev/objects/7",
        json={
            "id": "7",
            "name": "Apple MacBook Pro 20",
            "data": {
                "year": 2040,
                "price": 1849.99,
                "CPU model": "Intel Core i9",
                "Hard disk size": "1 TB",
            },
        },
        status=200,
    )
    assert process_restful() == 29


def process_restful() -> int:
    response = requests.get(url="https://api.restful-api.dev/objects/7")
    response_content = json.loads(response.content)
    if response.status_code != 200:
        raise ValueError("Request to Restful API FAILED!")

    device_name = response_content["name"]
    if device_name == "Apple MacBook Pro 20":
        return 29
    return 42

    # response = requests.get(url="https://api.restful-api.dev/objects/7")
    #
    # assert response.status_code == 200
    # response_content = json.loads(response.content)
    # assert response_content["id"] == "7"
    # assert response_content["name"] == "Apple MacBook Pro 20"
    # assert response_content["data"]["year"] == 2040
    # assert response_content["data"]["price"] == 1849.99
    # assert response_content["data"]["CPU model"] == "Intel Core i9"
    # assert response_content["data"]["Hard disk size"] == "1 TB"
