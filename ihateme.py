import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import urllib2
import urllib
import os
loggedIn=False

driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://if188.infusionsoft.com/")
elem = driver.find_element_by_id('username')
elem.send_keys(pw["username"])
elem = driver.find_element_by_id('password')
elem.send_keys(pw["password"])
elem.send_keys(Keys.RETURN)
driver.get('https://if188.infusionsoft.com/Import/jumpToWizard.jsp?update=false&profileClass=com.infusion.crm.db.importer.profiles.ROrderProfile')
driver.find_element_by_id("importFile").send_keys("/home/jlmarks/importme.csv")
driver.find_element_by_id("Submit").click()
driver.find_element_by_id("Submit").click()
driver.find_element_by_id("Submit").click()
driver.find_element_by_id("Submit").click()
