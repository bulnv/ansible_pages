import pytest
import requests_mock
from ..cloudflare_pages import api_request, get_headers, find_and_compare_page_project, create_pages_project


def test_api_request():
    with requests_mock.Mocker() as m:
        m.get('https://api.example.com/data',
              json={'key': 'value'}, status_code=200)
        status_code, response = api_request(
            'GET', 'https://api.example.com/data', {})

        assert status_code == 200
        assert response == {'key': 'value'}


def test_get_headers():
    token = "asd_token_test"
    assert get_headers(token) == {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def test_find_and_compare_page_project():
    project_name = 'testname'
    search_result = {'result': [{'name': project_name}]}
    assert find_and_compare_page_project(search_result, project_name) == True
    assert find_and_compare_page_project([], project_name) == False


def test_create_pages_project():
    api_token = "test_token"
    account_id = "test_account"
    project_name = "test_project"
    project_details = {"detail_key": "detail_value"}

    expected_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects"
    expected_headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    expected_response = {
        "success": True,
        "result": {
            "name": project_name,
            "details": project_details
        }
    }

    with requests_mock.Mocker() as m:
        m.post(expected_url, json=expected_response, status_code=200)
        status_code, response = create_pages_project(api_token, account_id, project_name, project_details)

        assert status_code == 200
        assert response == expected_response