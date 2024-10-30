import subprocess
import json
import base64

def check_l5_3_sast_all(repo):
    try:
        static_analysis_indicators = []

        # Check for generic sast tool config files
        config_files = [
            '.eslintrc', '.pylintrc', 'sonar-project.properties', '.golangci.yml', 'tslint.json',
            '.rubocop.yml', 'stylelint.config.js', '.ktlint.yml', '.swiftlint.yml'
        ]

        for file in config_files:
            result = subprocess.run(
                ['gh', 'api', f'/repos/{repo}/contents/{file}'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                static_analysis_indicators.append(f"Config file: {file}")

        # Look GitHub Actions workflows for static analysis
        actions_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/workflows'],
            capture_output=True, text=True
        )

        if actions_result.returncode == 0:
            workflows = json.loads(actions_result.stdout)
            for workflow in workflows['workflows']:
                if any(keyword in workflow['name'].lower() for keyword in ['lint', 'analyze', 'sonar', 'static analysis']):
                    static_analysis_indicators.append(f"GitHub Action: {workflow['name']}")

        if static_analysis_indicators:
            return f"Static analysis configured: {', '.join(static_analysis_indicators)}"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
