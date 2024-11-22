import subprocess
import json

# Required Github permissions: "User" permissions (read)
# Rule: L2.4 (MFA enabled): Check if Multi-Factor Authentication is enabled for the repository owner
# Ideas: Check MFA status for the repository owner
#        Could be extended to check MFA status for all collaborators or organization members

def check_l2_4_mfa(repo):
    try:
        # Get the repository owner using GitHub CLI
        owner_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}'],
            capture_output=True, text=True
        )
        if owner_result.returncode == 0:
            # Parse the JSON output to get the owner's login
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
            # Parse the JSON output to get the user's information
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
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
