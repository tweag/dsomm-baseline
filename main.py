import yaml
import importlib
import csv
from tabulate import tabulate
import os

def load_check_levels(yaml_file):
    with open(yaml_file, 'r') as f:
        return yaml.safe_load(f)

CHECK_LEVELS = load_check_levels('dsomm_checks.yaml')

AVAILABLE_CHECKS = [check['name'] for level in CHECK_LEVELS.values() for check in level if check.get('supported', False)]

def load_check(check_name):
    for level_checks in CHECK_LEVELS.values():
        for check in level_checks:
            if check['name'] == check_name and check.get('supported', False):
                module_name = check.get('module')
                if not module_name:
                    raise ValueError(f"Module name not found for supported check '{check_name}' in checks directory.")
                try:
                    module = importlib.import_module(f'checks.{module_name}')
                    check_function = getattr(module, f'check_{module_name}')
                    return check_function
                except ImportError:
                    raise ImportError(f"Error: Module 'checks.{module_name}' not found. Please ensure the file 'checks/{module_name}.py' exists.")
                except AttributeError:
                    raise AttributeError(f"Error: Function 'check_{module_name}' not found in module 'checks.{module_name}'. Please ensure the function is defined correctly.")
    raise ValueError(f"Not Supported - Manual Process")

def check_repo_security_features(repo, selected_checks):
    results = {}
    for check in selected_checks:
        try:
            check_function = load_check(check)
            results[check] = check_function(repo)
        except (ImportError, AttributeError, ValueError) as e:
            results[check] = str(e)
    return results

def print_check_menu(show_all=False):
    print("Available checks:")
    check_number = 1
    for level, checks in CHECK_LEVELS.items():
        print(f"\n{level}:")
        for check in checks:
            supported = check.get('supported', False)
            if show_all or supported:
                print(f"  {check_number}. {check['name']} {'(Supported)' if supported else '(Not Supported)'}")
                check_number += 1

def get_selected_checks(user_input, show_all=False):
    selected_checks = []
    
    if user_input.strip().upper() == "ALL":
        return [check['name'] for level in CHECK_LEVELS.values() for check in level]

    all_checks = [check['name'] for level in CHECK_LEVELS.values() for check in level]
    displayed_checks = all_checks if show_all else AVAILABLE_CHECKS

    for item in user_input.split(','):
        item = item.strip().upper()
        if item in CHECK_LEVELS:
            selected_checks.extend([check['name'] for check in CHECK_LEVELS[item]])
        elif item.isdigit():
            index = int(item) - 1
            if 0 <= index < len(displayed_checks):
                selected_checks.append(displayed_checks[index])
    
    return list(set(selected_checks))

def get_check_level(check):
    for level, checks in CHECK_LEVELS.items():
        if any(c['name'] == check for c in checks):
            return level
    return "Unknown"

def output_results(all_results, repos, selected_checks, output_format, output_path=None, show_all=True):
    headers = ["Security Feature"] + repos
    table_data = []
    level_stats = {level: {repo: {'total': 0, 'successful': 0} for repo in repos} for level in CHECK_LEVELS}
    total_stats = {repo: {'total': 0, 'successful': 0} for repo in repos}

    for feature in selected_checks:
        level = get_check_level(feature)
        row = [feature]
        for repo in repos:
            result = all_results[repo.strip()][feature]
            row.append(result)
            if any(check['name'] == feature and check.get('supported', False) for checks in CHECK_LEVELS.values() for check in checks):
                level_stats[level][repo]['total'] += 1
                total_stats[repo]['total'] += 1
                if result.lower() not in ['not detected', 'no', 'not available', 'not enabled', 'unable to check', 'error parsing data', 'error exception', 'error']:
                    level_stats[level][repo]['successful'] += 1
                    total_stats[repo]['successful'] += 1
        table_data.append(row)

    # Add level score rows
    for level, repo_stats in level_stats.items():
        if any(stats['total'] > 0 for stats in repo_stats.values()):
            score_row = [f"{level} Score"]
            for repo in repos:
                stats = repo_stats[repo]
                if stats['total'] > 0:
                    score_row.append(f"{stats['successful']}/{stats['total']}")
                else:
                    score_row.append("")
            table_data.append(score_row)

    # Add Total Score row
    total_score_row = ["Total Score"]
    for repo in repos:
        stats = total_stats[repo]
        if stats['total'] > 0:
            total_score_row.append(f"{stats['successful']}/{stats['total']}")
        else:
            total_score_row.append("")
    table_data.append(total_score_row)

    if output_format.lower() == 'csv':
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            csv_filename = output_path
        else:
            csv_filename = 'dsomm.csv'
        
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(table_data)
        print(f"Results have been saved to {csv_filename}")
    else:  # Default to tabular format
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

def main():
    show_all_menu = input("Show all checks in menu (including not supported)?, default is N (y/N): ").strip().lower() == 'y'
    print_check_menu(show_all_menu)
    
    user_input = input("\nEnter the levels (Level1, Level2 etc.,) or specific check numbers or type 'ALL' to run all checks: ")
    selected_checks = get_selected_checks(user_input, show_all_menu)
    
    if not selected_checks:
        print("No valid checks selected. Exiting.")
        return

    repos = input("Enter the repositories to check (comma-separated, format: github-org/repo): ").split(',')
    
    output_format = input("Enter output format (tabular/csv, default is tabular): ").strip() or 'tabular'
    
    output_path = None
    if output_format.lower() == 'csv':
        output_path = input("Enter the path and filename for the CSV file (e.g., /path/to/output.csv): ").strip()
    
    show_all_output = input("Show all checks in output (including Not Supported)?, default is Y (Y/n): ").strip().lower() != 'n'
    
    all_results = {}
    for repo in repos:
        all_results[repo.strip()] = check_repo_security_features(repo.strip(), selected_checks)

    output_results(all_results, repos, selected_checks, output_format, output_path, show_all_output)

if __name__ == "__main__":
    main()
