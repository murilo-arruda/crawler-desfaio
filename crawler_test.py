from crawler import make_n_drivers, close_drivers,get_categorys, get_products
from selenium.common.exceptions import WebDriverException
import unittest

class TestDrivers(unittest.TestCase):
    def setUp(self):
        try:
            self.drivers = make_n_drivers(1)
        except WebDriverException:
            print(" Message: 'geckodriver' executable needs to be in PATH. skiping the tests...")
            self.skipTest("Error while creating the driver.")

    def tearDown(self):
        close_drivers(self.drivers)

    def test_driver_creation(self):
        self.assertEqual(len(self.drivers), 1)

    def test_get_categorys(self):
        self.assertEqual(type(get_categorys("https://www.epocacosmeticos.com.br/", self.drivers[0])), list)

    def test_if_category_have_links(self):
        categorys =  get_categorys("https://www.epocacosmeticos.com.br/", self.drivers[0])
        for category in categorys:
            self.assertEqual(category[:4], "http")

    def test_get_products(self):
        self.assertEqual(
            type(get_products("https://www.epocacosmeticos.com.br/unhas", self.drivers[0],8, [])),
            list)

    def test_if_products_has_found(self):
        products = get_products("https://www.epocacosmeticos.com.br/unhas", self.drivers[0],8, [])
        for product in products:
            self.assertEqual(product[0][-1], "p")

if __name__ == '__main__':
    unittest.main(warnings='ignore')