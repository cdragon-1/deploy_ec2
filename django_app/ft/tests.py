# from django.test import LiveServerTestCase
# from selenium import webdriver
#
#
# class BaseTestCase(LiveServerTestCase):
#     def setUp(self):
#         self.browser = webdriver.Chrome()
#         self.browser.implicitly_wait(1)
#
#     def tearDown(self):
#         self.browser.quit()
#
#     def make_url(self, url):
#         return '{}{}'.format(self.live_server_url, url)
#
#
#
# class NewVisitorTest(BaseTestCase):
#     def test_show_hello_world(self):
#         self.browser.get(self.live_server_url)
#         page_text = self.browser.find_elements_by_tag_name('body').text
#         self.
