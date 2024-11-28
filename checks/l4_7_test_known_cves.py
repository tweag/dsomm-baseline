import subprocess
import json
import base64

# Required Github permissions: "Contents" and "Actions" repository permissions (read)
# Rule: L4.7 (Test for known vulnerabilities): Check for implementation of vulnerability testing
# Ideas: Check for GitHub Advanced Security, vulnerability scanning tool configurations, and related GitHub Actions workflows
#        Could be extended to analyze specific tool configurations or vulnerability testing methods

def check_l4_7_test_known_cves(repo):
    try:
        vulnerability_indicators = []

        # Check if GitHub Advanced Security is enabled for the repository
        repo_info = subprocess.run(
            ['gh', 'api', f'/repos/{repo}'],
            capture_output=True, text=True
        )
        if repo_info.returncode == 0:
            repo_data = json.loads(repo_info.stdout)
            if repo_data.get('security_and_analysis', {}).get('advanced_security', {}).get('status') == 'enabled':
                vulnerability_indicators.append("GitHub Advanced Security enabled")

        # Check for common vulnerability scanning tool configurations
        tool_configs = {
            'Trivy': ['.trivyignore', 'trivy.yaml', 'trivy-config.yaml'],
            'Clair': ['clair-config.yaml'],
            'Snyk': ['.snyk', 'snyk.yaml'],
            'GitHub Advanced Security': ['.github/workflows/codeql-analysis.yml']
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

        # Check for GitHub Actions workflows related to vulnerability scanning
        actions_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/workflows'],
            capture_output=True, text=True
        )

        if actions_result.returncode == 0:
            workflows = json.loads(actions_result.stdout)
            for workflow in workflows.get('workflows', []):
                # Fetch and decode the content of each workflow
                workflow_content = subprocess.run(
                    ['gh', 'api', workflow['url']],
                    capture_output=True, text=True
                )
                if workflow_content.returncode == 0 and 'content' in json.loads(workflow_content.stdout):
                    workflow_data = json.loads(workflow_content.stdout)
                    content = workflow_data['content']
                    decoded_content = base64.b64decode(content).decode('utf-8').lower()
                    # Check for keywords related to vulnerability scanning in workflow content
                    if any(keyword in decoded_content for keyword in ['codeql', 'vulnerability', 'security scan', 'snyk', 'dependabot']):
                        vulnerability_indicators.append(f"Vulnerability scanning workflow: {workflow['name']}")

        if vulnerability_indicators:
            return f"Vulnerability testing config: {'; '.join(vulnerability_indicators)}"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
