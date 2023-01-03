

class Aclresource:

    @classmethod
    def parse(cls, exportLine: str) -> dict:
        data = {}
        col = exportLine.split(';')
        obj = col[0]
        action = col[1]
        if obj.upper() != 'ACLRESOURCE':
            return data
        data['object'] = 'ACLRESOURCE'
        if action == 'ADD':
            data['name'] = col[2]
            data['alias'] = col[3]
        elif action == 'SETPARAM':
            data['name'] = col[2]
            data[col[3]] = col[4]

        return data

    @classmethod
    def construct(cls, data: dict) -> 'Aclresource':
        if 'object' not in data or data['object'].upper() != 'ACLRESOURCE':
            return None
        if 'name' not in data or 'alias' not in data:
            return None
        centreonObject = Aclresource(data['name'], data['alias'])
        if 'comment' in data:
            centreonObject.setComment(data['comment'])
        if 'activate' in data and ((isinstance(data['activate'], str) and data['activate'] == '0') or (isinstance(data['activate'], bool) and not data['activate'])):
            centreonObject.disable()

        return centreonObject

    def __init__(self, name: str, alias: str):
        self._centreonObject = 'ACLRESOURCE'
        self._name = name
        self._alias = alias
        self._activate = True
        self._comment = None

    def generate(self, currentConfig: "Aclresource" = None) -> None:
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

    def setAlias(self, alias: str):
        self._alias = alias

    def enable(self):
        self._activate = True

    def disable(self):
        self._activate = False

    def setComment(self, comment: str):
        self._comment = comment
