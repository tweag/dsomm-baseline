import subprocess
import json
from datetime import datetime, timedelta

# Required Github permissions: "Pull requests" repository permissions (read)
# Rule: L1.1 (Automated PRs for patches): Check if there are automated pull requests
# Ideas: Check for PRs created by bot accounts in the last 30 days
#        Could be extended to check for specific bot names or PR titles/content

def check_l1_1_automated_prs(repo):
    try:
        # Calculate the date 30 days ago from now
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()

        # Use GitHub CLI to fetch pull requests from the last 30 days
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/pulls?state=all&sort=created&direction=desc&per_page=100&since={thirty_days_ago}'],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            # Parse the JSON output into a Python object
            prs = json.loads(result.stdout)

            # Filter PRs created by bot accounts
            automated_prs = [pr for pr in prs if pr['user']['type'] == 'Bot']

            if automated_prs:
                return f"Detected ({len(automated_prs)} in last 30 days)"
            else:
                return "Not detected"
        else:
            return "Unable to check"
    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error"
    except Exception as e:
        #return f"Error: {str(e)}"
        return "Error exception"
