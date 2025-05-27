import argparse
import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

args = None


class FileUploadTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)
        cls.base_url = args.base_url.rstrip('/')
        cls.sample_file = os.path.join(os.path.dirname(__file__), 'test_data', 'test_example.pdf')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_upload_with_folder_and_tags(self):
        driver = self.driver
        driver.get(f"{self.base_url}/#/content")

        # create new folder
        create_folder_btn = driver.find_element(By.XPATH, "//button[contains(., 'Create new folder')]")
        create_folder_btn.click()

        text_input = driver.find_element(By.CSS_SELECTOR, "input[id^='textField']")
        folder_name = f"selenium-folder-{int(time.time())}"
        text_input.send_keys(folder_name)
        driver.find_element(By.XPATH, "//button[contains(., 'Create folder')]").click()

        # add tag
        tag_input = driver.find_element(By.CSS_SELECTOR, "input[id^='tag-inline-picker']")
        tag_name = f"selenium-tag-{int(time.time())}"
        tag_input.send_keys(tag_name)
        tag_input.send_keys(Keys.ENTER)

        # upload file
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file'][aria-label='add files']")
        file_input.send_keys(self.sample_file)

        upload_btn = driver.find_element(By.XPATH, "//button[@aria-label='upload files']")
        upload_btn.click()

        progress = driver.find_element(By.CSS_SELECTOR, "progress")
        for _ in range(60):
            if progress.get_attribute('value') == '100':
                break
            time.sleep(1)
        self.assertEqual(progress.get_attribute('value'), '100')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', required=True, help='Base URL of the running web app')
    args = parser.parse_args()
    globals()['args'] = args
    unittest.main(argv=['first-arg-is-ignored'])
