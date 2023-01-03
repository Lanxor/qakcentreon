
import logging
import io
import unittest
import unittest.mock

import qakcentreon.lib.centreon.Aclresource


class TestLibCentreonAclresource(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_parse_line_wrong_object(self):
        data = qakcentreon.lib.centreon.Aclresource.Aclresource.parse('OTHER;ADD;resourceName;resourceAlias')
        self.assertEqual(data, {})

    def test_parse_line_add(self):
        data = qakcentreon.lib.centreon.Aclresource.Aclresource.parse('ACLRESOURCE;ADD;resourceName;resourceAlias')
        self.assertEqual(data, {'object':'ACLRESOURCE','name':'resourceName','alias':'resourceAlias'})

    def test_parse_line_setparam_alias(self):
        data = qakcentreon.lib.centreon.Aclresource.Aclresource.parse('ACLRESOURCE;SETPARAM;resourceName;alias;newAlias')
        self.assertEqual(data, {'object':'ACLRESOURCE','name':'resourceName','alias':'newAlias'})

    def test_parse_line_setparam_comment(self):
        data = qakcentreon.lib.centreon.Aclresource.Aclresource.parse('ACLRESOURCE;SETPARAM;resourceName;comment;newComment')
        self.assertEqual(data, {'object':'ACLRESOURCE','name':'resourceName','comment':'newComment'})

    def test_parse_line_setparam_activate_0(self):
        data = qakcentreon.lib.centreon.Aclresource.Aclresource.parse('ACLRESOURCE;SETPARAM;resourceName;activate;0')
        self.assertEqual(data, {'object':'ACLRESOURCE','name':'resourceName','activate':'0'})

    def test_parse_line_setparam_activate_1(self):
        data = qakcentreon.lib.centreon.Aclresource.Aclresource.parse('ACLRESOURCE;SETPARAM;resourceName;activate;1')
        self.assertEqual(data, {'object':'ACLRESOURCE','name':'resourceName','activate':'1'})

    def test_construct_empty_data(self):
        data = {}
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource.construct(data)
        self.assertIsNone(aclresource)

    def test_construct_wrong_object(self):
        data = {
            'object':'wrongObject'
        }
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource.construct(data)
        self.assertIsNone(aclresource)

    def test_construct_missing_name(self):
        data = {
            'object':'aclresource',
            'alias':'aclresourceAlias'
        }
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource.construct(data)
        self.assertIsNone(aclresource)

    def test_construct_missing_alias(self):
        data = {
            'object':'aclresource',
            'name':'aclresourceName'
        }
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource.construct(data)
        self.assertIsNone(aclresource)

    def test_construct_minimum(self):
        data = {
            'object':'aclresource',
            'name':'aclresourceName',
            'alias':'aclresourceAlias'
        }
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource.construct(data)
        self.assertIsInstance(aclresource, qakcentreon.lib.centreon.Aclresource.Aclresource)
        self.assertEqual(aclresource._name, 'aclresourceName')
        self.assertEqual(aclresource._alias, 'aclresourceAlias')
        self.assertEqual(aclresource._comment, None)
        self.assertEqual(aclresource._activate, True)

    def test_construct_with_comment(self):
        data = {
            'object':'aclresource',
            'name':'aclresourceName',
            'alias':'aclresourceAlias',
            'comment': 'commentValue'
        }
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource.construct(data)
        self.assertIsInstance(aclresource, qakcentreon.lib.centreon.Aclresource.Aclresource)
        self.assertEqual(aclresource._name, 'aclresourceName')
        self.assertEqual(aclresource._alias, 'aclresourceAlias')
        self.assertEqual(aclresource._comment, 'commentValue')

    def test_construct_with_disable(self):
        data = {
            'object':'aclresource',
            'name':'aclresourceName',
            'alias':'aclresourceAlias',
            'activate': '0'
        }
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource.construct(data)
        self.assertIsInstance(aclresource, qakcentreon.lib.centreon.Aclresource.Aclresource)
        self.assertEqual(aclresource._name, 'aclresourceName')
        self.assertEqual(aclresource._alias, 'aclresourceAlias')
        self.assertEqual(aclresource._activate, False)

    def test_object_init(self):
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        self.assertIsInstance(aclresource, qakcentreon.lib.centreon.Aclresource.Aclresource)
        self.assertEqual(aclresource._name, 'aclresourceName')
        self.assertEqual(aclresource._alias, 'aclresourceAlias')
        self.assertEqual(aclresource._activate, True)
        self.assertEqual(aclresource._comment, None)

    def test_set_alias(self):
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.setAlias('newAlias')
        self.assertEqual(aclresource._alias, 'newAlias')
        
    def test_enable(self):
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.enable()
        self.assertEqual(aclresource._activate, True)

    def test_disable(self):
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.disable()
        self.assertEqual(aclresource._activate, False)

    def test_set_comment(self):
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.setComment('myComment')
        self.assertEqual(aclresource._comment, 'myComment')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_minimal(self, mock_stdout):
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLRESOURCE;ADD;aclresourceName;aclresourceAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_minimal_with_set_alias(self, mock_stdout):
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.setAlias('newAlias')
        aclresource.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLRESOURCE;ADD;aclresourceName;newAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_enable_status(self, mock_stdout):
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.enable()
        aclresource.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLRESOURCE;ADD;aclresourceName;aclresourceAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_disable_status(self, mock_stdout):
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.disable()
        aclresource.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLRESOURCE;ADD;aclresourceName;aclresourceAlias\nACLRESOURCE;SETPARAM;aclresourceName;activate;0\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_comment(self, mock_stdout):
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.setComment('commentValue')
        aclresource.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLRESOURCE;ADD;aclresourceName;aclresourceAlias\nACLRESOURCE;SETPARAM;aclresourceName;comment;commentValue\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_with_none_comment(self, mock_stdout):
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.setComment(None)
        aclresource.generate()
        self.assertEqual(mock_stdout.getvalue(), 'ACLRESOURCE;ADD;aclresourceName;aclresourceAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_minimal_same(self, mock_stdout):
        currentAclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.generate(currentAclresource)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_minimal_alias_update(self, mock_stdout):
        currentAclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'newAlias')
        aclresource.generate(currentAclresource)
        self.assertEqual(mock_stdout.getvalue(), 'ACLRESOURCE;SETPARAM;aclresourceName;alias;newAlias\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_enable_when_already_enabled(self, mock_stdout):
        currentAclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        currentAclresource.enable()
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.enable()
        aclresource.generate(currentAclresource)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_enable_when_disabled(self, mock_stdout):
        currentAclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        currentAclresource.disable()
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.enable()
        aclresource.generate(currentAclresource)
        self.assertEqual(mock_stdout.getvalue(), 'ACLRESOURCE;SETPARAM;aclresourceName;activate;1\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_comment_when_already_defined_and_same(self, mock_stdout):
        currentAclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        currentAclresource.setComment('commentValue')
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.setComment('commentValue')
        aclresource.generate(currentAclresource)
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_diff_comment_when_already_defined_and_different(self, mock_stdout):
        currentAclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        currentAclresource.setComment('commentValue')
        aclresource = qakcentreon.lib.centreon.Aclresource.Aclresource('aclresourceName', 'aclresourceAlias')
        aclresource.setComment('newValue')
        aclresource.generate(currentAclresource)
        self.assertEqual(mock_stdout.getvalue(), 'ACLRESOURCE;SETPARAM;aclresourceName;comment;newValue\n')

if __name__ == '__main__':
    logging.disable = True
    unittest.main()
