"""Main function call
"""

import argparse
from pathlib import Path, PosixPath, WindowsPath
from . import deploy_script, gitlab_test

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("remote", choices=['gitlab','github'], help="Deploy it to Gitlab or Github")
    parser.add_argument("config", help="path to config", type=Path)
    args = parser.parse_args()
    if args.config is not None:
        config_path = args.config  # type: Path
    if args.remote =="gitlab":
        gitlab_test.main(config_path)
    elif args.remote =="github":
        deploy_script.main(config_path)
