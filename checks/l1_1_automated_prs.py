import subprocess
import json
from datetime import datetime, timedelta

def check_l1_1_automated_prs(repo):
    try:
        # Check PRs from the last 30 days
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/pulls?state=all&sort=created&direction=desc&per_page=100&since={thirty_days_ago}'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            prs = json.loads(result.stdout)
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
