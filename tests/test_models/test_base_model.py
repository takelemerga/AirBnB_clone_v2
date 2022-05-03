#!/usr/bin/python3
"""
Unittest for BaseModel class
"""
import unittest
from datetime import datetime
import os

from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base1 = BaseModel()
        cls.base1.name = "Arik"
        cls.base1.my_number = 29

    @classmethod
    def tearDownClass(cls):
        del cls.base1
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_checking_for_functions(self):
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)

    def test_attributes(self):
        self.assertTrue(hasattr(BaseModel, "__init__"))
        self.assertTrue(hasattr(BaseModel, "save"))
        self.assertTrue(hasattr(BaseModel, "to_dict"))

    def test_init(self):
        self.assertTrue(isinstance(self.base1, BaseModel))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "won't work in db")
    def test_save(self):
        self.base1.save()
        self.assertNotEqual(self.base1.created_at, self.base1.updated_at)

    def test_to_dict(self):
        base1_dict = self.base1.to_dict()
        self.assertEqual(self.base1.__class__.__name__, 'BaseModel')
        self.assertIsInstance(base1_dict['created_at'], str)
        self.assertIsInstance(base1_dict['updated_at'], str)
    obj = BaseModel()
    def testattr(self):
        """Test the attributes of BaseModel"""  # test scenario
        self.assertTrue(hasattr(self.obj, "created_at"))  # testcase
        self.assertTrue(hasattr(self.obj, "id"))  # testcase
        self.assertTrue(hasattr(self.obj, "updated_at"))
        self.assertTrue(type(self.obj.created_at) is datetime)
        self.assertEqual(type(self.obj.updated_at), datetime)
        self.assertTrue(type(self.obj.id) is str)
        self.assertFalse(type(self.obj.created_at) is str)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary"""  # testscenari
        dictio = self.obj.to_dict()
        self.assertTrue(type(dictio) is dict)  # testcase
        self.assertIn('__class__', dictio.keys())  # testcase
        self.assertIn('created_at', dictio.keys())  # testcase
        self.assertIn('updated_at', dictio.keys())
        self.assertIn('id', dictio.keys())
        self.assertEqual(dictio["__class__"], self.obj.__class__.__name__)
        self.assertTrue(type(dictio["created_at"]) is str)

    def test_dict_args(self):
        """testing when dictionary passed as argument"""  # test scenario
        dictionary = self.obj.to_dict()
        inst = BaseModel(**dictionary)
        self.assertFalse(self.obj is inst)  # testcase
        self.assertNotIn("__class__", inst.__dict__.keys())  # testcase
        self.assertNotEqual(inst.__dict__, dictionary)
        self.assertTrue(type(inst.created_at) is datetime)

    def test_save(self):
        """testing updated_at when save method called"""
        before = self.obj.to_dict()
        self.obj.save()
        after = self.obj.to_dict()
        self.assertNotEqual(before["updated_at"], after["updated_at"])
        self.assertEqual(before["created_at"], after["created_at"])
        self.assertEqual(before["id"], after["id"])   


if __name__ == "__main__":
    unittest.main()
