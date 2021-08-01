import os
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
import time
import json  
 
load_dotenv()
     
GITEA_URL = os.getenv('GITEA_URL')
GITEA_USERNAME = os.getenv('GITEA_USERNAME')
GITEA_PASSWORD = os.getenv('GITEA_PASSWORD')
GITEA_USER = os.getenv('GITEA_USER')
GITEA_REPOSITORY_OWNER= os.getenv('GITEA_REPOSITORY_OWNER')
GITEA_TOKEN = os.getenv('GITEA_TOKEN') 
GITHUB_ORGNAME = os.getenv('GITHUB_ORGNAME')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME ')
GITHUB_PASSWORD = os.getenv('GITHUB_PASSWORD')
GITEA_USER_PASSWORD = os.getenv('GITEA_USER_PASSWORD ')

def prettifyJson(content):
    return json.dumps(json.loads(content), indent=4, sort_keys=True)

#
# Get Gitea user
#
def getGiteaUser():
    user_token = requests.get(f'{GITEA_URL}/api/v1/users/{GITEA_USER}/tokens', auth=HTTPBasicAuth(GITEA_USER, GITEA_USER_PASSWORD))
    if user_token.status_code == 401:
        print('[ERROR]: Gitea user or password is invalid.')
        exit()
    response_user = requests.get(
        f'{GITEA_URL}/api/v1/users/{GITEA_USER}')
    if response_user.status_code == 200:
        return response_user
    else:
        raise NameError(response_user.content)



#
#   get github repositories from github api
#
def getGithubRepositories(page):
    response = requests.get(
        f'https://api.github.com/orgs/{GITHUB_ORGNAME}/repos?' +
        f'per_page=100&page={page}',
        headers={'Authorization': 'token ' + GITHUB_TOKEN})
    if response.status_code == 200:
        return response
    else:
        raise NameError(response.content)

#
# migrate from github to the Gitea
#
def migrateGithubToGitea(repository, giteaUser):
    uid = giteaUser['id']
    repo_clone_url = repository['clone_url']
    repo_name = repository['name']
    description = repository['description']
    print(f'Creating repository: {repo_name} from {repo_clone_url}')
    
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))
    response_migrate = session.post(
        f'{GITEA_URL}/api/v1/repos/migrate',
        json={
            'clone_addr': repo_clone_url.replace(
                'https://github.com',
                f'https://{GITHUB_USERNAME}:' +
                GITHUB_PASSWORD +
                '@github.com'),
            'mirror': False,
            'private': True,
            "issues": False,
            "labels": False,
            "milestones": False,
            "pull_requests": False,
            "releases": False,
            "wiki": False,
            'repo_name': repo_name,
            'uid': uid,
            'repo_owner': GITEA_REPOSITORY_OWNER,
            'description': description
        },
        headers= {
            'Authorization': f'token {GITEA_TOKEN}' 
        },
        timeout=120)

    if response_migrate.status_code == 201:
        print(f'[INFO]: {repo_name} migrated successfully ✅')
        pass
    if response_migrate.status_code == 409:
        print(f'[WARNING]: {repo_name} already exists on {GITEA_URL}/{GITEA_REPOSITORY_OWNER}, moving on ... ⚠')
        pass
    if response_migrate.status_code == 401 or response_migrate.status_code == 403 or response_migrate.status_code == 422:
        print(f'[Status: {response_migrate.status_code}]',prettifyJson(response_migrate.content))
        exit()


def startMigrate():
    giteaUser = getGiteaUser().json()
    for n in range(1000):
        page = n + 1
        n = page
        githubRepos = getGithubRepositories(page)
        totalReposCounter = len(githubRepos.json())
        totalRepos = totalReposCounter
        # List Github repos
        if len(githubRepos.json()):
            for repo in githubRepos.json():
                totalReposCounter -= 1
                migrateGithubToGitea(repo, giteaUser)
                if totalReposCounter == 0: 
                    print(f'[INFO]: {totalRepos} repositories migrated from Github to {GITEA_URL} ✅.')  
                    exit()

startMigrate()

