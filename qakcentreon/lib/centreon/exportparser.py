
import logging
import json

from .Aclmenu import Aclmenu
from .Aclaction import Aclaction
from .Aclgroup import Aclgroup
from .Aclresource import Aclresource
from .Command import Command


def parse_export(exportData: str) -> dict:
    data = {}
    for exportLine in exportData.split('\n'):
        parsedData = None

        if exportLine.startswith('ACLMENU;'):
            parsedData = Aclmenu.parse(exportLine)
        if exportLine.startswith('ACLACTION;'):
            parsedData = Aclaction.parse(exportLine)
        if exportLine.startswith('ACLGROUP;'):
            parsedData = Aclgroup.parse(exportLine)
        if exportLine.startswith('ACLRESOURCE;'):
            parsedData = Aclgroup.parse(exportLine)
        if exportLine.startswith('CMD;'):
            parsedData = Command.parse(exportLine)

        if parsedData is None:
            continue
        if 'object' in parsedData and parsedData['object'] not in data:
            data[parsedData['object']] = {}
        if 'name' in parsedData and not parsedData['name'] in data[parsedData['object']]:
            data[parsedData['object']][parsedData['name']] = {}
        for key, value in parsedData.items():
            if isinstance(value, str):
                data[parsedData['object']][parsedData['name']][key] = value
            if isinstance(value, list):
                if key not in data[parsedData['object']][parsedData['name']]:
                    data[parsedData['object']][parsedData['name']][key] = []
                data[parsedData['object']][parsedData['name']][key] += value

    logging.debug(json.dumps(data, indent=2))

    for centreonTypeObject, centreonObjects in data.items():
        for centreonObjectName, centreonObjectValues in centreonObjects.items():
            if centreonTypeObject == 'ACLMENU':
                data[centreonTypeObject][centreonObjectName] = Aclmenu.construct(centreonObjectValues)
            if centreonTypeObject == 'ACLACTION':
                data[centreonTypeObject][centreonObjectName] = Aclaction.construct(centreonObjectValues)
            if centreonTypeObject == 'ACLGROUP':
                data[centreonTypeObject][centreonObjectName] = Aclgroup.construct(centreonObjectValues)
            if centreonTypeObject == 'ACLRESOURCE':
                data[centreonTypeObject][centreonObjectName] = Aclresource.construct(centreonObjectValues)
            if centreonTypeObject == 'CMD':
                data[centreonTypeObject][centreonObjectName] = Command.construct(centreonObjectValues)

    return data
