import subprocess

packages = [
    "pymox-kit==1.0.3",
    "pytz",
    "mkdocs",
    "mkdocs-material",
    "pyodide-mkdocs-theme",
    "mkdocs-awesome-pages-plugin",
    "mkdocs-open-in-new-tab",
    "python-semantic-release",
    "ruamel.yaml",
    "git-revision-date-localized",
    "build"
]

# Upgrade pip
subprocess.run(["pip", "install", "--upgrade", "pip"], check=True)

# Install packages
subprocess.run(["pip", "install"] + packages, check=True)
