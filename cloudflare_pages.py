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

def run_module():
    module_args = dict(
        api_token=dict(type='str', required=True),
        action=dict(type='str', required=True, choices=['create', 'update', 'delete', 'get']),
        account_id=dict(type='str', required=True),
        project_details=dict(type='dict', required=False)
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    
    api_token = module.params['api_token']
    action = module.params['action']
    project_details = module.params['project_details']
    account_id = module.params['account_id']
    succ, current_State = get_pages_projects(api_token, account_id)
    if not succ:
        raise(current_State)
    if action == 'create':
        success, response = create_pages_project(api_token, account_id, project_details)
        if success == True:
            result['changed'] = True
            result['message'] = 'Project created successfully.'
            result['response'] = response
        else:
            module.fail_json(msg='Error creating project', error=response)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
