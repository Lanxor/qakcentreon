
import logging
import io
import unittest
import unittest.mock

import qakcentreon.lib.centreon.Aclaction


class TestLibCentreonAclaction(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_parse_line_wrong_object(self):
        data = qakcentreon.lib.centreon.Aclaction.Aclaction.parse('OTHER;ADD;actionName;actionDescription')
        self.assertEqual(data, {})

    def test_parse_line_add(self):
        data = qakcentreon.lib.centreon.Aclaction.Aclaction.parse('ACLACTION;ADD;actionName;actionDescription')
        self.assertEqual(data, {'object':'ACLACTION','name':'actionName','description':'actionDescription'})

    def test_parse_line_setparam_description(self):
        data = qakcentreon.lib.centreon.Aclaction.Aclaction.parse('ACLACTION;SETPARAM;actionName;description;newDescription')
        self.assertEqual(data, {'object':'ACLACTION','name':'actionName','description':'newDescription'})

    def test_parse_line_setparam_activate_0(self):
        data = qakcentreon.lib.centreon.Aclaction.Aclaction.parse('ACLACTION;SETPARAM;actionName;activate;0')
        self.assertEqual(data, {'object':'ACLACTION','name':'actionName','activate':'0'})

    def test_parse_line_setparam_activate_1(self):
        data = qakcentreon.lib.centreon.Aclaction.Aclaction.parse('ACLACTION;SETPARAM;actionName;activate;1')
        self.assertEqual(data, {'object':'ACLACTION','name':'actionName','activate':'1'})

    def test_parse_line_grant(self):
        data = qakcentreon.lib.centreon.Aclaction.Aclaction.parse('ACLACTION;GRANT;actionName;firstAction')
        self.assertEqual(data, {'object':'ACLACTION','name':'actionName','grant':['firstAction']})

    def test_parse_line_two_grant(self):
        data = qakcentreon.lib.centreon.Aclaction.Aclaction.parse('ACLACTION;GRANT;actionName;firstAction|secondAction')
        self.assertEqual(data, {'object':'ACLACTION','name':'actionName','grant':['firstAction','secondAction']})

    def test_parse_line_revoke(self):
        data = qakcentreon.lib.centreon.Aclaction.Aclaction.parse('ACLACTION;REVOKE;actionName;firstAction')
        self.assertEqual(data, {'object':'ACLACTION','name':'actionName','revoke':['firstAction']})

    def test_parse_line_two_revoke(self):
        data = qakcentreon.lib.centreon.Aclaction.Aclaction.parse('ACLACTION;REVOKE;actionName;firstAction|secondAction')
        self.assertEqual(data, {'object':'ACLACTION','name':'actionName','revoke':['firstAction','secondAction']})

    def test_object_init(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        self.assertEqual(aclaction._name, 'aclactionName')
        self.assertEqual(aclaction._description, 'aclactionDescription')
        self.assertEqual(aclaction._activate, True)
        self.assertEqual(aclaction._grant, [])
        self.assertEqual(aclaction._revoke, [])

    def test_set_description(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setDescription('newDescription')
        self.assertEqual(aclaction._description, 'newDescription')
        
    def test_enable(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.enable()
        self.assertEqual(aclaction._activate, True)

    def test_disable(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.disable()
        self.assertEqual(aclaction._activate, False)

    def test_set_grant(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('firstAction')
        self.assertEqual(aclaction._grant,['firstAction'])

    def test_set_two_grant(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('firstAction')
        aclaction.setGrant('secondAction')
        self.assertEqual(aclaction._grant,['firstAction', 'secondAction'])

    def test_set_grant_with_revoke_already_defined(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('firstAction')
        aclaction.setGrant('firstAction')
        self.assertEqual(aclaction._revoke,[])
        self.assertEqual(aclaction._grant,['firstAction'])

    def test_set_grant_with_two_revoke_already_defined(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('firstAction')
        aclaction.setRevoke('secondAction')
        aclaction.setGrant('firstAction')
        self.assertEqual(aclaction._revoke,['secondAction'])
        self.assertEqual(aclaction._grant,['firstAction'])

    def test_set_revoke(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('firstAction')
        self.assertEqual(aclaction._revoke,['firstAction'])

    def test_set_two_revoke(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('firstAction')
        aclaction.setRevoke('secondAction')
        self.assertEqual(aclaction._revoke,['firstAction', 'secondAction'])

    def test_set_revoke_with_grant_already_defined(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('firstAction')
        aclaction.setRevoke('firstAction')
        self.assertEqual(aclaction._grant,[])
        self.assertEqual(aclaction._revoke,['firstAction'])

    def test_set_revoke_with_two_grant_already_defined(self):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('firstAction')
        aclaction.setGrant('secondAction')
        aclaction.setRevoke('firstAction')
        self.assertEqual(aclaction._grant,['secondAction'])
        self.assertEqual(aclaction._revoke,['firstAction'])

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_minimal(self, mock_stdout):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;ADD;aclactionName;aclactionDescription\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_minimal_with_set_description(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclmenu.setDescription('newDescription')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;ADD;aclactionName;newDescription\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_enable_status(self, mock_stdout):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.enable()
        aclaction.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;ADD;aclactionName;aclactionDescription\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_disable_status(self, mock_stdout):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.disable()
        aclaction.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;ADD;aclactionName;aclactionDescription\nACLACTION;SETPARAM;aclactionName;activate;0\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_grant(self, mock_stdout):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('actionValue')
        aclaction.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;ADD;aclactionName;aclactionDescription\nACLACTION;GRANT;aclactionName;actionValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_two_set_grant(self, mock_stdout):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('firstAction')
        aclaction.setGrant('secondAction')
        aclaction.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;ADD;aclactionName;aclactionDescription\nACLACTION;GRANT;aclactionName;firstAction|secondAction\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_grant_but_revoke_already_exist(self, mock_stdout):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('actionValue')
        aclaction.setGrant('actionValue')
        aclaction.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;ADD;aclactionName;aclactionDescription\nACLACTION;GRANT;aclactionName;actionValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_revoke(self, mock_stdout):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('actionValue')
        aclaction.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;ADD;aclactionName;aclactionDescription\nACLACTION;REVOKE;aclactionName;actionValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_two_set_revoke(self, mock_stdout):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('firstAction')
        aclaction.setRevoke('secondAction')
        aclaction.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;ADD;aclactionName;aclactionDescription\nACLACTION;REVOKE;aclactionName;firstAction|secondAction\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_revoke_but_grant_already_exist(self, mock_stdout):
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('actionValue')
        aclaction.setRevoke('actionValue')
        aclaction.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;ADD;aclactionName;aclactionDescription\nACLACTION;REVOKE;aclactionName;actionValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_minimal_same(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_minimal_description_update(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'newDescription')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;SETPARAM;aclactionName;description;newDescription\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_enable_when_already_enabled(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        currentAclaction.enable()
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.enable()
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_enable_when_disabled(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        currentAclaction.disable()
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.enable()
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;SETPARAM;aclactionName;activate;1\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grant_when_already_defined_and_same(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        currentAclaction.setGrant('actionValue')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('actionValue')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grant_when_two_already_defined_and_same(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        currentAclaction.setGrant('firstAction')
        currentAclaction.setGrant('secondAction')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('firstAction')
        aclaction.setGrant('secondAction')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grant_new_value_01(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('actionValue')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;GRANT;aclactionName;actionValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grant_new_value_02(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        currentAclaction.setGrant('firstAction')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('firstAction')
        aclaction.setGrant('secondAction')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;GRANT;aclactionName;firstAction|secondAction\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grant_two_new_value(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        currentAclaction.setGrant('firstAction')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('firstAction')
        aclaction.setGrant('secondAction')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;GRANT;aclactionName;firstAction|secondAction\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grant_replace_from_revoke(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        currentAclaction.setRevoke('actionValue')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setGrant('actionValue')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;GRANT;aclactionName;actionValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_revoke_when_already_defined_and_same(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        currentAclaction.setRevoke('actionValue')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('actionValue')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_revoke_when_two_already_defined_and_same(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        currentAclaction.setRevoke('firstAction')
        currentAclaction.setRevoke('secondAction')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('firstAction')
        aclaction.setRevoke('secondAction')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_revoke_new_value_01(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('actionValue')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;REVOKE;aclactionName;actionValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_revoke_new_value_02(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        currentAclaction.setRevoke('firstAction')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('firstAction')
        aclaction.setRevoke('secondAction')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;REVOKE;aclactionName;firstAction|secondAction\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_revoke_two_new_value(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('firstAction')
        aclaction.setRevoke('secondAction')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;REVOKE;aclactionName;firstAction|secondAction\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_revoke_replace_from_grant(self, mock_stdout):
        currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        currentAclaction.setGrant('actionValue')
        aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
        aclaction.setRevoke('actionValue')
        aclaction.generate(currentAclaction)
        self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;REVOKE;aclactionName;actionValue\n')

    # @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    # def test_generate_diff_revoke_replace_from_grantro(self, mock_stdout):
    #     currentAclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
    #     currentAclaction.setGrantRo('Home')
    #     aclaction = qakcentreon.lib.centreon.Aclaction.Aclaction('aclactionName', 'aclactionDescription')
    #     aclaction.setRevoke('Home')
    #     aclaction.generate(currentAclaction)
    #     self.assertEqual(mock_stdout.getvalue(), 'ACLACTION;REVOKE;aclactionName;0;Home\n')

if __name__ == '__main__':
    logging.disable = True
    unittest.main()
