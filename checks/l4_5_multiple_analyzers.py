import subprocess
import json
import base64

# Required Github permissions: "Contents" and "Actions" repository permissions (read)
# Rule: L4.5 (Usage of multiple analyzers): Check for implementation of multiple static analysis tools
# Ideas: Check for configuration files of various analyzers and related GitHub Actions workflows
#        Could be extended to analyze specific tool configurations or integration methods

def check_l4_5_multiple_analyzers(repo):
    analyzers = {}

    # List of common analyzers and their associated configuration files
    analyzer_configs = {
        'SonarQube': ['sonar-project.properties', '.sonarcloud.properties'],
        'ESLint': ['.eslintrc', '.eslintrc.js', '.eslintrc.json', '.eslintrc.yml'],
        'Pylint': ['.pylintrc', 'pylintrc'],
        'RuboCop': ['.rubocop.yml'],
        'Checkstyle': ['checkstyle.xml'],
        'Flake8': ['.flake8', 'setup.cfg'],
        'Stylelint': ['.stylelintrc', '.stylelintrc.json', '.stylelintrc.yml'],
    }

    try:
        # Check for configuration files of each analyzer
        for analyzer, config_files in analyzer_configs.items():
            for file in config_files:
                result = subprocess.run(
                    ['gh', 'api', f'/repos/{repo}/contents/{file}'],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    analyzers[analyzer] = f"Config file: {file}"
                    break  # Found a config file for this analyzer, move to next

        # Check for GitHub Actions workflows that might use analyzers
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
                        
                        # Check for analyzer keywords in workflow content
                        for analyzer in analyzer_configs.keys():
                            if analyzer.lower() in decoded_content and analyzer not in analyzers:
                                analyzers[analyzer] = f"GitHub Action: {workflow['name']}"

        # Determine the result based on the number of analyzers found
        if len(analyzers) > 1:
            return f"Multiple analyzers detected: {', '.join([f'{k} ({v})' for k, v in analyzers.items()])}"
        elif len(analyzers) == 1:
            analyzer, details = list(analyzers.items())[0]
            return f"Single analyzer detected: {analyzer} ({details})"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
