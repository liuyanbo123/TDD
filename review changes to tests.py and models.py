[1mdiff --git a/functional_tests.py b/functional_tests.py[m
[1mindex 2c8debe..167568c 100644[m
[1m--- a/functional_tests.py[m
[1m+++ b/functional_tests.py[m
[36m@@ -7,12 +7,16 @@[m [mclass NewVisitorTest(unittest.TestCase):                #(1)[m
 		self.browser = webdriver.Chrome()[m
 [m
 	def tearDown(self):[m
[31m-		self.browser.quit()  [m
[32m+[m		[32mself.browser.quit()[m
[32m+[m	[32mdef check_for_row_in_list_table(self, row_text):[m
[32m+[m		[32mtable = self.browser.find_element_by_id('id_list_table')[m
[32m+[m		[32mrows = table.find_elements_by_tag_name('tr')[m
[32m+[m		[32mself.assertIn(row_text, [row.text for row in rows])[m[41m  [m
 [m
 	def test_can_start_a_list_and_retrieve_it_later(self):                       [m
[31m-[m
 		#Edith has heard about a cool new online to-do app. She goes[m
 		#to check out its homepage[m
[32m+[m		[32m#不能改[m
 		self.browser.get('http://localhost:8000')      [m
 [m
 		#She notices the page title and header mention to-do lists[m
[36m@@ -26,26 +30,39 @@[m [mclass NewVisitorTest(unittest.TestCase):                #(1)[m
 			inputbox.get_attribute('placeholder'),[m
 			'Enter a to-do item'[m
 			)[m
[32m+[m		[32m#不能改[m
 [m
 		#She types "Buy peacock feathers" into a text box (Edith's hobby[m
 		#is tying fly-fishing lures)[m
[31m-		inputbox.send_keys('Buy peacock feathers')[m
[32m+[m[32m#		inputbox.send_keys('Use peacock feathers to make a fly')[m
 [m
 		#when she hits enter, the page updates, and now the page lists[m
 		#"1: Buy peacock feathers" as an item in a to-do list[m
[32m+[m		[32minputbox.send_keys('Buy peacock feathers')[m
 		inputbox.send_keys(Keys.ENTER)[m
 		time.sleep(1)[m
[32m+[m		[32mself.check_for_row_in_list_table('1: Buy peacock feathers')[m
 [m
[31m-		table = self.browser.find_element_by_id('id_list_table')[m
[31m-		rows = table.find_elements_by_tag_name('tr')[m
[31m-		self.assertTrue([m
[31m-			any(row.text == '1: Buy peacock feathers' for row in rows),[m
[31m-			"New to-do item did not appear in table"[m
[31m-			)[m
[32m+[m[32m#		self.assertTrue([m
[32m+[m[32m#			any(row.text == '1: Buy peacock feathers' for row in rows),[m
[32m+[m[32m#			f"New to-do item did not appear in table. Contents were:\n{table.text}"[m
[32m+[m[32m#			)   不要，用assertIn[m
 [m
 		#There is still a text box inviting her to add another item. She[m
 		#enters "Use peacock feathers to make a fly"(Edith is very methodical)[m
[31m-		self.fail('Finish the test!')[m
[32m+[m		[32m#[m
[32m+[m		[32minputbox = self.browser.find_element_by_id('id_new_item')[m
[32m+[m		[32minputbox.send_keys('Use peacock feathers to make a fly')[m
[32m+[m		[32minputbox.send_keys(Keys.ENTER)[m
[32m+[m		[32mtime.sleep(1)[m
[32m+[m		[32m#[m
[32m+[m[32m#		self.assertIn('1: Buy peacock feathers', [row.text for row in rows])[m
[32m+[m[32m#		self.assertIn([m
[32m+[m[32m#			'2: Use peacock feathers to make a fly',[m
[32m+[m[32m#			[row.text for row in rows][m
[32m+[m[32m#			) 换成用一个方法代替check_for_row_in_list_table[m
[32m+[m		[32mself.check_for_row_in_list_table('1: Buy peacock feathers')[m
[32m+[m		[32mself.check_for_row_in_list_table('2: Use peacock feathers to make a fly')[m
 [m
 		#The page updates again, and now shows both items on her list[m
 [m
[36m@@ -55,5 +72,6 @@[m [mclass NewVisitorTest(unittest.TestCase):                #(1)[m
 [m
 		#She visits that URL - her to-do list is still there.[m
 		#Satisfied, she goes back to sleep[m
[32m+[m		[32mself.fail('Finish the test!')[m
 if __name__ == '__main__':[m
 	unittest.main()[m
\ No newline at end of file[m
[1mdiff --git a/lists/models.py b/lists/models.py[m
[1mindex 71a8362..c8fa297 100644[m
[1m--- a/lists/models.py[m
[1m+++ b/lists/models.py[m
[36m@@ -1,3 +1,7 @@[m
 from django.db import models[m
 [m
[32m+[m[32mclass Item(models.Model):[m
[32m+[m	[32mtext = models.TextField(default='')[m
[32m+[m
[32m+[m
 # Create your models here.[m
[1mdiff --git a/lists/tests.py b/lists/tests.py[m
[1mindex 9c5594a..8b723d4 100644[m
[1m--- a/lists/tests.py[m
[1m+++ b/lists/tests.py[m
[36m@@ -3,6 +3,7 @@[m [mfrom django.test import TestCase[m
 from django.http import HttpRequest[m
 #from django.template.loader import render_to_string[m
 from lists.views import home_page[m
[32m+[m[32mfrom lists.models import Item[m
 [m
 class HomePageTest(TestCase):[m
 	def test_root_url_resolve_to_home_page_view(self):[m
[36m@@ -23,5 +24,28 @@[m [mclass HomePageTest(TestCase):[m
 #		self.assertTrue(html.strip().endswith('</html>'))[m
 [m
 		self.assertTemplateUsed(response, 'home.html')[m
[32m+[m	[32mdef test_can_save_a_POST_request(self):[m
[32m+[m		[32mresponse = self.client.post('/', data={'item_text': 'A new list item'})[m
[32m+[m		[32mself.assertIn('A new list item', response.content.decode())[m
[32m+[m		[32mself.assertTemplateUsed(response, 'home.html')[m
[32m+[m
[32m+[m[32mclass ItemModelTest(TestCase):[m
[32m+[m
[32m+[m	[32mdef test_saving_and_retrieving_items(self):[m
[32m+[m		[32mfirst_item = Item()[m
[32m+[m		[32mfirst_item.text = 'The first (ever) list item'[m
[32m+[m		[32mfirst_item.save()[m
[32m+[m
[32m+[m		[32msecond_item = Item()[m
[32m+[m		[32msecond_item.text = 'Item the second'[m
[32m+[m		[32msecond_item.save()[m
[32m+[m
[32m+[m		[32msaved_items = Item.objects.all()[m
[32m+[m		[32mself.assertEqual(saved_items.count(), 2)[m
[32m+[m
[32m+[m		[32mfirst_saved_item = saved_items[0][m
[32m+[m		[32msecond_saved_item = saved_items[1][m
[32m+[m		[32mself.assertEqual(first_saved_item.text, 'The first (ever) list item')[m
[32m+[m		[32mself.assertEqual(second_saved_item.text, 'Item the second')[m
 [m
 # Create your tests here.[m
[1mdiff --git a/lists/views.py b/lists/views.py[m
[1mindex 5f0b859..48d9d32 100644[m
[1m--- a/lists/views.py[m
[1m+++ b/lists/views.py[m
[36m@@ -1,6 +1,9 @@[m
[31m-#from django.shortcuts import render[m
[31m-#from django.http import HttpResponse[m
[32m+[m[32mfrom django.http import HttpResponse[m
 # Create your views here.[m
 from django.shortcuts import render[m
 def home_page(request):[m
[31m-	return render(request,'home.html')[m
\ No newline at end of file[m
[32m+[m[32m#	if request.method == 'POST':[m
[32m+[m[32m#		return HttpResponse(request.POST['item_text'])[m
[32m+[m	[32mreturn render(request, 'home.html',{[m
[32m+[m		[32m'new_item_text': request.POST.get('item_text', ''),[m
[32m+[m		[32m})[m
