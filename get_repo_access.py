import requests
import os

def get_repo_collaborators(owner, repo, token):
    """Get the list of collaborators with access to the repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/collaborators"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return [collaborator['login'] for collaborator in response.json()]
    else:
        print(f"Error fetching collaborators: {response.status_code}, {response.text}")
        return []

def get_repo_teams(owner, repo, token):
    """Get the list of teams with access to the repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/teams"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return [team['slug'] for team in response.json()]
    else:
        print(f"Error fetching teams: {response.status_code}, {response.text}")
        return []

def get_team_members(org, team_slug, token):
    """Get the list of members of a given team in an organization."""
    url = f"https://api.github.com/orgs/{org}/teams/{team_slug}/members"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return [member['login'] for member in response.json()]
    else:
        print(f"Error fetching team members: {response.status_code}, {response.text}")
        return []

def main():
    # Get environment variables
    owner = os.getenv('OWNER')
    repo = os.getenv('REPO')
    token = os.getenv('GITHUB_TOKEN')

    # Fetch collaborators
    collaborators = get_repo_collaborators(owner, repo, token)
    # Fetch teams with access to the repo
    teams = get_repo_teams(owner, repo, token)
    # Collect team members for each team
    all_team_members = []
    for team_slug in teams:
        all_team_members += get_team_members(owner, team_slug, token)
    # Write combined list of users to a file
    with open("access_report.txt", "w") as f:
        # Write collaborators and team members into the file
        #all_users = collaborators + all_team_members
        all_users = all_team_members

        for user in all_users:
            f.write(f"{user}\n")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    main()
