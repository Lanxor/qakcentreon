
import logging
import io
import unittest
import unittest.mock

import qakcentreon.lib.centreon.Command


class TestLibCentreonCommand(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_parse_line_wrong_object(self):
        data = qakcentreon.lib.centreon.Command.Command.parse('OTHER;ADD;commandName;commandType;commandLine')
        self.assertEqual(data, {})

    def test_parse_line_add(self):
        data = qakcentreon.lib.centreon.Command.Command.parse('CMD;ADD;commandName;commandType;commandLine')
        self.assertEqual(data, {'object':'CMD','name':'commandName','type':'commandType','line':'commandLine'})

    def test_parse_line_setparam_type(self):
        data = qakcentreon.lib.centreon.Command.Command.parse('CMD;SETPARAM;commandName;type;newType')
        self.assertEqual(data, {'object':'CMD','name':'commandName','type':'newType'})

    def test_parse_line_setparam_comment(self):
        data = qakcentreon.lib.centreon.Command.Command.parse('CMD;SETPARAM;commandName;comment;newComment')
        self.assertEqual(data, {'object':'CMD','name':'commandName','comment':'newComment'})

    def test_parse_line_setparam_activate_0(self):
        data = qakcentreon.lib.centreon.Command.Command.parse('CMD;SETPARAM;commandName;activate;0')
        self.assertEqual(data, {'object':'CMD','name':'commandName','activate':'0'})

    def test_parse_line_setparam_activate_1(self):
        data = qakcentreon.lib.centreon.Command.Command.parse('CMD;SETPARAM;commandName;activate;1')
        self.assertEqual(data, {'object':'CMD','name':'commandName','activate':'1'})

    def test_construct_empty_data(self):
        data = {}
        command = qakcentreon.lib.centreon.Command.Command.construct(data)
        self.assertIsNone(command)

    def test_construct_wrong_object(self):
        data = {
            'object':'wrongObject'
        }
        command = qakcentreon.lib.centreon.Command.Command.construct(data)
        self.assertIsNone(command)

    def test_construct_missing_name(self):
        data = {
            'object':'command',
            'type':'commandType'
        }
        command = qakcentreon.lib.centreon.Command.Command.construct(data)
        self.assertIsNone(command)

    def test_construct_missing_type(self):
        data = {
            'object':'command',
            'name':'commandName'
        }
        command = qakcentreon.lib.centreon.Command.Command.construct(data)
        self.assertIsNone(command)

    def test_construct_minimum(self):
        data = {
            'object':'CMD',
            'name':'commandName',
            'type':'commandType',
            'line': 'commandLine'
        }
        command = qakcentreon.lib.centreon.Command.Command.construct(data)
        self.assertIsInstance(command, qakcentreon.lib.centreon.Command.Command)
        self.assertEqual(command._name, 'commandName')
        self.assertEqual(command._type, 'commandType')
        self.assertEqual(command._line, 'commandLine')
        self.assertEqual(command._example, None)
        self.assertEqual(command._comment, None)
        self.assertEqual(command._activate, True)
        self.assertEqual(command._enableShell, False)

    def test_construct_with_example(self):
        data = {
            'object':'CMD',
            'name':'commandName',
            'type':'commandType',
            'line': 'commandLine',
            'example': 'commandExample'
        }
        command = qakcentreon.lib.centreon.Command.Command.construct(data)
        self.assertIsInstance(command, qakcentreon.lib.centreon.Command.Command)
        self.assertEqual(command._name, 'commandName')
        self.assertEqual(command._type, 'commandType')
        self.assertEqual(command._line, 'commandLine')
        self.assertEqual(command._comment, 'commandExample')

    def test_construct_with_comment(self):
        data = {
            'object':'CMD',
            'name':'commandName',
            'type':'commandType',
            'line': 'commandLine',
            'comment': 'commandComment'
        }
        command = qakcentreon.lib.centreon.Command.Command.construct(data)
        self.assertIsInstance(command, qakcentreon.lib.centreon.Command.Command)
        self.assertEqual(command._name, 'commandName')
        self.assertEqual(command._type, 'commandType')
        self.assertEqual(command._line, 'commandLine')
        self.assertEqual(command._comment, 'commandComment')

    def test_construct_with_disable(self):
        data = {
            'object':'CMD',
            'name':'commandName',
            'type':'commandType',
            'line': 'commandLine',
            'activate': '0'
        }
        command = qakcentreon.lib.centreon.Command.Command.construct(data)
        self.assertIsInstance(command, qakcentreon.lib.centreon.Command.Command)
        self.assertEqual(command._name, 'commandName')
        self.assertEqual(command._type, 'commandType')
        self.assertEqual(command._line, 'commandLine')
        self.assertEqual(command._activate, False)

    def test_construct_with_enableshell(self):
        data = {
            'object':'CMD',
            'name':'commandName',
            'type':'commandType',
            'line': 'commandLine',
            'enable_shell': '1'
        }
        command = qakcentreon.lib.centreon.Command.Command.construct(data)
        self.assertIsInstance(command, qakcentreon.lib.centreon.Command.Command)
        self.assertEqual(command._name, 'commandName')
        self.assertEqual(command._type, 'commandType')
        self.assertEqual(command._line, 'commandLine')
        self.assertEqual(command._enableShell, True)

    def test_object_init(self):
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        self.assertIsInstance(command, qakcentreon.lib.centreon.Command.Command)
        self.assertEqual(command._name, 'commandName')
        self.assertEqual(command._type, 'commandType')
        self.assertEqual(command._line, 'commandLine')
        self.assertEqual(command._example, None)
        self.assertEqual(command._comment, None)
        self.assertEqual(command._activate, True)
        self.assertEqual(command._enableShell, False)

    def test_set_good_type(self):
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.setType('newType')
        self.assertEqual(command._type, 'newType')
        
    def test_enable(self):
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.enable()
        self.assertEqual(command._activate, True)

    def test_disable(self):
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.disable()
        self.assertEqual(command._activate, False)

    def test_set_comment(self):
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.setComment('myComment')
        self.assertEqual(command._comment, 'myComment')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_minimal(self, mock_stdout):
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.generate()
        self.assertEqual(mock_stdout.getvalue(), 'CMD;ADD;commandName;commandType;commandLine\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_minimal_with_set_type(self, mock_stdout):
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.setType('newType')
        command.generate()
        self.assertEqual(mock_stdout.getvalue(), 'CMD;ADD;commandName;newType;commandLine\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_enable_status(self, mock_stdout):
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.enable()
        command.generate()
        self.assertEqual(mock_stdout.getvalue(), 'CMD;ADD;commandName;commandType;commandLine\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_disable_status(self, mock_stdout):
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.disable()
        command.generate()
        self.assertEqual(mock_stdout.getvalue(), 'CMD;ADD;commandName;commandType;commandLine\nCMD;SETPARAM;commandName;activate;0\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_comment(self, mock_stdout):
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.setComment('commentValue')
        command.generate()
        self.assertEqual(mock_stdout.getvalue(), 'CMD;ADD;commandName;commandType;commandLine\nCMD;SETPARAM;commandName;comment;commentValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_none_comment(self, mock_stdout):
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.setComment(None)
        command.generate()
        self.assertEqual(mock_stdout.getvalue(), 'CMD;ADD;commandName;commandType;commandLine\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_minimal_same(self, mock_stdout):
        currentCommand = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.generate(currentCommand)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_minimal_type_update(self, mock_stdout):
        currentCommand = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'newType', 'commandLine')
        command.generate(currentCommand)
        self.assertEqual(mock_stdout.getvalue(), 'CMD;SETPARAM;commandName;type;newType\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_minimal_line_update(self, mock_stdout):
        currentCommand = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'newLine')
        command.generate(currentCommand)
        self.assertEqual(mock_stdout.getvalue(), 'CMD;SETPARAM;commandName;line;newLine\n')


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_enable_when_already_enabled(self, mock_stdout):
        currentCommand = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        currentCommand.enable()
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.enable()
        command.generate(currentCommand)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_enable_when_disabled(self, mock_stdout):
        currentCommand = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        currentCommand.disable()
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.enable()
        command.generate(currentCommand)
        self.assertEqual(mock_stdout.getvalue(), 'CMD;SETPARAM;commandName;activate;1\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_comment_when_already_defined_and_same(self, mock_stdout):
        currentCommand = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        currentCommand.setComment('commentValue')
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.setComment('commentValue')
        command.generate(currentCommand)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_comment_when_already_defined_and_different(self, mock_stdout):
        currentCommand = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        currentCommand.setComment('commentValue')
        command = qakcentreon.lib.centreon.Command.Command('commandName', 'commandType', 'commandLine')
        command.setComment('newValue')
        command.generate(currentCommand)
        self.assertEqual(mock_stdout.getvalue(), 'CMD;SETPARAM;commandName;comment;newValue\n')

if __name__ == '__main__':
    logging.disable = True
    unittest.main()
