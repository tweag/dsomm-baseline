import subprocess
import json

# Required Github permissions: "Contents" and "Actions" repository permissions (read)
# Rule: L4.4 (Static analysis for all self-written components): Check for implementation of static analysis tools
# Ideas: Check for configuration files of common static analysis tools and related GitHub Actions workflows
#        Could be extended to analyze specific tool configurations or coverage of different languages/components

def check_l4_4_sast_self_components(repo):
    try:
        static_analysis_indicators = []

        # Check for configuration files of common static analysis tools
        config_files = [
            '.eslintrc', '.pylintrc', 'sonar-project.properties', '.golangci.yml', 'tslint.json',
            '.rubocop.yml', 'stylelint.config.js', '.ktlint.yml', '.swiftlint.yml'
        ]

        # Use GitHub CLI to check for the existence of each config file
        for file in config_files:
            result = subprocess.run(
                ['gh', 'api', f'/repos/{repo}/contents/{file}'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                static_analysis_indicators.append(f"Config file: {file}")

        # Check for GitHub Actions workflows related to static analysis
        actions_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/workflows'],
            capture_output=True, text=True
        )

        if actions_result.returncode == 0:
            # Parse the JSON output of workflows
            workflows = json.loads(actions_result.stdout)
            # Check for workflows with static analysis-related keywords in their names
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
