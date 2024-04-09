# Pipfile Comparison Tool

This Python script is designed to compare two `pipfile.lock` files, identifying common packages, unique packages, and version differences between them. It can handle both local files and `pipfile.lock` files hosted on public GitHub repositories. (as yet to be tested)

## Requirements

- Python 3.x
- Requests library for Python (for fetching files from GitHub URLs)

Before running the script, ensure you have the `requests` library installed:

```bash
pip install requests
```

## Usage

The script accepts two positional arguments, which can be either paths to local `pipfile.lock` files or URLs to `pipfile.lock` files in public GitHub repositories.

### Comparing Local Files

To compare two local `pipfile.lock` files, use the following command format:

```bash
python compare_pipfiles.py path/to/first/pipfile.lock path/to/second/pipfile.lock
```

For example, using the demonstration files in the root directory:

```bash
python compare_pipfiles.py streamlit-pipfile.lock streamlit-analytics2-pipfile.lock
```

### Comparing Files from GitHub Repositories

To compare files directly from GitHub, provide the URLs to the raw `pipfile.lock` content:

```bash
python compare_pipfiles.py <URL_to_first_pipfile.lock> <URL_to_second_pipfile.lock>
```

Ensure you use the URL to the raw version of the file on GitHub.

### Output

The script outputs the comparison results in three sections:

1. **Common Packages**: Lists packages found in both `pipfile.lock` files.
2. **Unique Packages**: Lists packages unique to each `pipfile.lock` file, side by side.
3. **Version Differences**: Lists packages that are present in both files but with different versions, showing the version in each file side by side.

## Example

After running the script with the provided example files, you might see output similar to the following:

```
Common Packages:
package1
package2

Unique Packages to streamlit-pipfile and streamlit-analytics2-pipfile:
Unique to streamlit-pipfile    | Unique to streamlit-analytics2-pipfile
-------------------------------------------------------------
                               | google-api-core
                               | google-auth
                               ...

Version Differences:
Package              | streamlit-pipfile | streamlit-analytics2-pipfile
-----------------------------------------------------
packaging            | ==24.0          | ==23.2
streamlit            | ==1.33.0        | ==1.32.2
...
```

This structured output makes it easy to quickly identify differences and commonalities between the two `pipfile.lock` environments.