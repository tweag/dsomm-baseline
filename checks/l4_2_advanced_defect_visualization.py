import subprocess
import json

# Required Github permissions: "Contents" and "Actions" repository permissions (read)
# Rule: L4.2 (Advanced visualization of defects): Check for implementation of advanced defect visualization
# Ideas: Check for visualization-related files, tool integrations, and GitHub Actions workflows
#        Could be extended to analyze specific visualization configurations or outputs

def check_l4_2_advanced_defect_visualization(repo):
    try:
        visualization_indicators = []

        # Check for visualization-related files
        viz_files = [
            'diagram.svg',
            'repo-visualization.yml',
            'create-diagram.yml',
            'defect-visualization-config.json'
        ]
        # Use GitHub CLI to check for the existence of each visualization-related file
        for file in viz_files:
            result = subprocess.run(
                ['gh', 'api', f'/repos/{repo}/contents/{file}'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                visualization_indicators.append(f"Visualization file found: {file}")

        # Check for integration with visualization tools
        integrations_to_check = ['veracode', 'snyk']
        # Use GitHub CLI to check for configuration files of specific visualization tools
        for integration in integrations_to_check:
            result = subprocess.run(
                ['gh', 'api', f'/repos/{repo}/contents/.{integration}'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                visualization_indicators.append(f"Integration found: {integration}")

        # Check for GitHub Actions related to visualization
        actions_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/workflows'],
            capture_output=True, text=True
        )
        if actions_result.returncode == 0:
            # Parse the JSON output of workflows
            workflows = json.loads(actions_result.stdout)
            # Check for workflows with visualization-related keywords in their names
            for workflow in workflows['workflows']:
                if any(keyword in workflow['name'].lower() for keyword in ['visualiz', 'diagram', 'defect']):
                    visualization_indicators.append(f"Visualization workflow: {workflow['name']}")

        if visualization_indicators:
            return f"Advanced defect visualization detected: {', '.join(visualization_indicators)}"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
