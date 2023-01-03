
import logging
import io
import unittest
import unittest.mock

import qakcentreon.lib.centreon.Aclgroup


class TestLibCentreonAclgroup(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_parse_line_wrong_object(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('OTHER;ADD;groupName;groupAlias')
        self.assertEqual(data, {})

    def test_parse_line_add(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;ADD;groupName;groupAlias')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','alias':'groupAlias'})

    def test_parse_line_setparam_alias(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETPARAM;groupName;alias;newAlias')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','alias':'newAlias'})

    def test_parse_line_setparam_comment(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETPARAM;groupName;comment;newComment')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','comment':'newComment'})

    def test_parse_line_setparam_activate_0(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETPARAM;groupName;activate;0')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','activate':'0'})

    def test_parse_line_setparam_activate_1(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETPARAM;groupName;activate;1')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','activate':'1'})

    def test_parse_line_setcontact_one(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETCONTACT;groupName;contactOne')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','contact':['contactOne']})

    def test_parse_line_setcontact_two(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETCONTACT;groupName;contactOne|contactTwo')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','contact':['contactOne','contactTwo']})

    def test_parse_line_setcontactgroup_one(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETCONTACTGROUP;groupName;contactgroupOne')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','contactgroup':['contactgroupOne']})

    def test_parse_line_setcontactgroup_two(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETCONTACTGROUP;groupName;contactgroupOne|contactgroupTwo')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','contactgroup':['contactgroupOne','contactgroupTwo']})

    def test_parse_line_setmenu_one(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETMENU;groupName;menuOne')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','menu':['menuOne']})

    def test_parse_line_setmenu_two(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETMENU;groupName;menuOne|menuTwo')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','menu':['menuOne','menuTwo']})

    def test_parse_line_setaction_one(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETACTION;groupName;actionOne')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','action':['actionOne']})

    def test_parse_line_setaction_two(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETACTION;groupName;actionOne|actionTwo')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','action':['actionOne','actionTwo']})

    def test_parse_line_setresource_one(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETRESOURCE;groupName;resourceOne')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','resource':['resourceOne']})

    def test_parse_line_setresource_two(self):
        data = qakcentreon.lib.centreon.Aclgroup.Aclgroup.parse('ACLGROUP;SETRESOURCE;groupName;resourceOne|resourceTwo')
        self.assertEqual(data, {'object':'ACLGROUP','name':'groupName','resource':['resourceOne','resourceTwo']})

    def test_construct_empty_data(self):
        data = {}
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup.construct(data)
        self.assertIsNone(aclgroup)

    def test_construct_wrong_object(self):
        data = {
            'object':'wrongObject'
        }
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup.construct(data)
        self.assertIsNone(aclgroup)

    def test_construct_missing_name(self):
        data = {
            'object':'aclgroup',
            'alias':'aclgroupAlias'
        }
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup.construct(data)
        self.assertIsNone(aclgroup)

    def test_construct_missing_alias(self):
        data = {
            'object':'aclgroup',
            'name':'aclgroupName'
        }
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup.construct(data)
        self.assertIsNone(aclgroup)

    def test_construct_minimum(self):
        data = {
            'object':'aclgroup',
            'name':'aclgroupName',
            'alias':'aclgroupAlias'
        }
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup.construct(data)
        self.assertIsInstance(aclgroup, qakcentreon.lib.centreon.Aclgroup.Aclgroup)
        self.assertEqual(aclgroup._name, 'aclgroupName')
        self.assertEqual(aclgroup._alias, 'aclgroupAlias')
        self.assertEqual(aclgroup._activate, True)
        self.assertEqual(aclgroup._contact, [])
        self.assertEqual(aclgroup._contactGroup, [])
        self.assertEqual(aclgroup._menu, [])
        self.assertEqual(aclgroup._action, [])
        self.assertEqual(aclgroup._resource, [])

    def test_construct_with_disable(self):
        data = {
            'object':'aclgroup',
            'name':'aclgroupName',
            'alias':'aclgroupAlias',
            'activate': '0'
        }
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup.construct(data)
        self.assertIsInstance(aclgroup, qakcentreon.lib.centreon.Aclgroup.Aclgroup)
        self.assertEqual(aclgroup._name, 'aclgroupName')
        self.assertEqual(aclgroup._alias, 'aclgroupAlias')
        self.assertEqual(aclgroup._activate, False)

    def test_object_init(self):
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        self.assertIsInstance(aclgroup, qakcentreon.lib.centreon.Aclgroup.Aclgroup)
        self.assertEqual(aclgroup._name, 'aclgroupName')
        self.assertEqual(aclgroup._alias, 'aclgroupAlias')
        self.assertEqual(aclgroup._activate, True)

    def test_set_alias(self):
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup.setAlias('newAlias')
        self.assertEqual(aclgroup._alias, 'newAlias')
        
    def test_enable(self):
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup.enable()
        self.assertEqual(aclgroup._activate, True)

    def test_disable(self):
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup.disable()
        self.assertEqual(aclgroup._activate, False)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_minimal(self, mock_stdout):
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLGROUP;ADD;aclgroupName;aclgroupAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_minimal_with_set_alias(self, mock_stdout):
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup.setAlias('newAlias')
        aclgroup.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLGROUP;ADD;aclgroupName;newAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_enable_status(self, mock_stdout):
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup.enable()
        aclgroup.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLGROUP;ADD;aclgroupName;aclgroupAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_disable_status(self, mock_stdout):
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup.disable()
        aclgroup.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLGROUP;ADD;aclgroupName;aclgroupAlias\nACLGROUP;SETPARAM;aclgroupName;activate;0\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_minimal_same(self, mock_stdout):
        currentAclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup.generate(currentAclgroup)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_minimal_alias_update(self, mock_stdout):
        currentAclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'newAlias')
        aclgroup.generate(currentAclgroup)
        self.assertEqual(mock_stdout.getvalue(), 'ACLGROUP;SETPARAM;aclgroupName;alias;newAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_enable_when_already_enabled(self, mock_stdout):
        currentAclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        currentAclgroup.enable()
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup.enable()
        aclgroup.generate(currentAclgroup)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_enable_when_disabled(self, mock_stdout):
        currentAclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        currentAclgroup.disable()
        aclgroup = qakcentreon.lib.centreon.Aclgroup.Aclgroup('aclgroupName', 'aclgroupAlias')
        aclgroup.enable()
        aclgroup.generate(currentAclgroup)
        self.assertEqual(mock_stdout.getvalue(), 'ACLGROUP;SETPARAM;aclgroupName;activate;1\n')

if __name__ == '__main__':
    logging.disable = True
    unittest.main()
