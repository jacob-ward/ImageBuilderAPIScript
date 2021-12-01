import configparser
import pathlib

def main() -> None:
    config = configparser.ConfigParser()
    path = pathlib.Path.cwd() / "config" / "config_template.ini"
    new_path = pathlib.Path.cwd() / "config" / "config.ini"
    config.read(path)
    aciton_name = "test2"
    config.set("github","action_name", aciton_name)
    with open(new_path,"w") as f:
        config.write(f)

if __name__ == "__main__":
    main()