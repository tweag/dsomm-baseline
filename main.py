import importlib
import csv
from tabulate import tabulate
import sys
import os

CHECK_LEVELS = {
    'LEVEL1': ['l1_1_automated_prs', 'l1_2_versioning', 'l1_3_test_stored_secrets'],
    'LEVEL2': ['l2_1_artifact_pinning', 'l2_2_sbom', 'l2_3_automated_pr_merges', 'l2_4_mfa', 'l2_5_serverside_sca', 'l2_6_test_libyear'],
    'LEVEL3': ['l3_1_code_signing', 'l3_2_dependency_inventory', 'l3_3_version_update_approvals', 'l3_4_defect_visualization', 'l3_5_patch_management_stats', 'l3_6_treatment_of_defects_middle', 'l3_7_vulnerability_management', 'l3_8_client_side_sca', 'l3_9_sast_clientside_components', 'l3_10_sast_serverside_components'],
    'LEVEL4': ['l4_1_gitignore', 'l4_2_advanced_defect_visualization', 'l4_3_reproducible_defects', 'l4_4_sast_self_components', 'l4_5_multiple_analyzers', 'l4_6_correlate_cve_images', 'l4_7_test_known_cves', 'l4_8_test_infra_known_cves'],
    'LEVEL5': ['l5_1_artifact_sigining', 'l5_2_treatment_of_defects_all', 'l5_3_sast_all']
}

AVAILABLE_CHECKS = [check for level in CHECK_LEVELS.values() for check in level]

def load_check(check_name):
    module = importlib.import_module(f'checks.{check_name}')
    return getattr(module, f'check_{check_name}')

def check_repo_security_features(repo, selected_checks):
    results = {}
    for check in selected_checks:
        check_function = load_check(check)
        results[check] = check_function(repo)
    return results

def print_check_menu():
    print("Available checks:")
    check_number = 1
    for level, checks in CHECK_LEVELS.items():
        print(f"\n{level}:")
        for check in checks:
            print(f"  {check_number}. {check}")
            check_number += 1

def get_selected_checks(user_input):
    selected_checks = []
    
    if user_input.strip().upper() == "ALL":
        return AVAILABLE_CHECKS  # Return all checks if "ALL" is selected

    for item in user_input.split(','):
        item = item.strip().upper()
        if item in CHECK_LEVELS:
            selected_checks.extend(CHECK_LEVELS[item])
        elif item.isdigit():
            index = int(item) - 1
            if 0 <= index < len(AVAILABLE_CHECKS):
                selected_checks.append(AVAILABLE_CHECKS[index])
    
    return list(set(selected_checks))  # Remove duplicates

def get_check_level(check):
    for level, checks in CHECK_LEVELS.items():
        if check in checks:
            return level
    return "Unknown"

def output_results(all_results, repos, selected_checks, output_format):
    headers = ["Security Feature"] + repos
    table_data = []
    level_stats = {level: {'total': 0, 'successful': 0} for level in CHECK_LEVELS}

    for feature in selected_checks:
        level = get_check_level(feature)
        row = [feature]
        for repo in repos:
            result = all_results[repo.strip()][feature]
            row.append(result)
            level_stats[level]['total'] += 1
            if result.lower() not in ['not detected', 'no', 'not available', 'not enabled', 'unable to check', 'error parsing data', 'error exception', 'error']:
                level_stats[level]['successful'] += 1
        table_data.append(row)

    if output_format.lower() == 'csv':
        csv_filename = 'dsomm.csv'
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(table_data)
        print(f"Results have been saved to {csv_filename}")
    else:  # Default to tabular format
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    print("\nScore for the checks in selected Level(s):")
    for level, stats in level_stats.items():
        if stats['total'] > 0:
            print(f"{level}: {stats['successful']}/{stats['total']} checks successful")

def main():
    print_check_menu()
    
    user_input = input("\nEnter the levels (Level1, Level2 etc.,) or specific check numbers or type 'ALL' to run all checks: ")
    selected_checks = get_selected_checks(user_input)
    
    if not selected_checks:
        print("No valid checks selected. Exiting.")
        return

    repos = input("Enter the repositories to check (comma-separated, format: github-org/repo): ").split(',')
    
    output_format = input("Enter output format (tabular/csv, default is tabular): ").strip() or 'tabular'
    
    all_results = {}
    for repo in repos:
        all_results[repo.strip()] = check_repo_security_features(repo.strip(), selected_checks)

    output_results(all_results, repos, selected_checks, output_format)

if __name__ == "__main__":
    main()

