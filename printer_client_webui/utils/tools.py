import yaml

def read_config(dir: str="./config.yaml"):
    with open(dir) as file:
        return yaml.safe_load(file)
    