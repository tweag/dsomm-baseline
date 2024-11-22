import subprocess
import json

# Required Github permissions: "Secret scanning alerts" repository permissions (read)
# Rule: L1.3 (Test for stored secrets): Check if secret scanning is enabled and for any alerts
# Ideas: Check if secret scanning is enabled for the repository
#        Could be extended to check for specific types of secrets or the number of open alerts

def check_l1_3_test_stored_secrets(repo):
    try:
        # Check for secret scanning alerts if enabled
        alerts_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/secret-scanning/alerts'],
            capture_output=True, text=True
        )

        # Check if secret scanning is enabled
        security_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}'],
            capture_output=True, text=True
        )

        if alerts_result.returncode == 0 and security_result.returncode == 0:
            # Parse the repository data JSON
            repo_data = json.loads(security_result.stdout)
            security_and_analysis = repo_data.get('security_and_analysis', {})
            secret_scanning = security_and_analysis.get('secret_scanning', {})

            status = []
            if secret_scanning.get('status') == 'enabled':
                status.append("Secret scanning enabled")
                return f"Detected: {', '.join(status)}"
            else:
                return "Not detected"

        elif alerts_result.returncode != 0:
            return "Not enabled"
        else:
            return "Unable to check"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error"
    except Exception as e:
        return "Error exception"
