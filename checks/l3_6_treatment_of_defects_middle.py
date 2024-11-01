import subprocess
import json

# Required Github permissions: "Administration" repository permissions (read)
# L3.6 (Treatment of defects with severity middle)
# Description: Vulnerabilities with severity middle are added to the quality gate.
# Rule: Vulnerabilities with severity middle are added to the quality gate.
# Ideas: Check if dependabot alerts for medium vulnerabilities are added to the quality gate
def check_l3_4_defect_visualization(repo):
    try:
        vulnerability_check_keyword = "medium-vulnerability"
        branch = "main"

        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/rules/branches/{branch}'],
            capture_output=True, text=True, check=True
        )

        rulesets = json.loads(result.stdout)
       
        for ruleset in rulesets:
            if ruleset['type'] == 'required_status_checks':
                for check in ruleset['parameters']['required_status_checks']:
                    if vulnerability_check_keyword in check['context']:
                        return f"Ruleset '{ruleset['ruleset_id']}' applies to '{branch}' and includes a required status check for medium vulnerabilities"
                            
        return  "No ruleset with required status checks for medium vulnerabilities found for branch main"
          
    except subprocess.CalledProcessError as e:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error"
    except Exception as e:
        #return f"Error: {str(e)}"
        return "Error exception"
    