import configparser
import pathlib
import getpass

def get_parameters() -> dict:
    """This funciton gets parameters from user

    Returns:
        list: a list of all parameters that are required for config
    """
    github_params = {}
    github_params["github_token"] = getpass.getpass("GitHub access token: ")
    github_params["repo_name"] = str(input("Please enter your repo name: "))
    github_params["repo_owner"] = str(input("Please enter your repo owner: "))
    github_params["action_name"] = str(input("Please enter the name of the action you would like to use: "))
    secrets = {}
    secrets["harbor_username"] = str(input("Please enter your harbor username: "))
    secrets["harbor_token"] = getpass.getpass("Harbor access token: ")
    return github_params, secrets

def write_to_config(config : configparser.ConfigParser , github_params : "dict[str:str]", secrets_params: "dict[str:str]") -> None:
    """This functions creates a config file from parameters supplied

    Args:
        config (configparser.ConfigParser): The config tempalte that is used to create config
        values_to_write (list[str]): the values to populate config with
    """
    new_path = pathlib.Path.cwd() / "config" / "config.ini"
    if github_params is not None:
        config.add_section("github")
        for key, item in github_params.items():
            config.set("github",key,item)
    if secrets_params is not None:
        config.add_section("secrets")
        for key, item in secrets_params.items():
            config.set("secrets",key,item)
    with open(new_path,"w") as f:
        config.write(f)

def main() -> None:
    """Main function
    """
    config = configparser.ConfigParser()
    github_params,secrets_params = get_parameters()
    write_to_config(config,github_params,secrets_params)


if __name__ == "__main__":
    main()
