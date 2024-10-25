import subprocess
import json

def check_l2_4_mfa(repo):
    try:
        # Get the repository owner
        owner_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}'],
            capture_output=True, text=True
        )
        if owner_result.returncode == 0:
            repo_info = json.loads(owner_result.stdout)
            owner = repo_info['owner']['login']
        else:
            return "Unable to check"

        # Check MFA status for the repository owner
        user_result = subprocess.run(
            ['gh', 'api', f'/users/{owner}'],
            capture_output=True, text=True
        )
        if user_result.returncode == 0:
            user_info = json.loads(user_result.stdout)
            if user_info.get('two_factor_authentication'):
                return f"MFA Enabled for {owner}"
            else:
                return f"Not Enabled"
        else:
            return "Unable to check"
    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error"
    except Exception as e:
        return f"Error: {str(e)}"
