import subprocess
import json
from datetime import datetime, timedelta

def check_l2_3_automated_pr_merges(repo):
    try:
        # Check for auto merged PRs from the last 30 days
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=100'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            prs = json.loads(result.stdout)
            automated_merges = []
            for pr in prs:
                if pr.get('merged_at'):
                    merged_at = datetime.fromisoformat(pr['merged_at'].rstrip('Z'))
                    if merged_at > datetime.fromisoformat(thirty_days_ago):
                        merged_by = pr.get('merged_by', {})
                        if merged_by and merged_by.get('type') == 'Bot':
                            automated_merges.append(pr)

            if automated_merges:
                return f"Detected ({len(automated_merges)} in last 30 days)"
            else:
                return "Not detected"
        else:
            return "Unable to check"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
