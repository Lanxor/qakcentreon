

class Aclaction:

    @classmethod
    def parse(cls, exportLine: str) -> dict:
        data = {}
        col = exportLine.split(';')
        obj = col[0]
        action = col[1]
        if obj.upper() != 'ACLACTION':
            return data
        data['object'] = 'ACLACTION'
        if action == 'ADD':
            data['name'] = col[2]
            data['description'] = col[3]
        elif action == 'SETPARAM':
            data['name'] = col[2]
            data[col[3]] = col[4]
        elif action == 'GRANT':
            data['name'] = col[2]
            data['grant'] = col[3].split('|')
        elif action == 'REVOKE':
            data['name'] = col[2]
            data['revoke'] = col[3].split('|')

        return data

    @classmethod
    def construct(cls, data: dict) -> 'Aclaction':
        if 'object' not in data or data['object'].upper() != 'ACLACTION':
            return None
        if 'name' not in data or 'description' not in data:
            return None
        centreonObject = Aclaction(data['name'], data['description'])
        if 'activate' in data and ((isinstance(data['activate'], str) and data['activate'] == '0') or (isinstance(data['activate'], bool) and not data['activate'])):
            centreonObject.disable()
        if 'grant' in data:
            centreonObject.setGrant(data['grant'])
        if 'revoke' in data:
            centreonObject.setRevoke(data['revoke'])

        return centreonObject

    def __init__(self, name: str, description: str):
        self._centreonObject = 'ACLACTION'
        self._name = name
        self._description = description
        self._activate = True
        self._grant = []
        self._revoke = []

    def generate(self, currentConfig: "Aclaction" = None) -> None:
        diffMode = currentConfig is not None

        if not diffMode:
            print(f'{self._centreonObject};ADD;{self._name};{self._description}')

        # All new object created on centreon define the description parameter, if diff mode is disabled it's not necessary to set description parameter
        if diffMode and self._description != currentConfig._description:
            print(f'{self._centreonObject};SETPARAM;{self._name};description;{self._description}')

        # All new object created on centreon are enabled by default, if diff mode is disabled it's not necessary to set activate parameter
        if not diffMode and not self._activate:
            activateValue = '1' if self._activate else '0'
            print(f'{self._centreonObject};SETPARAM;{self._name};activate;{activateValue}')
        elif diffMode and self._activate != currentConfig._activate:
            activateValue = '1' if self._activate else '0'
            print(f'{self._centreonObject};SETPARAM;{self._name};activate;{activateValue}')

        if not diffMode:
            if self._grant != []:
                grantActions = '|'.join(self._grant)
                print(f'{self._centreonObject};GRANT;{self._name};{grantActions}')
        else:
            if self._grant != [] and currentConfig._grant is not None and set(self._grant) != set(currentConfig._grant):
                grantActions = '|'.join(self._grant)
                print(f'{self._centreonObject};GRANT;{self._name};{grantActions}')

        if not diffMode:
            if self._revoke != []:
                revokeActions = '|'.join(self._revoke)
                print(f'{self._centreonObject};REVOKE;{self._name};{revokeActions}')
        else:
            if self._revoke != [] and currentConfig._revoke is not None and set(self._revoke) != set(currentConfig._revoke):
                revokeActions = '|'.join(self._revoke)
                print(f'{self._centreonObject};REVOKE;{self._name};{revokeActions}')

    def setDescription(self, description: str):
        self._description = description

    def enable(self):
        self._activate = True

    def disable(self):
        self._activate = False

    def setGrant(self, action):
        if isinstance(action, str):
            action = [action]
        if isinstance(action, list):
            for actionValue in action:
                if actionValue not in self._grant:
                    self._grant.append(actionValue)
                if actionValue in self._revoke:
                    self._revoke.remove(actionValue)

    def setRevoke(self, action):
        if isinstance(action, str):
            action = [action]
        if isinstance(action, list):
            for actionValue in action:
                if actionValue not in self._revoke:
                    self._revoke.append(actionValue)
                if actionValue in self._grant:
                    self._grant.remove(actionValue)
