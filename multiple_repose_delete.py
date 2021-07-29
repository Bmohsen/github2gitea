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
GITEA_REPOSITORY_OWNER = os.getenv('GITEA_REPOSITORY_OWNER')
GITEA_USER_PASSWORD = os.getenv('GITEA_USER_PASSWORD ')
GITEA_TOKEN = os.getenv('GITEA_TOKEN')


def deleteOrganizationRepositories():
    orgRepos = requests.get(f'{GITEA_URL}/api/v1/orgs/{GITEA_REPOSITORY_OWNER}/repos', headers={
        'Authorization': f'token {GITEA_TOKEN}'
    })
    for repo in orgRepos.json():
        for key in repo:
            if key == 'owner':
                if(repo[key]['username'] == GITEA_REPOSITORY_OWNER):
                    delete(repo)


def deleteAllUserRepositories():
    orgRepos = requests.get(f'{GITEA_URL}/api/v1/user/repos', headers={
        'Authorization': f'token {GITEA_TOKEN}'
    })
    for repo in orgRepos.json():
        for key in repo:
            if key == 'owner':
                if(repo[key]['username'] == GITEA_REPOSITORY_OWNER):
                    delete(repo)



def delete(repo):
    deletedRepo = requests.delete(f'{GITEA_URL}/api/v1/repos/{GITEA_USER}/{repo["name"]}', headers={
        'Authorization': f'token {GITEA_TOKEN}'
    })
    if deletedRepo.status_code == 204:
        print(f'{repo["name"]} deleted successfully ✅.')


# deleteOrganizationRepositories()
deleteAllUserRepositories()