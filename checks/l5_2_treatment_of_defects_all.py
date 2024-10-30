import subprocess
import json
from datetime import datetime, timedelta

def check_l5_2_treatment_of_defects_all(repo):
    try:
        defect_indicators = []

        # Check for issues labeled as defects
        issues_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/issues?state=all&labels=bug,defect&per_page=100'],
            capture_output=True, text=True
        )
        if issues_result.returncode == 0:
            issues = json.loads(issues_result.stdout)
            if issues:
                defect_indicators.append(f"Found {len(issues)} issues labeled as bugs/defects")

        # Check for pull requests mentioning defect fixes
        prs_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/pulls?state=all&per_page=100'],
            capture_output=True, text=True
        )
        if prs_result.returncode == 0:
            prs = json.loads(prs_result.stdout)
            defect_prs = [pr for pr in prs if 'fix' in pr['title'].lower() or 'bug' in pr['title'].lower()]
            if defect_prs:
                defect_indicators.append(f"Found {len(defect_prs)} PRs related to defect fixes")

        if defect_indicators:
            return f"Defect treatment detected: {', '.join(defect_indicators)}"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
