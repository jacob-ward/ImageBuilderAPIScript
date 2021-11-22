# Installation QUICK START
To install this script from source clone this repo using `git clone`. after cloning the repo make sure that all python requirements are met. Install all python packages that are needed for buildibng from source; On linux run: <br/>
`apt update` <br/>
`apt install python3-pip` <br/>
`apt install python3-venv` <br/>
`pip3 install build` <br/>
After that the script should be ready for build. To build it use `python -m build -s` from the repo root directory. After build just run `pip3 install dist/imageBuilderDeployer-<version number>.tar.gz` and it should be ready for use. 

## Supported versions
To build and rus this package you will need to use python >=3.6

## How to build
To build this python package you will need to have python build installed as a package. To do this please run `python -m pip install build`. To build ImageBuilderAPI navigate to root directory of this repo and run `python -m build`. When build finfishes new directory will appear name `dist`

## How to install
To install package globaly simply run `python -m pip install dist/imageBuilderDeployer<version>.tag.gz>`

## Configuration
Before using this script it needs a configuration file, the template for this file can be found in `config/config_template`. Simply fill in the template file and store it somewhere in your system.

## How to run this package
After installing this package run `python -m imageBuilderDeployer <path_to_your_config_file>` and it should just work.

## Troubleshooting
TODO