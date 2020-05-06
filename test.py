"""
THREW EVERYTHING IS IN ONE FILE FOR CONVENIENCE,
REALITY WOULD USE SOME FRAMEWORK, IM USED TO PYTHON BEHAVE AND CUCUMBER,
HONESTLY PYTHON IS VERY MESSY BUT GOOD FOR SCRIPTING AND TESTING
MY PREFERED LANGUAGE FOR TESTS BY WRITING PRODUCTION I WOULD USE SOME OTHER LANGUGAGE
USED TO USE SELENIUM WITH JUNIT AND API TESTING WITH JMETER
"""
import datetime
import logging
import time

# 3RD PARTY IMPORTS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
from urllib3.connectionpool import log as urllibLogger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# DISABLE LOGGING OF SELENIUM ETC..
urllibLogger.setLevel(logging.WARNING)
seleniumLogger.setLevel(logging.WARNING)

"""
DATES AND TIMES FOR BOOKING
REALITY WOULD NOT HARDCODE AND WOULD CALC DATES ETC
EXAMPLE LIKE BELOW AND WOULD DO SOMETHING WITH THEM

CURRENT_DATE = datetime.datetime.now()
CHECK_IN = CURRENT_DATE + datetime.timedelta(weeks=12)
CHECK_OUT = CHECK_IN + datetime.timedelta(days=3)
"""
URL = 'https://booking.com/'

TIMEOUT = 10

# PAGE OBJECT MODEL
# NORMALLY WOULD USE CLASSES AND HAVE THEM IN DIFFERENT FILES TO MAP THE OBJECTS
PAGE_HOME = {
	'SEARCH_INPUT': (By.ID, "ss"),
	'DATE_PICKER': (By.CSS_SELECTOR, ".xp__input-group:nth-child(3) .bk-icon"),
	'MONTH_NEXT_BUTTON': (By.CSS_SELECTOR, ".bui-calendar__control--next svg"),
	'SEARCH_BUTTON': (By.CSS_SELECTOR, ".sb-searchbox__button > span:nth-child(1)"),
	'DATE_1': (By.CSS_SELECTOR, ".bui-calendar__wrapper:nth-child(2) .bui-calendar__row:nth-child(2) > .bui-calendar__date:nth-child(5) > span > span"),
	'DATE_2': (By.CSS_SELECTOR, ".bui-calendar__wrapper:nth-child(2) .bui-calendar__row:nth-child(2) > .bui-calendar__date:nth-child(7) > span > span"),
	'ACCEPT': (By.CSS_SELECTOR, '.bui-button--primary > .bui-button__text'),
}

PAGE_RESULTS = {
	'SAUNA_BUTTON': (By.CSS_SELECTOR, '#filter_popular_activities .filterelement:nth-child(4) .bui-checkbox__label'),
	'SEARCH_BUTTON_2': (By.CSS_SELECTOR, '#frm > div.sb-searchbox__row.u-clearfix.-submit.sb-searchbox__footer.-last > div.sb-searchbox-submit-col.-submit-button > button')
}


# YOU PUT THE PATH TO THE BINARY HERE BASED ON BROWSER
# LOGIC NORMALLY WOULD BE TO DO PROGRAMTICALLY TO CHECK FOR PATHS ETC...
# EXAMPLE CURRENT_DIR or PATH + BIN
# CAN ADD FIREFOX OR ANOTHER BROWSER TO THE DICTIONARY
# REALITY WOULD USE SOME LIVE DEBUGGING AND NOT USE LOGS AS THIS IS VERY OLD SCHOOL

BIN_PATH = {
	'CHROME': (webdriver.Chrome, '/code/bin/chromedriver')
}


def setup():
	logging.basicConfig(level=logging.DEBUG, filename="output.log")
	logging.info('--------------------------------------------')
	logging.info('--------------------------------------------')
	logging.info('Creating instance of driver')
	browser, path = BIN_PATH['CHROME']
	driver = browser(path)
	logging.info('Created the driver instance successfully')
	driver.get(URL)
	logging.info('on url {}'.format(driver.current_url))
	return driver


def tear_down(driver):
	"""NORMALLY CHECK INSTANCE TYPE OR IS NULL BEFORE DESTORY"""
	logging.info('tearing down the driver')
	driver.quit()
	logging.info('--------------------------------------------')
	logging.info('--------------------------------------------')


def get_element_home(driver, page, identifier, text=None):
	"""
	GENERIC FUNCTION TO LOG AND FIND ELEMENTS AND ASSERT THEY ARENT NULL
	"""
	driver.implicitly_wait(TIMEOUT)

	# NEVER USE SLEEPS AND USE SOME WAIT UNTIL SHOW, OR CLICKABLE OR IS DISPLAYED ETC...

	logging.debug('looking for {} ON url {}'.format(identifier, driver.current_url))
	element = driver.find_element(*page[identifier])
	logging.debug('current value of {} is {}'.format(identifier, element))
	assert element, 'Could not locate {}'.format(identifier)
	element.click()

	if text:
		element.send_keys(text)
		assert element.get_attribute('value') == text, 'Input is not set correctly'


def test_suite(driver):
	"""
	FIRST FEW STEPS NEVER CHANGE
	AFTER THEY DO BECAUSE OF DYNAMIC ELEMENTS ON PAGE
	THESE WOULD NORMALLY GO INTO SOME FRAMEWORK AND BE CALLED ONE BY ONE BY THIS IS JUST A SOME SCRIPT
	"""
	get_element_home(driver, PAGE_HOME, 'SEARCH_INPUT', 'Limerick City')
	
	STATIC_ELEMENTS = [
		'ACCEPT', 
		'DATE_PICKER', 
		'MONTH_NEXT_BUTTON', 
		'MONTH_NEXT_BUTTON', 
		'DATE_1', 
		'DATE_2', 
		'SEARCH_BUTTON'
	]

	for x in STATIC_ELEMENTS:
		get_element_home(driver, PAGE_HOME, x)

	# ELEMENTS MAY NOT EXIST ON PAGE OR PATHS MAY CHANGE
	# BEST WOULD TO USE SOME SMART FILTER LIKE QUERY SELECTOR WITH JAVASCRIPT
	# OR A CSS SELECTOR OR ID, BUT SOMETIMES DO NOT EXIST IN SELENIUM
	# OTHER JAVASCRIPT FRAMEWORKS LIKE CYPRESS HAVE FIXED SOME FLAWS IN SELENIUM
	# BUT ALSO UP TO THE PROGRAMMER TO BE SMARTER AS WELL
	try:
		get_element_home(driver, PAGE_RESULTS, 'SAUNA_BUTTON')
	except Exception as e:
		logging.error('{}'.format(e))

	get_element_home(driver, PAGE_RESULTS, 'SEARCH_BUTTON_2')




def main():
	driver = setup()
	test_suite(driver)
	tear_down(driver)

if __name__ == '__main__':
	main()