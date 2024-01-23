from ansible.module_utils.basic import AnsibleModule
import requests
from urllib.parse import urljoin

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/"


def api_request(method, url, headers, data=None, params=None):
    """ Helper function to make API requests. """
    response = requests.request(method, url, headers=headers, json=data, params=params)
    return response.status_code, response.json()


def get_headers(api_token):
    """ Prepare the headers for the API request. """
    return {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }


def get_pages_projects(api_token, account_id, page=None):
    """ Get the list of pages projects. """
    data = []
    page = 1
    while True:
        params = {}
        params["page"] = page
        url = urljoin(API_BASE_URL, f"{account_id}/pages/projects")
        status_code, response = api_request("GET", url, headers=get_headers(api_token), params=params)
        if status_code < 300:
            data.extend(response.get("result", []))
            result_info = response.get("result_info", {})
            total_pages = result_info.get("total_pages", 0)

            # If there are more pages, update the page number and continue the loop
            if page < total_pages:
                page += 1
            else:
                break
        else:
            return status_code, response.get("errors", {})
    return status_code, data


def create_pages_project(api_token, account_id, project_name, project_details):
    """ Create a pages project. """
    url = urljoin(API_BASE_URL, f"{account_id}/pages/projects")
    project_details['name'] = project_name
    return api_request("POST", url, get_headers(api_token), project_details)


def delete_pages_project(api_token, account_id, project_name):
    """ Delete a pages project. """
    url = urljoin(API_BASE_URL, f"{account_id}/pages/projects/{project_name}")
    return api_request("DELETE", url, get_headers(api_token))


def update_pages_project(api_token, account_id, project_name, project_details):
    """ Update a pages project. """
    url = urljoin(API_BASE_URL, f"{account_id}/pages/projects/{project_name}")
    return api_request("PATCH", url, get_headers(api_token), project_details)


def find_and_compare_page_project(search_result, project_name):
    exist = False
    for item in search_result:
        if item['name'] == project_name:
            exist = True
    return exist


def run_module():
    """ Main module execution. """
    module_args = {
        "api_token": {"type": 'str', "required": True},
        "state": {"type": 'str', "required": True, "choices": ['present', 'absent']},
        "account_id": {"type": 'str', "required": True},
        "name": {"type": 'str', "required": True},
        "project_details": {"type": 'dict', "required": False}
    }

    result = {
        "changed": False,
        "message": ''
    }

    module = AnsibleModule(argument_spec=module_args,
                           supports_check_mode=False)

    api_token = module.params['api_token']
    state = module.params['state']
    account_id = module.params['account_id']
    project_name = module.params['name']
    project_details = module.params['project_details']

    status_code, response = get_pages_projects(api_token, account_id)
    if status_code not in (200, 201):
        module.fail_json(msg='Error fetching project details', error=response)

    project_exists = find_and_compare_page_project(response, project_name)
    if state == 'present':
        if project_exists:
            status_code, response = update_pages_project(
                api_token, account_id, project_name, project_details)
            if status_code in (200, 201):
                result['changed'] = True
                result['message'] = 'Project updated successfully.'
            else:
                module.fail_json(msg='Error updating project', error=response)
        else:
            status_code, response = create_pages_project(
                api_token, account_id, project_name, project_details)
            if status_code in (200, 201):
                result['changed'] = True
                result['message'] = 'Project created successfully.'
            else:
                module.fail_json(msg='Error creating project', error=response)
    elif state == 'absent':
        if project_exists:
            status_code, response = delete_pages_project(
                api_token, account_id, project_name)
            if status_code in (200, 201):
                result['changed'] = True
                result['message'] = 'Project deleted successfully.'
            else:
                module.fail_json(msg='Error deleting project', error=response)
        else:
            result['message'] = 'Project does not exist or already deleted.'

    module.exit_json(**result)


def main():
    """ Main entry point. """
    run_module()


if __name__ == '__main__':
    main()
