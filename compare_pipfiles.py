import json
import sys
import requests
from itertools import zip_longest

def fetch_file_content(filepath_or_url):
    if filepath_or_url.startswith('http'):
        # Assume it's a GitHub URL and convert/fetch it
        content = fetch_file_from_github(filepath_or_url)
    else:
        # Assume it's a local file path
        with open(filepath_or_url, 'r') as file:
            content = file.read()
    return json.loads(content)

def fetch_file_from_github(repo_url):
    # Convert GitHub repo URL to raw content URL - this is simplified and may need adjustment
    raw_url = repo_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob', '')
    response = requests.get(raw_url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch file: {response.status_code}")

def extract_packages(data):
    packages = {pkg_name: details.get('version', 'No version info') for pkg_name, details in data.get('default', {}).items()}
    return packages

def compare_environments(data1, data2, label1, label2):
    packages1 = extract_packages(data1)
    packages2 = extract_packages(data2)

    common_packages = set(packages1.keys()) & set(packages2.keys()) - {pkg for pkg in packages1 if packages1[pkg] != packages2[pkg]}
    
    diffs = {
        f'unique_to_{label1}': set(packages1.keys()) - set(packages2.keys()),
        f'unique_to_{label2}': set(packages2.keys()) - set(packages1.keys()),
    }
    
    version_diffs = {}
    for pkg in set(packages1.keys()) & set(packages2.keys()):
        if packages1[pkg] != packages2[pkg]:
            version_diffs[pkg] = {label1: packages1[pkg], label2: packages2[pkg]}
    
    return common_packages, diffs, version_diffs

def print_side_by_side(common_packages, diffs, version_diffs, label1, label2):

    print(f"\nCommon Packages to {label1} and {label2}:")
    for pkg in common_packages:
        print(f"{pkg:<30}")


    print(f"\nUnique Packages to {label1} and {label2}:")
    print(f"{'Unique to ' + label1:<30} | {'Unique to ' + label2:<30}")
    print("-" * 61)
    for env1_pkg, env2_pkg in zip_longest(sorted(diffs[f'unique_to_{label1}']), sorted(diffs[f'unique_to_{label2}']), fillvalue=''):
        print(f"{env1_pkg:<30} | {env2_pkg:<30}")

    print("\nVersion Differences:")
    print(f"{'Package':<20} | {label1:<15} | {label2:<15}")
    print("-" * 53)
    for pkg, versions in version_diffs.items():
        print(f"{pkg:<20} | {versions[label1]:<15} | {versions[label2]:<15}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_or_url_to_first_pipfile.lock> <path_or_url_to_second_pipfile.lock>")
        sys.exit(1)
    
    input1, input2 = sys.argv[1], sys.argv[2]
    label1 = input1.split('/')[-1].split('.')[0]  # Simplifies input to a label
    label2 = input2.split('/')[-1].split('.')[0]  # Simplifies input to a label

    data1 = fetch_file_content(input1)
    data2 = fetch_file_content(input2)
    common_packages, diffs, version_diffs = compare_environments(data1, data2, label1, label2)
    print_side_by_side(common_packages, diffs, version_diffs, label1, label2)
