import subprocess
import json

def get_repos_from_org(org_name):
    try:
        page = 1
        per_page = 100
        hasPages = True
        all_repos = []

        while hasPages:
            result = subprocess.run(
                ['gh', 'api', f'/orgs/{org_name}/repos?per_page={per_page}&page={page}'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0 and result.stdout != '[]':
                all_repos.extend(json.loads(result.stdout))
                page += 1
            else:
                hasPages = False

        return [repo['full_name'] for repo in all_repos]
    except subprocess.CalledProcessError:
        return "Unable to get repos"
    except json.JSONDecodeError:
        return "Error"
    except Exception as e:
        return f"Error: {str(e)}"
