
import logging
import io
import unittest
import unittest.mock

import qakcentreon.lib.centreon.Aclmenu


class TestLibCentreonAclmenu(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_parse_line_wrong_object(self):
        data = qakcentreon.lib.centreon.Aclmenu.Aclmenu.parse('OTHER;ADD;menuName;menuAlias')
        self.assertEqual(data, {})

    def test_parse_line_add(self):
        data = qakcentreon.lib.centreon.Aclmenu.Aclmenu.parse('ACLMENU;ADD;menuName;menuAlias')
        self.assertEqual(data, {'object':'ACLMENU','name':'menuName','alias':'menuAlias'})

    def test_parse_line_setparam_alias(self):
        data = qakcentreon.lib.centreon.Aclmenu.Aclmenu.parse('ACLMENU;SETPARAM;menuName;alias;newAlias')
        self.assertEqual(data, {'object':'ACLMENU','name':'menuName','alias':'newAlias'})

    def test_parse_line_setparam_comment(self):
        data = qakcentreon.lib.centreon.Aclmenu.Aclmenu.parse('ACLMENU;SETPARAM;menuName;comment;newComment')
        self.assertEqual(data, {'object':'ACLMENU','name':'menuName','comment':'newComment'})

    def test_parse_line_setparam_activate_0(self):
        data = qakcentreon.lib.centreon.Aclmenu.Aclmenu.parse('ACLMENU;SETPARAM;menuName;activate;0')
        self.assertEqual(data, {'object':'ACLMENU','name':'menuName','activate':'0'})

    def test_parse_line_setparam_activate_1(self):
        data = qakcentreon.lib.centreon.Aclmenu.Aclmenu.parse('ACLMENU;SETPARAM;menuName;activate;1')
        self.assertEqual(data, {'object':'ACLMENU','name':'menuName','activate':'1'})

    def test_parse_line_grantrw(self):
        data = qakcentreon.lib.centreon.Aclmenu.Aclmenu.parse('ACLMENU;GRANTRW;menuName;0;firstMenu')
        self.assertEqual(data, {'object':'ACLMENU','name':'menuName','grantrw':['firstMenu']})

    def test_parse_line_grantro(self):
        data = qakcentreon.lib.centreon.Aclmenu.Aclmenu.parse('ACLMENU;GRANTRO;menuName;0;firstMenu')
        self.assertEqual(data, {'object':'ACLMENU','name':'menuName','grantro':['firstMenu']})

    def test_parse_line_revoke(self):
        data = qakcentreon.lib.centreon.Aclmenu.Aclmenu.parse('ACLMENU;REVOKE;menuName;0;firstMenu')
        self.assertEqual(data, {'object':'ACLMENU','name':'menuName','revoke':['firstMenu']})

    def test_object_init(self):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        self.assertEqual(aclmenu._name, 'aclmenuName')
        self.assertEqual(aclmenu._alias, 'aclmenuAlias')
        self.assertEqual(aclmenu._activate, True)
        self.assertEqual(aclmenu._comment, None)
        self.assertEqual(aclmenu._grantrw, [])
        self.assertEqual(aclmenu._grantro, [])
        self.assertEqual(aclmenu._revoke, [])

    def test_set_alias(self):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setAlias('newAlias')
        self.assertEqual(aclmenu._alias, 'newAlias')
        
    def test_enable(self):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.enable()
        self.assertEqual(aclmenu._activate, True)

    def test_disable(self):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.disable()
        self.assertEqual(aclmenu._activate, False)

    def test_set_comment(self):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setComment('myComment')
        self.assertEqual(aclmenu._comment, 'myComment')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_minimal(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_minimal_with_set_alias(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setAlias('newAlias')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;newAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_enable_status(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.enable()
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_disable_status(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.disable()
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\nACLMENU;SETPARAM;aclmenuName;activate;0\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_comment(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setComment('commentValue')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\nACLMENU;SETPARAM;aclmenuName;comment;commentValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_none_comment(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setComment(None)
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_grantrw(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRw('menuValue')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\nACLMENU;GRANTRW;aclmenuName;0;menuValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_grantrw_but_grantro_already_exist(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRo('menuValue')
        aclmenu.setGrantRw('menuValue')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\nACLMENU;GRANTRW;aclmenuName;0;menuValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_grantrw_but_revoke_already_exist(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setRevoke('menuValue')
        aclmenu.setGrantRw('menuValue')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\nACLMENU;GRANTRW;aclmenuName;0;menuValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_grantro(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRo('menuValue')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\nACLMENU;GRANTRO;aclmenuName;0;menuValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_grantro_but_grantrw_already_exist(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRw('menuValue')
        aclmenu.setGrantRo('menuValue')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\nACLMENU;GRANTRO;aclmenuName;0;menuValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_grantro_but_revoke_already_exist(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setRevoke('menuValue')
        aclmenu.setGrantRo('menuValue')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\nACLMENU;GRANTRO;aclmenuName;0;menuValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_revoke(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setRevoke('menuValue')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\nACLMENU;REVOKE;aclmenuName;0;menuValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_revoke_but_grantrw_already_exist(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRw('menuValue')
        aclmenu.setRevoke('menuValue')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\nACLMENU;REVOKE;aclmenuName;0;menuValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_set_revoke_but_grantro_already_exist(self, mock_stdout):
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRo('menuValue')
        aclmenu.setRevoke('menuValue')
        aclmenu.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;ADD;aclmenuName;aclmenuAlias\nACLMENU;REVOKE;aclmenuName;0;menuValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_minimal_same(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_minimal_alias_update(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'newAlias')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;SETPARAM;aclmenuName;alias;newAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_enable_when_already_enabled(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.enable()
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.enable()
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_enable_when_disabled(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.disable()
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.enable()
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;SETPARAM;aclmenuName;activate;1\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_comment_when_already_defined_and_same(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setComment('commentValue')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setComment('commentValue')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_comment_when_already_defined_and_different(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setComment('commentValue')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setComment('newValue')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;SETPARAM;aclmenuName;comment;newValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grantrw_when_already_defined_and_same(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setGrantRw('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRw('Home')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grantrw_new_value(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setGrantRw('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRw('Home')
        aclmenu.setGrantRw('Configuration')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;GRANTRW;aclmenuName;0;Configuration\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grantrw_replace_from_grantro(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setGrantRo('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRw('Home')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;GRANTRW;aclmenuName;0;Home\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grantrw_replace_from_revoke(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setRevoke('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRw('Home')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;GRANTRW;aclmenuName;0;Home\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grantro_when_already_defined_and_same(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setGrantRo('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRo('Home')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grantro_new_value(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setGrantRo('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRo('Home')
        aclmenu.setGrantRo('Configuration')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;GRANTRO;aclmenuName;0;Configuration\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grantro_replace_from_grantrw(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setGrantRw('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRo('Home')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;GRANTRO;aclmenuName;0;Home\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_grantro_replace_from_revoke(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setRevoke('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setGrantRo('Home')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;GRANTRO;aclmenuName;0;Home\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_revoke_when_already_defined_and_same(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setRevoke('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setRevoke('Home')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_revoke_new_value(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setRevoke('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setRevoke('Home')
        aclmenu.setRevoke('Configuration')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;REVOKE;aclmenuName;0;Configuration\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_revoke_replace_from_grantrw(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setGrantRw('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setRevoke('Home')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;REVOKE;aclmenuName;0;Home\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_revoke_replace_from_grantro(self, mock_stdout):
        currentAclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        currentAclmenu.setGrantRo('Home')
        aclmenu = qakcentreon.lib.centreon.Aclmenu.Aclmenu('aclmenuName', 'aclmenuAlias')
        aclmenu.setRevoke('Home')
        aclmenu.generate(currentAclmenu)
        self.assertEqual(mock_stdout.getvalue(), 'ACLMENU;REVOKE;aclmenuName;0;Home\n')

if __name__ == '__main__':
    logging.disable = True
    unittest.main()
