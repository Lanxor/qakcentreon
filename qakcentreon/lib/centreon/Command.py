

class Command:

    @classmethod
    def parse(cls, exportLine: str) -> dict:
        data = {}
        col = exportLine.split(';')
        obj = col[0]
        action = col[1]
        if obj.upper() != 'CMD':
            return data
        data['object'] = 'CMD'
        if action == 'ADD':
            data['name'] = col[2]
            data['type'] = col[3]
            data['line'] = col[4]
        elif action == 'SETPARAM':
            data['name'] = col[2]
            data[col[3]] = col[4]

        return data

    @classmethod
    def construct(cls, data: dict) -> 'Command':
        if 'object' not in data or data['object'].upper() != 'CMD':
            return None
        if 'name' not in data or 'type' not in data or 'line' not in data:
            return None
        centreonObject = Command(data['name'], data['type'], data['line'])
        if 'example' in data:
            centreonObject.setComment(data['example'])
        if 'comment' in data:
            centreonObject.setComment(data['comment'])
        if 'activate' in data and ((isinstance(data['activate'], str) and data['activate'] == '0') or (isinstance(data['activate'], bool) and not data['activate'])):
            centreonObject.disable()
        if 'enable_shell' in data and ((isinstance(data['enable_shell'], str) and data['enable_shell'] == '1') or (isinstance(data['enable_shell'], bool) and data['enable_shell'])):
            centreonObject.enableShell()

        return centreonObject

    def __init__(self, name: str, type: str, line: str):
        self._centreonObject = 'CMD'
        self._name = name
        self._type = type
        self._line = line
        self._example = None
        self._comment = None
        self._activate = True
        self._enableShell = False

    def generate(self, currentConfig: "Command" = None) -> None:
        diffMode = currentConfig is not None

        if not diffMode:
            print(f'{self._centreonObject};ADD;{self._name};{self._type};{self._line}')

        # All new object created on centreon define the alias parameter, if diff mode is disabled it's not necessary to set alias parameter
        if diffMode and self._type != currentConfig._type:
            print(f'{self._centreonObject};SETPARAM;{self._name};type;{self._type}')

        # All new object created on centreon define the alias parameter, if diff mode is disabled it's not necessary to set alias parameter
        if diffMode and self._line != currentConfig._line:
            print(f'{self._centreonObject};SETPARAM;{self._name};line;{self._line}')

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

    def setType(self, type: str):
        self._type = type

    def setLine(self, line: str):
        self._line = line

    def enable(self):
        self._activate = True

    def disable(self):
        self._activate = False

    def enableShell(self):
        self._enableShell = True

    def disableShell(self):
        self._enableShell = False

    def setComment(self, comment: str):
        self._comment = comment

    def setExample(self, example: str):
        self._example = example
