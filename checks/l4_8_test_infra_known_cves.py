import subprocess
import json
import base64

# Required Github permissions: "Contents" and "Actions" repository permissions (read)
# Rule: L4.8 (Test of infrastructure components for known vulnerabilities)
# Ideas: Check for infrastructure vulnerability scanning tool configurations and related GitHub Actions workflows
#        Could be extended to analyze specific tool configurations or infrastructure testing methods

def check_l4_8_test_infra_known_cves(repo):
    try:
        vulnerability_indicators = []

        # Check for common infrastructure vulnerability scanning tool configurations
        tool_configs = {
            'Trivy': ['.trivyignore', 'trivy.yaml'],
            'Terrascan': ['.terrascan', 'terrascan.yaml'],
            'Checkov': ['.checkov.yaml', '.checkov.yml'],
            'tfsec': ['.tfsec', 'tfsec.yaml'],
            'Snyk': ['.snyk', 'snyk.yaml']
        }

        # Check for the presence of configuration files for each tool
        for tool, config_files in tool_configs.items():
            for file in config_files:
                result = subprocess.run(
                    ['gh', 'api', f'/repos/{repo}/contents/{file}'],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    vulnerability_indicators.append(f"{tool} config found: {file}")

        # Check for GitHub Actions workflows related to infrastructure vulnerability scanning
        actions_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/workflows'],
            capture_output=True, text=True
        )

        if actions_result.returncode == 0:
            workflows = json.loads(actions_result.stdout)
            for workflow in workflows['workflows']:
                # Fetch and decode the content of each workflow
                workflow_content = subprocess.run(
                    ['gh', 'api', workflow['url']],
                    capture_output=True, text=True
                )
                if workflow_content.returncode == 0 and 'content' in json.loads(workflow_content.stdout):
                    content = json.loads(workflow_content.stdout)['content']
                    decoded_content = base64.b64decode(content).decode('utf-8').lower()
                    
                    # Check for keywords related to infrastructure vulnerability scanning in workflow content
                    if any(keyword in decoded_content for keyword in ['infrastructure', 'iac', 'terraform', 'cloudformation', 'trivy', 'terrascan', 'checkov', 'tfsec', 'snyk', 'lacework']):
                        vulnerability_indicators.append(f"Infrastructure scanning workflow: {workflow['name']}")

        if vulnerability_indicators:
            return f"Infrastructure vulnerability testing likely enabled: {'; '.join(vulnerability_indicators)}"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
