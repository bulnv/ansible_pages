import pytest
import requests_mock
from ..cloudflare_pages_domain import (create_pages_project_domain,
                                       delete_pages_project_domin,
                                       get_pages_project_domains,
                                       update_pages_project_domain)


@pytest.fixture()
def mock_api_token():
    return "test_api_token"


@pytest.fixture()
def mock_account_id():
    return "test_account_id"


@pytest.fixture()
def mock_project_name():
    return "test_project_name"


@pytest.fixture()
def mock_domain_name():
    return "test_domain_name"


def test_get_pages_project_domains_success(mock_api_token, mock_account_id, mock_project_name):
    with requests_mock.Mocker() as m:
        m.get(f"https://api.cloudflare.com/client/v4/accounts/{mock_account_id}/pages/projects/{mock_project_name}/domains",
              json={"result": []}, status_code=200)
        status_code, response = get_pages_project_domains(
            mock_api_token, mock_account_id, mock_project_name)
        assert status_code == 200


def test_create_pages_project_domain_success(mock_api_token, mock_account_id, mock_project_name, mock_domain_name):
    with requests_mock.Mocker() as m:
        m.post(f"https://api.cloudflare.com/client/v4/accounts/{mock_account_id}/pages/projects/{mock_project_name}/domains/",
               json={"success": True}, status_code=201)
        status_code, response = create_pages_project_domain(
            mock_api_token, mock_account_id, mock_project_name, mock_domain_name)
        assert status_code == 201


def test_delete_pages_project_domain_success(mock_api_token, mock_account_id, mock_project_name, mock_domain_name):
    with requests_mock.Mocker() as m:
        m.delete(f"https://api.cloudflare.com/client/v4/accounts/{mock_account_id}/pages/projects/{mock_project_name}/domains/{mock_domain_name}",
                 json={"success": True}, status_code=200)
        status_code, response = delete_pages_project_domin(
            mock_api_token, mock_account_id, mock_project_name, mock_domain_name)
        assert status_code == 200


def test_update_pages_project_domain_success(mock_api_token, mock_account_id, mock_project_name, mock_domain_name):
    with requests_mock.Mocker() as m:
        m.patch(f"https://api.cloudflare.com/client/v4/accounts/{mock_account_id}/pages/projects/{mock_project_name}/domains/{mock_domain_name}",
                json={"success": True}, status_code=200)
        status_code, response = update_pages_project_domain(
            mock_api_token, mock_account_id, mock_project_name, mock_domain_name)
        assert status_code == 200


def test_get_pages_project_domains_failure(mock_api_token, mock_account_id, mock_project_name):
    with requests_mock.Mocker() as m:
        m.get(f"https://api.cloudflare.com/client/v4/accounts/{mock_account_id}/pages/projects/{mock_project_name}/domains",
              json={"error": "Not Found"}, status_code=404)
        status_code, response = get_pages_project_domains(
            mock_api_token, mock_account_id, mock_project_name)
        assert status_code == 404
        assert "error" in response
