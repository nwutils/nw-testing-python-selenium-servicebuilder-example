import json
import platform
import os
import sys
import semver

from unittest import TestCase

from selenium import webdriver

from pathlib import Path

'''
NW.js Selenium test suite example
'''
class TestWindow(TestCase):

    '''
    Setup Selenium driver.
    '''
    def setUp(self):

        with open('./package.json') as f:
            pkg = json.load(f)

        dependencies = pkg.get('devDependencies', {})
        version = dependencies['nw']
        version = semver.VersionInfo.parse(version[1:])
        version = f"{version.major}.{version.minor}.{version.patch}"

        host_platform = ''
        if (sys.platform == 'linux'):
            host_platform = 'linux'
        if (sys.platform == 'win32'):
            host_platform = 'win'
        if (sys.platform == 'darwin'):
            host_platform = 'osx'

        host_arch = ''
        if (platform.machine() == 'x86_64' or platform.machine() == 'AMD64'):
            host_arch = 'x64'
        if (platform.machine() == 'i686'):
            host_arch = 'ia32'
        if (platform.machine() == 'arm64'):
            host_arch = 'arm64'

        nwjs_dir = f"nwjs-sdk-v{version}-{host_platform}-{host_arch}"
        # We are using the nw node module to download NW.js
        # Change the path as necessary
        
        chromedriver_path = Path('node_modules', 'nw', nwjs_dir, 'chromedriver')
        chromedriver_path = str(chromedriver_path.resolve())

        if sys.platform == "win32":
            chromedriver_path += ".exe"
        
        print(platform.machine())
        print(chromedriver_path)

        options = webdriver.ChromeOptions()
        # File path to NW.js project
        options.add_argument("nwapp=" + str(Path('py', 'selenium', 'service_builder').resolve()))
        # Useful if running in CI
        options.add_argument("headless=new")

        # Pass file path of NW.js chromedriver to ServiceBuilder
        service = webdriver.ChromeService(executable_path=chromedriver_path)

        # Create a new session using the Chromium options and DriverService defined above.
        self.driver = webdriver.Chrome(service=service, options=options)

    '''
    Get text via element's id and assert it is equal.
    '''
    def test_text_by_id(self):
        try:
            text_element = self.driver.find_element(webdriver.common.by.By.ID, 'test')
            text = text_element.get_attribute('innerText')
            assert(text == "Hello, World!")
        except:
            assert False

    '''
    Quit Selenium driver.
    '''
    def tearDown(self):
        self.driver.quit()
