import unittest
from unittest.mock import MagicMock, patch
from typing import Any  
from io import BytesIO
import pandas as pd
from openpyxl import Workbook
from scrape_data import get_driver, write_file, scrape_website  
from selenium.webdriver.common.by import By

class TestScrapingFunctions(unittest.TestCase):

    def create_mock_excel(self):
        wb = Workbook()
        ws = wb.active
        ws['A1'] = 'Establishment Name (DECRS)'
        ws['B1'] = 'DUNS (DECRS)'
        ws['C1'] = 'Business Operations (DECRS)'
        ws['D1'] = 'Registration Expiration Date (DECRS)'
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        return buffer

    


    @patch('selenium.webdriver.Chrome')
    @patch('selenium.webdriver.common.by.By')
    def test_scrape_website(self, mock_by, mock_chrome_driver):
      
        mock_driver = MagicMock()
        mock_chrome_driver.return_value = mock_driver
        mock_driver.find_element.return_value.text = "Test Data"
        
      
        mock_driver.find_element(By.ID, 'decrs_table').find_elements.return_value = [MagicMock()]
        
        
        excel_file = self.create_mock_excel()
        
       
        establishments_list = {1: 'Test Address', 2: 'Another Address'}
        links = ['http://mock.com']
        search_param = 'address'
        
       
        buffer = scrape_website(excel_file, links, establishments_list, search_param)
        
      
        mock_driver.find_element.assert_called_with(By.ID, 'decrs_table')
        self.assertIsInstance(buffer, BytesIO)

    
if __name__ == '__main__':
    unittest.main()
