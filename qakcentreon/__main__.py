#!/usr/bin/env python3

import os
import sys
import argparse
import logging
import glob
import json
import yaml

import lib.common.log
from lib.centreon.exportparser import parse_export
from lib.centreon.Aclmenu import Aclmenu
from lib.centreon.Aclaction import Aclaction

DEFAULT_CENTREON_CONFIG_DIRECTORY = 'conf/centreon'
DEFAULT_TARGET = 'centreon_generated.conf'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='centreon-configurator',
        description='Generate and apply configuration to a Centreon server')
    parser.add_argument('-c', '--config',
                        type=str,
                        default=DEFAULT_CENTREON_CONFIG_DIRECTORY)
    parser.add_argument('-i', '--input',
                        action='store_true',
                        help='Input read to enable diff mode.')
    parser.add_argument('-d', '--debug',
                        action='store_true')
    args = parser.parse_args()

    # initialise logging configuration
    lib.common.log.setup(args.debug)
    logging.debug(f'Values of parser : {args}')

    currentConfiguration = None

    # Mode diff enabled if export is provided in stdin
    if args.input:
        logging.info('Diff mode enabled. Start to read stdin.')
        currentConfiguration = parse_export(sys.stdin.read())
        logging.info('Reading completed.')

    # parse all centreon configuration yml files
    logging.info('Start to compile all centreon .yml configuration files.')
    configuration = []
    if os.path.isdir(args.config):
        searchFilter = f"{args.config}/**/*yml"
        logging.debug("Glob search: {0}".format(searchFilter))
        for filePath in glob.iglob(searchFilter, recursive=True):
            with open(filePath, 'rt') as configFile:
                try:
                    configuration += yaml.safe_load(configFile.read())
                except yaml.YAMLError:
                    logging.exception(
                        f'An error occure when reading the following file {filePath}. Is it in the right format?')
    elif os.path.isfile(args.config):
        filePath = args.config
        with open(filePath, 'rt') as configFile:
            try:
                configuration += yaml.safe_load(configFile.read())
            except yaml.YAMLError:
                logging.exception(
                    f'An error occure when reading the following file {filePath}. Is it in the right format?')
    logging.info('Configuration compilation complete.')

    logging.info('Start to generate configuration.')
    for centreonObject in configuration:
        logging.debug(json.dumps(centreonObject, indent=2))
        currentCentreonObject = None
        if args.input:
            if 'object' in centreonObject and centreonObject['object'].upper() in currentConfiguration and centreonObject['name'] in currentConfiguration[centreonObject['object'].upper()]:
                currentCentreonObject = currentConfiguration[centreonObject['object'].upper()][centreonObject['name']]
        if 'object' in centreonObject and centreonObject['object'].upper() == 'ACLMENU':
            Aclmenu.construct(centreonObject).generate(currentCentreonObject)
        if 'object' in centreonObject and centreonObject['object'].upper() == 'ACLACTION':
            Aclaction.construct(centreonObject).generate(currentCentreonObject)
    logging.info('Configuration generation is completed.')

    sys.exit(0)
