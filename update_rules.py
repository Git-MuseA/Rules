import requests
import yaml
from yaml.loader import SafeLoader

config_dict = yaml.load(open("myconfig.yaml", "r"), Loader=SafeLoader)

rule_providers_dict = config_dict["rule-providers"]
rule_urls = [rule_providers_dict[k]["url"] for k in rule_providers_dict]
rule_local_paths = [rule_providers_dict[k]["path"] for k in rule_providers_dict]

for url, path in dict(zip(rule_urls, rule_local_paths)).items():
    with open(path, "wb") as f:
        content = requests.get(url, stream=True).content
        f.write(content)
