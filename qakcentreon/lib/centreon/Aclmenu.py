

class Aclmenu:

    @classmethod
    def parse(cls, exportLine: str) -> dict:
        data = {}
        col = exportLine.split(';')
        obj = col[0]
        action = col[1]
        if obj.upper() != 'ACLMENU':
            return data
        data['object'] = 'ACLMENU'
        if action == 'ADD':
            data['name'] = col[2]
            data['alias'] = col[3]
        elif action == 'SETPARAM':
            data['name'] = col[2]
            data[col[3]] = col[4]
        elif action == 'GRANTRO':
            data['name'] = col[2]
            data['grantro'] = [';'.join(col[4:]).strip(';')]
        elif action == 'GRANTRW':
            data['name'] = col[2]
            data['grantrw'] = [';'.join(col[4:]).strip(';')]
        elif action == 'REVOKE':
            data['name'] = col[2]
            data['revoke'] = [';'.join(col[4:]).strip(';')]

        return data

    @classmethod
    def construct(cls, data: dict) -> 'Aclmenu':
        if 'object' not in data or data['object'].upper() != 'ACLMENU':
            return None
        if 'name' not in data or 'alias' not in data:
            return None
        centreonObject = Aclmenu(data['name'], data['alias'])
        if 'comment' in data:
            centreonObject.setComment(data['comment'])
        if 'activate' in data and ((isinstance(data['activate'], str) and data['activate'] == '0') or (isinstance(data['activate'], bool) and not data['activate'])):
            centreonObject.disable()
        if 'grantrw' in data:
            centreonObject.setGrantRw(data['grantrw'])
        if 'grantro' in data:
            centreonObject.setGrantRo(data['grantro'])
        if 'revoke' in data:
            centreonObject.setRevoke(data['revoke'])

        return centreonObject

    def __init__(self, name: str, alias: str):
        self._centreonObject = 'ACLMENU'
        self._name = name
        self._alias = alias
        self._activate = True
        self._comment = None
        self._grantrw = []
        self._grantro = []
        self._revoke = []

    def generate(self, currentConfig: "Aclmenu" = None) -> None:
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
            if self._comment is not None and self._comment != '':
                print(f'{self._centreonObject};SETPARAM;{self._name};comment;{self._comment}')
        else:
            # Non-destructive method
            if self._comment is not None and self._comment != '' and currentConfig._comment is not None and self._comment != currentConfig._comment:
                print(f'{self._centreonObject};SETPARAM;{self._name};comment;{self._comment}')

        if not diffMode:
            for grantMenu in self._grantrw:
                print(f'{self._centreonObject};GRANTRW;{self._name};0;{grantMenu}')
        else:
            for grantMenu in self._grantrw:
                if currentConfig._grantrw is not None and grantMenu not in currentConfig._grantrw:
                    print(f'{self._centreonObject};GRANTRW;{self._name};0;{grantMenu}')

        if not diffMode:
            for grantMenu in self._grantro:
                print(f'{self._centreonObject};GRANTRO;{self._name};0;{grantMenu}')
        else:
            for grantMenu in self._grantro:
                if currentConfig._grantro is not None and grantMenu not in currentConfig._grantro:
                    print(f'{self._centreonObject};GRANTRO;{self._name};0;{grantMenu}')

        if not diffMode:
            for grantMenu in self._revoke:
                print(f'{self._centreonObject};REVOKE;{self._name};0;{grantMenu}')
        else:
            for grantMenu in self._revoke:
                if currentConfig._revoke is not None and grantMenu not in currentConfig._revoke:
                    print(f'{self._centreonObject};REVOKE;{self._name};0;{grantMenu}')

    def setAlias(self, alias: str):
        self._alias = alias

    def enable(self):
        self._activate = True

    def disable(self):
        self._activate = False

    def setComment(self, comment: str):
        self._comment = comment

    def setGrantRw(self, menu):
        if isinstance(menu, str):
            menu = [menu]
        if isinstance(menu, list):
            for menuValue in menu:
                if menuValue not in self._grantrw:
                    self._grantrw.append(menuValue)
                if menuValue in self._grantro:
                    self._grantro.remove(menuValue)
                elif menuValue in self._revoke:
                    self._revoke.remove(menuValue)

    def setGrantRo(self, menu):
        if isinstance(menu, str):
            menu = [menu]
        if isinstance(menu, list):
            for menuValue in menu:
                if menuValue not in self._grantro:
                    self._grantro.append(menuValue)
                if menuValue in self._grantrw:
                    self._grantrw.remove(menuValue)
                elif menuValue in self._revoke:
                    self._revoke.remove(menuValue)

    def setRevoke(self, menu):
        if isinstance(menu, str):
            menu = [menu]
        if isinstance(menu, list):
            for menuValue in menu:
                if menuValue not in self._revoke:
                    self._revoke.append(menuValue)
                if menuValue in self._grantrw:
                    self._grantrw.remove(menuValue)
                elif menuValue in self._grantro:
                    self._grantro.remove(menuValue)
