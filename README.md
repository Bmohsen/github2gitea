## Github to Gitea 
these are useful scripts for easily migrating, deleting and etc ... of your organization's repositories from github to your own hosted Gitea!
tested on latest stable build of Gitea and api version v1.

## Content
- [Install](#installation)
- [Scripts](#scripts)
- [Environments](#environments)


### Important
- in order to use scripts please make sure you already have enabled Gitea swagger Api in Gitea Config. more [info](https://docs.gitea.io/en-us/config-cheat-sheet/#api-api)
- the migration script does not import your labels, pull requests, milestones and etc ... , it's only make a mirror from repositories with all branches.

## Installation

### 1- Run with Virtual Environment (recommended)
if you don't want to setup virtual environments skip this step.

- pull this repository
- setup new python virtual environments , instructions [here](https://docs.python.org/3/tutorial/venv.html)(recommended) 
- make sure you are in the env terminal.
- run ```pip install -r requirement.txt```
- rename .env-example to .env
- fill the env
- now you can run the scripts you want with ``` python SCRIPT_NAME.py ```

### 2- Install without Virtual Environment
- pull this repository
- run ```pip install -r requirement.txt```
- rename .env-example to .env
- fill the env
- now you can run the scripts you want with ``` python SCRIPT_NAME.py ```


## Scripts

- ``` github_to_gitea_migrator.py ``` this script migrate all repositories from your own or organizations(if you have access) to your Gitea instance.

- ``` multiple_repose_delete.py ``` this script delete all of user or organization repositories in your Gitea instance.

## Environments
| NAME                   | Example                 | INFO                                                                                                                                                                                          |
|------------------------|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GITEA_URL              | https://git.example.com | your Gitea url                                                                                                                                                                                |
| GITEA_USERNAME         | git                     | Gitea APP_USER , [click](https://docs.gitea.io/en-us/config-cheat-sheet/#overall-default)                                                                                                     |
| GITEA_PASSWORD         | password                | GITEA_USERNAME password                                                                                                                                                                       |
| GITEA_USER             | john                    | Gitea user for migration , example: username of your account in the Gitea. for migrating organization repositories this user must be in the owner group of that organization.                 |
| GITEA_USER_PASSWORD    | password                | Gitea user password|
| GITEA_REPOSITORY_OWNER | test                    | username of user or organization name, example: if you set this to Google all repositories from Github will be migrate to ``` https://git.example.com/Google ```                              |
| GITEA_TOKEN            | token                   | click [here](https://docs.gitea.io/en-us/api-usage/#generating-and-listing-api-tokens) for learning how to generate token                                                                     |
| GITHUB_ORGNAME         | organization name       | your organization name in the Github                                                                                                                                                          |
| GITHUB_TOKEN           | token                   | click [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) for learning how the generate token in Github. |
| GITHUB_USERNAME        | john-doe                | your Github username                                                                                                                                                                          |
| GITHUB_PASSWORD        | password                | your Github password                                                                                                                                                                          |