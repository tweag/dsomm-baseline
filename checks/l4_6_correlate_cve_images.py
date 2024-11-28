import subprocess
import json
import base64

# Required Github permissions: "Contents" and "Actions" repository permissions (read)
# Rule: L4.6 (Correlate known vulnerabilities in infrastructure with new image versions)
# Ideas: Check for configuration files of vulnerability scanning tools and related GitHub Actions workflows
#        Could be extended to analyze specific tool configurations or correlation methods

def check_l4_6_correlate_cve_images(repo):
    try:
        correlation_indicators = []

        # Check for common vulnerability scanning and correlation tools
        tool_configs = {
            'Trivy': ['.trivyignore', 'trivy.yaml', 'trivy-config.yaml'],
            'Clair': ['clair-config.yaml'],
            'Snyk': ['.snyk', 'snyk.yaml'],
            'Dependabot': ['.github/dependabot.yml'],
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
                    correlation_indicators.append(f"{tool} config found: {file}")

        # Check for GitHub Actions workflows related to vulnerability scanning
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
                if workflow_content.returncode == 0:
                    workflow_data = json.loads(workflow_content.stdout)
                    if 'content' in workflow_data:
                        content = workflow_data['content']
                        decoded_content = base64.b64decode(content).decode('utf-8').lower()
                        
                        # Check for keywords related to vulnerability scanning in workflow content
                        if any(keyword in decoded_content for keyword in ['codeql', 'vulnerability', 'security scan', 'trivy', 'clair', 'snyk']):
                            correlation_indicators.append(f"Vulnerability scanning workflow: {workflow['name']}")

        if correlation_indicators:
            return f"Vulnerability correlation enabled: {'; '.join(correlation_indicators)}"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
