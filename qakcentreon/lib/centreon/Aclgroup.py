

class Aclgroup:

    @classmethod
    def parse(cls, exportLine: str) -> dict:
        data = {}
        col = exportLine.split(';')
        obj = col[0]
        action = col[1]
        if obj.upper() != 'ACLGROUP':
            return data
        data['object'] = 'ACLGROUP'
        if action == 'ADD':
            data['name'] = col[2]
            data['alias'] = col[3]
        elif action == 'SETPARAM':
            data['name'] = col[2]
            data[col[3]] = col[4]
        elif action == 'SETCONTACT':
            data['name'] = col[2]
            data['contact'] = col[3].split('|')
        elif action == 'SETCONTACTGROUP':
            data['name'] = col[2]
            data['contactgroup'] = col[3].split('|')
        elif action == 'SETMENU':
            data['name'] = col[2]
            data['menu'] = col[3].split('|')
        elif action == 'SETACTION':
            data['name'] = col[2]
            data['action'] = col[3].split('|')
        elif action == 'SETRESOURCE':
            data['name'] = col[2]
            data['resource'] = col[3].split('|')

        return data

    @classmethod
    def construct(cls, data: dict) -> 'Aclgroup':
        if 'object' not in data or data['object'].upper() != 'ACLGROUP':
            return None
        if 'name' not in data or 'alias' not in data:
            return None
        centreonObject = Aclgroup(data['name'], data['alias'])
        if 'activate' in data and ((isinstance(data['activate'], str) and data['activate'] == '0') or (isinstance(data['activate'], bool) and not data['activate'])):
            centreonObject.disable()

        return centreonObject

    def __init__(self, name: str, alias: str):
        self._centreonObject = 'ACLGROUP'
        self._name = name
        self._alias = alias
        self._activate = True
        self._contact = []
        self._contactGroup = []
        self._menu = []
        self._action = []
        self._resource = []

    def generate(self, currentConfig: "Aclgroup" = None) -> None:
        diffMode = currentConfig is not None

        if not diffMode:
            print(f'{self._centreonObject};ADD;{self._name};{self._alias}')

        # All new object created on centreon define the alias parameter, if diff mode is disabled it's not necessary to set alias parameter
        if diffMode and self._alias != currentConfig._alias:
            print(f'{self._centreonObject};SETPARAM;{self._name};alias;{self._alias}')

        # All new object created on centreon are enabled by default, if diff mode is disabled it's not necessary to set activate parameter
        if not diffMode and not self._activate:
            activateValue = '1' if self._activate else '0'
            print(f'{self._centreonObject};SETPARAM;{self._name};activate;{activateValue}')
        elif diffMode and self._activate != currentConfig._activate:
            activateValue = '1' if self._activate else '0'
            print(f'{self._centreonObject};SETPARAM;{self._name};activate;{activateValue}')

        if not diffMode:
            if self._contact != []:
                contactValues = '|'.join(self._contact)
                print(f'{self._centreonObject};SETCONTACT;{self._name};{contactValues}')
        else:
            if self._contact != [] and currentConfig._contact is not None and set(self._contact) != set(currentConfig._contact):
                contactValues = '|'.join(self._contact)
                print(f'{self._centreonObject};SETCONTACT;{self._name};{contactValues}')

        if not diffMode:
            if self._contactGroup != []:
                contactGroupValues = '|'.join(self._contactGroup)
                print(f'{self._centreonObject};SETCONTACTGROUP;{self._name};{contactGroupValues}')
        else:
            if self._contactGroup != [] and currentConfig._contactGroup is not None and set(self._contactGroup) != set(currentConfig._contactGroup):
                contactGroupValues = '|'.join(self._contactGroup)
                print(f'{self._centreonObject};SETCONTACTGROUP;{self._name};{contactGroupValues}')

        if not diffMode:
            if self._menu != []:
                menuValues = '|'.join(self._menu)
                print(f'{self._centreonObject};SETMENU;{self._name};{menuValues}')
        else:
            if self._menu != [] and currentConfig._menu is not None and set(self._menu) != set(currentConfig._menu):
                menuValues = '|'.join(self._menu)
                print(f'{self._centreonObject};SETMENU;{self._name};{menuValues}')

        if not diffMode:
            if self._action != []:
                actionValues = '|'.join(self._action)
                print(f'{self._centreonObject};SETACTION;{self._name};{actionValues}')
        else:
            if self._action != [] and currentConfig._action is not None and set(self._action) != set(currentConfig._action):
                actionValues = '|'.join(self._action)
                print(f'{self._centreonObject};SETACTION;{self._name};{actionValues}')

        if not diffMode:
            if self._resource != []:
                resourceValues = '|'.join(self._resource)
                print(f'{self._centreonObject};SETRESOURCE;{self._name};{resourceValues}')
        else:
            if self._resource != [] and currentConfig._resource is not None and set(self._resource) != set(currentConfig._resource):
                resourceValues = '|'.join(self._resource)
                print(f'{self._centreonObject};SETRESOURCE;{self._name};{resourceValues}')

    def setAlias(self, alias: str):
        self._alias = alias

    def enable(self):
        self._activate = True

    def disable(self):
        self._activate = False

    def setContact(self, contact):
        if isinstance(contact, str):
            contact = [contact]
        if isinstance(contact, list):
            for contactValue in contact:
                if contactValue not in self._contact:
                    self._contact.append(contactValue)

    def setContactGroup(self, contactGroup):
        if isinstance(contactGroup, str):
            contactGroup = [contactGroup]
        if isinstance(contactGroup, list):
            for contactGroupValue in contactGroup:
                if contactGroupValue not in self._contactGroup:
                    self._contactGroup.append(contactGroupValue)

    def setMenu(self, menu):
        if isinstance(menu, str):
            menu = [menu]
        if isinstance(menu, list):
            for menuValue in menu:
                if menuValue not in self._menu:
                    self._menu.append(menuValue)

    def setAction(self, action):
        if isinstance(action, str):
            action = [action]
        if isinstance(action, list):
            for actionValue in action:
                if actionValue not in self._action:
                    self._action.append(actionValue)

    def setResource(self, resource):
        if isinstance(resource, str):
            resource = [resource]
        if isinstance(resource, list):
            for resourceValue in resource:
                if resourceValue not in self._resource:
                    self._resource.append(resourceValue)
