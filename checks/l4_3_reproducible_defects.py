import subprocess
import json

# Required Github permissions: "Issues" and "Contents" repository permissions (read)
# Rule: L4.3 (Reproducible defect tickets): Check for implementation of reproducible defect reporting
# Ideas: Check for bug report templates, reproducibility labels, and issues with reproduction steps
#        Could be extended to analyze the quality of reproduction steps or automation of reproduction

def check_l4_3_reproducible_defects(repo):
    try:
        indicators = []

        # Check for issue templates, particularly bug report templates
        templates_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/contents/.github/ISSUE_TEMPLATE'],
            capture_output=True, text=True
        )
        if templates_result.returncode == 0:
            templates = json.loads(templates_result.stdout)
            for template in templates:
                if 'bug' in template['name'].lower() or 'defect' in template['name'].lower():
                    indicators.append("Bug report template found")
                    break

        # Check for labels related to reproducibility
        labels_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/labels'],
            capture_output=True, text=True
        )
        if labels_result.returncode == 0:
            labels = json.loads(labels_result.stdout)
            reproducible_labels = [label for label in labels if 'reproducible' in label['name'].lower()]
            if reproducible_labels:
                indicators.append(f"Reproducibility labels found: {', '.join([l['name'] for l in reproducible_labels])}")

        # Check for issues with reproducibility information in their body
        issues_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/issues?state=all&per_page=100'],
            capture_output=True, text=True
        )
        if issues_result.returncode == 0:
            issues = json.loads(issues_result.stdout)
            reproducible_issues = [
                issue for issue in issues 
                if issue.get('body') and ('steps to reproduce' in issue['body'].lower() or 'reproduction steps' in issue['body'].lower())
            ]
            if reproducible_issues:
                indicators.append(f"Found {len(reproducible_issues)} issues with reproduction steps")

        if indicators:
            return f"Reproducible defect tickets likely configured: {', '.join(indicators)}"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
