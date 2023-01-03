
import logging
import io
import unittest
import unittest.mock

from qakcentreon.lib.centreon.Aclmenu import Aclmenu
from qakcentreon.lib.centreon.Aclaction import Aclaction
from qakcentreon.lib.centreon.Aclgroup import Aclgroup
import qakcentreon.lib.centreon.exportparser


class TestLibCentreonExportparser(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)
        
    def test_parse_aclmenu_oneline(self):
        data = qakcentreon.lib.centreon.exportparser.parse_export('ACLMENU;ADD;menuName;menuAlias')
        self.assertIn('ACLMENU', data)
        self.assertIn('menuName', data['ACLMENU'])
        # self.assertEqual(data['ACLMENU']['menuName'], {'object':'ACLMENU','name':'menuName','alias':'menuAlias'})

    def test_parse_aclmenu_with_not_aclmenu(self):
        data = qakcentreon.lib.centreon.exportparser.parse_export('ACL;ADD;menuName;menuAlias')
        self.assertNotIn('ACLMENU', data)

    def test_parse_complete_export(self):
        with open('tests/data/export_complete_export.txt', 'rt') as exportData:
            data = qakcentreon.lib.centreon.exportparser.parse_export(exportData.read())

        self.assertIn('ACLMENU', data)
        self.assertIn('menuName', data['ACLMENU'])
        self.assertIsInstance(data['ACLMENU']['menuName'], Aclmenu)
        self.assertEqual(data['ACLMENU']['menuName']._name, 'menuName')
        self.assertEqual(data['ACLMENU']['menuName']._alias, 'menuAlias')
        self.assertEqual(data['ACLMENU']['menuName']._activate, False)
        self.assertEqual(data['ACLMENU']['menuName']._comment, 'menuComment')
        self.assertEqual(data['ACLMENU']['menuName']._grantrw, ['firstMenu','secondMenu'])
        self.assertEqual(data['ACLMENU']['menuName']._grantro, ['thirdMenu','fourthMenu'])
        self.assertEqual(data['ACLMENU']['menuName']._revoke, ['fifthMenu','sixthMenu'])

        self.assertIn('ACLACTION', data)
        self.assertIn('actionName', data['ACLACTION'])
        self.assertIsInstance(data['ACLACTION']['actionName'], Aclaction)
        self.assertEqual(data['ACLACTION']['actionName']._name, 'actionName')
        self.assertEqual(data['ACLACTION']['actionName']._description, 'actionDescription')
        self.assertEqual(data['ACLACTION']['actionName']._grant, ['firstAction','secondAction'])
        self.assertEqual(data['ACLACTION']['actionName']._revoke, ['thirdAction','fourthAction'])

        self.assertIn('ACLGROUP', data)
        self.assertIn('groupName', data['ACLGROUP'])
        self.assertIsInstance(data['ACLGROUP']['groupName'], Aclgroup)
        self.assertEqual(data['ACLGROUP']['groupName']._name, 'groupName')
        self.assertEqual(data['ACLGROUP']['groupName']._alias, 'groupAlias')

if __name__ == '__main__':
    unittest.main()
