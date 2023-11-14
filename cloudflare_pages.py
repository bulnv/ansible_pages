from ansible.module_utils.basic import AnsibleModule
import requests

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts"

def get_pages_projects(api_token, account_id):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    response = requests.get("{}/{}/pages/projects".format(API_BASE_URL, account_id), headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        return True, response.json()
    else:
        return False, response.json()
    
def create_pages_project(api_token, account_id, project_details):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    response = requests.post("{}/{}/pages/projects".format(API_BASE_URL, account_id), headers=headers, 
                             json=project_details)
    
    if response.status_code == 200 or response.status_code == 201:
        return True, {}
    else:
        return False, response.json()
    
def delete_pages_project(api_token, account_id, project_details):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    response = requests.delete("{}/{}/pages/projects/{}".format(API_BASE_URL, account_id, project_details['name']), headers=headers)
    
    if response.status_code == 200 or response.status_code == 201:
        return True, {}
    else:
        return False, response.json()

def find_and_compare_page_project(search_result, project_details):
    exist = False
    equal = False
    for item in search_result['result']:
        if item['name'] == project_details['name']:
            exist = True
    return exist, equal

def run_module():
    module_args = dict(
        api_token=dict(type='str', required=True),
        state=dict(type='str', required=True, choices=['present', 'absent']),
        account_id=dict(type='str', required=True),
        project_details=dict(type='dict', required=False)
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )
    
    api_token = module.params['api_token']
    state = module.params['state']
    project_details = module.params['project_details']
    account_id = module.params['account_id']

    succ, response = get_pages_projects(api_token, account_id)
    if not succ:
        pass
    else:
        current_state = response
    exist, equal = find_and_compare_page_project(current_state, project_details)

    if state == 'present':
        if exist:
            result['changed'] = False
            result['message'] = 'Project already there'
            result['response'] = 'Project already there'
        else:
            success, response = create_pages_project(api_token, account_id, project_details)
            if success == True:
                result['changed'] = True
                result['message'] = 'Project created successfully.'
                result['response'] = response
            else:
                module.fail_json(msg='Error creating project', error=response)
    elif state == 'absent':
        if exist:
            success, response = delete_pages_project(api_token, account_id, project_details)
            if success == True:
                result['changed'] = True
                result['message'] = 'Project deleted successfully.'
                result['response'] = response
            else:
                module.fail_json(msg='Error deleting project', error=response)
        else:
            result['changed'] = False
            result['message'] = 'Project already deleted'
            result['response'] = 'Project already deleted'
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
