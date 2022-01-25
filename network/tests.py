from django.test import Client, TestCase
import os
import pathlib
import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .models import User, Post

#

def file_uri(filename):
		return pathlib.Path((os.path.abspath(filename))) 

# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome()
timeout = 10
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'follow'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print ("Timed out waiting for page to load")

class UserTestCase(TestCase):
	# separate test db, setUp is a special function
	def setUp(self):
		u1 = User.objects.create(username="dn", password="dn", email="dn@msn.com")
		p1= Post.objects.create(user=u1, content="test content")

	def test_users_content(self):
		# a = Airport.objects.create(…)
		'''testing user count '''
		u= User.objects.all()
		self.assertEqual(u.count(), 1)
		# self.assertTrue(f.is_valid_flight())

	
# driver = webdriver.Chrome("/Users/owner/Downloads/ChromeDriver")


class WebPageTests(unittest.TestCase):
	
	def test_title(self):
		
		# driver = webdriver.Chrome("/Users/owner/Downloads/ChromeDriver")
		# driver.get(file_uri("network/templates/network/index.html"))
		# WebDriverWait(driver, 2000)
		driver.get("http://127.0.0.1:8000/login")
		driver.find_element_by_id("username").send_keys("dn")

		driver.find_element_by_id("password").send_keys("dn")

		driver.find_element_by_id("submit").click()
		driver.get("http://127.0.0.1:8000/following/1")
		like_button = driver.find_element_by_class_name("like")
		for i in range(10):
			like_button.click()
		driver.close()
		# self.assertEqual(driver.title, "Social Network")
		# a = Select(WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".like"))))
		# # a = driver.find_elements_by_class_name("follow")
		# for i in range(2):
		# 	for j in range(100):
		# 		print(a[i].text)
		# 		a[i].click()
		# self.assertEqual(a.text,"{{ post.content }}")
		


if __name__ == "__main__":
	unittest.main()





# network/templates/network/layout.html
