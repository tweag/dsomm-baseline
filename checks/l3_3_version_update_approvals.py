import subprocess
import json

# Required Github permissions: "Pull requests" repository permissions (read)
# L3.1 (Version Update Approvals)
# Description: On each new version (e.g. Pull Request) of source code or infrastructure components a security peer review of the changes 
#              is performed (two eyes principle) and approval given by the reviewer.
# Rule:  Check if the last PR has requested reviewers
# Ideas: Check if the main branch has prtection rule that allow only to be merged with at least 1 approval (Prevent merging unsigned commits)
#        Check if the last x prs are has reviewer (Ensure that two eyes principle are being used in the past)
#        Some PRs are automated so it will not have a review for example the PRs that are created by dependabot 
def check_l3_1_version_update_approvals(repo):
    try:
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/pulls'],
            capture_output=True, text=True, check=True
        )
        pull_requests = json.loads(result.stdout)
        
        if len(pull_requests) == 0:
            return "No PRs"
        
        if len(pull_requests[0]['requested_reviewers']) > 0:
            return 'Last PR requested for review'
        else:
            return 'Not Detected'
                    
    except subprocess.CalledProcessError as e:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error"
    except Exception as e:
        #return f"Error: {str(e)}"
        return "Error exception"
    
print(check_l3_1_version_update_approvals('home-assistant/core'))