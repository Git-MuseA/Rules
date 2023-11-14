from pathlib import Path

import requests
import yaml
from tqdm import tqdm

HTTP_SUCCESS = 200


def download_file(url: str, path: Path) -> bool:
    """
    Download a file from a URL and save it to a specified path.

    Parameters
    ----------
    url : str
        The URL to download the file from.
    path : Path
        The Path object representing where to save the file.

    Returns
    -------
    bool
        True if the file was downloaded successfully, False otherwise.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == HTTP_SUCCESS:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("wb") as file:
                file.write(response.content)
            return True
    except requests.RequestException:
        return False


yaml_file = Path("config.yaml")
with yaml_file.open("r") as file:
    data = yaml.safe_load(file)

for _key, value in tqdm(data["rule-providers"].items(), desc="Downloading files"):
    file_path = Path(value["path"])
    if not download_file(value["url"], file_path):
        print(f"{value['url']} failed downloading.")

print("\nDownload completed.")
