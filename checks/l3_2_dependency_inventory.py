import subprocess
import json

# Required Github permissions: "Contents" repository permissions (read)
# Rule: Inventory of dependencies
# Ideas: Check for the presence of a Software Bill of Materials (SBOM) or dependency graph
#        Could be extended to analyze specific dependency management files or tools

def check_l3_2_dependency_inventory(repo):
    try:
        # Check for SBOM
        sbom_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/dependency-graph/sbom'],
            capture_output=True, text=True
        )
        
        # Check for dependency graph
        graph_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/dependency-graph/dependencies'],
            capture_output=True, text=True
        )
        
        if sbom_result.returncode == 0:
            sbom_data = json.loads(sbom_result.stdout)
            package_count = len(sbom_data['sbom'].get('packages', []))
            return f"Detected (SBOM with {package_count} packages)"
        elif graph_result.returncode == 0:
            graph_data = json.loads(graph_result.stdout)
            dependency_count = sum(len(manifest['dependencies']) for manifest in graph_data.get('dependencies', []))
            return f"Detected (Dependency graph with {dependency_count} dependencies)"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
