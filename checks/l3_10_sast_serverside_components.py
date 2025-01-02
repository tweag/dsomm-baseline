import subprocess
import json

# Required Github permissions: "Contents" and "Actions" repository permissions (read)
# Rule: Static analysis for important server-side components
# Ideas: Check for server-side static analysis tool configurations and related GitHub Actions workflows
#        Could be extended to analyze specific tool outputs or coverage of critical server components

def check_l3_10_sast_serverside_components(repo):
    try:
        analysis_indicators = []

        # Check for common server-side static analysis tool config files
        config_files = {
            'Pylint': ['.pylintrc', 'pylintrc'],
            'Flake8': ['.flake8', 'setup.cfg'],
            'Rubocop': ['.rubocop.yml'],
            'PHP_CodeSniffer': ['phpcs.xml', 'phpcs.xml.dist'],
            'SonarQube': ['sonar-project.properties'],
            'Checkstyle': ['checkstyle.xml']
        }

        for tool, files in config_files.items():
            for file in files:
                result = subprocess.run(
                    ['gh', 'api', f'/repos/{repo}/contents/{file}'],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    analysis_indicators.append(f"{tool} config found: {file}")
                    break  # Found a config file for this tool, move to next

        # Check for GitHub Actions workflows related to server-side static analysis
        actions_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/workflows'],
            capture_output=True, text=True
        )

        if actions_result.returncode == 0:
            workflows = json.loads(actions_result.stdout)
            for workflow in workflows['workflows']:
                if any(keyword in workflow['name'].lower() for keyword in ['pylint', 'flake8', 'rubocop', 'phpcs', 'sonarqube', 'checkstyle', 'static analysis']):
                    analysis_indicators.append(f"GitHub Action: {workflow['name']}")

        if analysis_indicators:
            return f"Server-side static analysis detected: {', '.join(analysis_indicators)}"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
