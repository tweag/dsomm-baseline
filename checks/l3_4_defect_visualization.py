import subprocess
import json

# Required Github permissions: "Administration" repository permissions (read)
# L3.4 (Defect visualization) NOTE: on others checks this is considered a L2
# Description: Vulnerabilities are simple visualized.
# Rule: Check if the repository has vulnerability alerts enabled
# Ideas: Check if dependabot is enabled
def check_l3_4_defect_visualization(repo):
    try:
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/vulnerability-alerts'],
            capture_output=True, text=True, check=True
        )
        if result.returncode == 0:
            print(f"Vulnerability alerts are enabled for the repository.")
        else:
            print(f"Vulnerability alerts are not enabled for the repository.")
          
    except subprocess.CalledProcessError as e:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error"
    except Exception as e:
        #return f"Error: {str(e)}"
        return "Error exception"