"""Update the rule provider files defined in the 'config.yaml' file.

It downloads the files from the URLs given in the config, saves them to disk, and then generates a 
new rules file by concatenating the downloaded files with the existing rules file.
"""
from pathlib import Path

import requests
import yaml

# Load the Clash configuration file
config_file_path = Path("config.yaml")

with config_file_path.open() as f:
    config = yaml.safe_load(f)

# Check if `rule_provider` directory exists
rule_provider_dir = Path.cwd().joinpath("rule_provider")
if not rule_provider_dir.exists():
    rule_provider_dir.mkdir()

# Loop through each rule provider
for provider in config["rule-providers"]:
    # Get the URL and path for this provider
    url = config["rule-providers"][provider]["url"]
    path = rule_provider_dir.joinpath(Path(config["rule-providers"][provider]["path"]).name)

    # Download the rule provider file
    if path.suffix in (".txt", ".yaml"):
        print(f"Downloading {url} to {path}")
        r = requests.get(url, timeout=5)
        with path.open(mode="w") as f:
            f.write(r.text)
    else:
        print(f"Skipping {provider}")
