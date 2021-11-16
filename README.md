# Installation
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