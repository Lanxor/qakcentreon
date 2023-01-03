# Qak Centreon

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Configuration as Code utility for Centreon operator.

**Goals**:

- Configuration change management via git.
- Ensure the consistency of the Centreon configuration.
- Simplifies the configuration of a new Centreon stack.
- Standalone and lightweight.

## Installation

```sh
python -m pip install virtenv
python -m virtenv env
source env/bin/activate # or env/Scripts/activate from windows (via git bash with visualstudio)
python -m pip install -r requirements.txt
```

## Usage

### 1. Create yaml centreon configuration

Example :

- Create the file my_acl_menu.yml with the following content :

```yml
- object: aclmenu
  name: ACL menu number 1
  alias: An ACL menu
  activate: True
  comment: My first ACL Menu with qake centreon
  grantrw:
    - Home
```

### 2.1 Simple generation file

```sh
python qake -c my_acl_menu.yml
# or into a file
python qake -c my_acl_menu.yml > centreon_config.txt
```

### 2.2 Simple generation and centreon import process

```sh
python qake -c my_acl_menu.yml > centreon_config.txt && centreon -u admin -p mypassword -i centreon_config.txt
```

### 2.3 Diff generation and centreon import process

```sh
centreon -u admin -p mypassword -e | python qake -c my_acl_menu.yml > centreon_config.txt && centreon -u admin -p mypassword -i centreon_config.txt
```

## Contribution

Any help is welcome. For advice or to participate in the code. The [docs/development](docs/development) section summarizes the development information of this project. It is intended to evolve as improvements are made.

## Roadmap

Much work remains to be done.

But here are the next steps:

- Add Github Action for a continuous integration.
- Use Github Roadmap feature to better communicate about the project.
- Developping Centreon ACL resources configuration (and these unit tests).
- Developping Centreon ACL groups configuration (and these unit tests).

Here are the other topics that will be covered (this list may be expanded).

- Developping Centreon commands configuration (and these unit tests).
- Developping Centreon contact groups configuration (and these unit tests).
- Developping Centreon contact templates configuration (and these unit tests).
- Developping Centreon host categories configuration (and these unit tests).
- Developping Centreon host groups configuration (and these unit tests).
- Developping Centreon host templates configuration (and these unit tests).
- Developping Centreon service categories configuration (and these unit tests).
- Developping Centreon service groups configuration (and these unit tests).
- Developping Centreon service templates configuration (and these unit tests).
- Developping Centreon time periods configuration (and these unit tests).
