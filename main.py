import json
import sys

def extract_packages(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    packages = {pkg_name: details.get('version', 'No version info') for pkg_name, details in data.get('default', {}).items()}
    return packages

def compare_environments(file1, file2):
    packages1 = extract_packages(file1)
    packages2 = extract_packages(file2)
    
    # Summarize packages
    summary = {
        'env1': list(packages1.keys()),
        'env2': list(packages2.keys()),
    }
    
    # Find differences
    diffs = {
        'unique_to_env1': set(packages1.keys()) - set(packages2.keys()),
        'unique_to_env2': set(packages2.keys()) - set(packages1.keys()),
    }
    
    # Find version differences
    version_diffs = {}
    for pkg in set(packages1.keys()) & set(packages2.keys()):
        if packages1[pkg] != packages2[pkg]:
            version_diffs[pkg] = {'env1': packages1[pkg], 'env2': packages2[pkg]}
    
    return summary, diffs, version_diffs

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_first_pipfile.lock> <path_to_second_pipfile.lock>")
        sys.exit(1)
    
    file1_path, file2_path = sys.argv[1], sys.argv[2]
    summary, diffs, version_diffs = compare_environments(file1_path, file2_path)
    print("Summary:\n\n", summary)
    print("\nDiffs:", diffs)
    print("\nVersion differences:", version_diffs)
