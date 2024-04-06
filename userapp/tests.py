

def test_login(self):
        # Replace the following lines with the actual login logic using Selenium
        self.selenium.get(self.live_server_url)  # Replace with your login page URL
        username_input = self.selenium.find_element_by_id('benz')
        password_input = self.selenium.find_element_by_id('Benz@123')

        # Fill in the login form
        username_input.send_keys('benz')
        password_input.send_keys('Benz@123')

        # Submit the form (replace with your submit button or form submission logic)
        password_input.submit()

        # Replace this with assertions that validate the successful login
        self.assertIn('Welcome', self.selenium.page_source)
        
        
        
        
        
   
   
   
from django.test import TestCase
from django.urls import reverse
from userapp.models import CustomUser  # Import your CustomUser model

class HomePageTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='benz',
            password='Benz@123'
        )

    def test_homepage_view_status_code(self):
        # Use the reverse function to get the URL for the loginview
        url = reverse('loginview')  # Replace 'loginview' with the actual name of your loginview URL pattern

        # Make a GET request to the loginview
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_homepage_view_with_authenticated_user(self):
        # Log in the test user
        self.client.login(username='benz', password='Benz@123')

        # Use the reverse function to get the URL for the loginview
        url = reverse('loginview')  # Replace 'loginview' with the actual name of your loginview URL pattern

        # Make a GET request to the loginview
        response = self.client.get(url)

        # Check that the response status code is 200 (OK) for an authenticated user
        self.assertEqual(response.status_code, 200)

        # Check that the username is present in the response content
        self.assertContains(response, self.user.username)

    def test_homepage_view_with_unauthenticated_user(self):
        # Use the reverse function to get the URL for the loginview
        url = reverse('loginview')  # Replace 'loginview' with the actual name of your loginview URL pattern

        # Make a GET request to the loginview
        response = self.client.get(url)

        # Check that the response status code is 200 (OK) for an unauthenticated user
        self.assertEqual(response.status_code, 200)

        # Check that the login link is present in the response content
        self.assertContains(response, 'Login')



from django.test import TestCase

class HomePageTests(TestCase):
    def test_homepage_view_status_code(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/')  # Change '/login/' to your actual login URL



class HomePageTests(TestCase):
    def test_homepage_view_with_authenticated_user(self):
        self.client.login(username='benz', password='Benz@123')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        







from django.test import TestCase, Client
from django.urls import reverse
from .models import Product

class AddProductViewTest(TestCase):
    def setUp(self):
        # Initialize the client
        self.client = Client()

    def test_add_product_view(self):
        # Your test data
        form_data = {
            'product-name': 'Leaf Motif Stone Encrusted diamond',
            'category-name': 'diamond',
            'subcategory-name': 'rings',
            'quantity': '1',
            'description': 'Diamonds are highly coveted gemstones known for their exceptional brilliance and hardness, symbolizing enduring love and luxury.',
            'price': '40987.00',
            'discount': '1.00',
            'status': 'Active',
            'making-charge': '50.00',
            'gold-value': '15.00',
            'stone-cost': '14.00',
            'gst-rate': '18.00',
            'gold-weight': '7.00',
            'purity-of-gold': '18K',
            # Include any other form fields as needed
        }

        # Get the URL for the add_product view
        url = reverse('add_product')

        # Make a POST request with the form data
        response = self.client.post(url, form_data, format='multipart')

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the product is created in the database
        self.assertEqual(Product.objects.count(), 1)

        # Retrieve the created product
        created_product = Product.objects.first()

        # Check that the product attributes match the form data
        self.assertEqual(created_product.product_name, 'Leaf Motif Stone Encrusted diamond')
        self.assertEqual(created_product.category, 'diamond')
        self.assertEqual(created_product.subcategory, 'rings')
        # Add more attribute checks as needed

        # Redirect to a success page or any other desired action
        self.assertRedirects(response, reverse('adminpage'))




from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product

class EditProductViewTest(TestCase):
    def setUp(self):
        # Create a user for testing (if needed)
        self.user = get_user_model().objects.create_user(username='benz', password='Benz@123')

        # Create a product for testing
        self.product = Product.objects.create(
            product_name='Leaf Motif Stone Encrusted diamond',
            category='gold',
            subcategory='necklace',
            quantity=10,
            description='Diamonds are highly coveted gemstones known for their exceptional brilliance and hardness, symbolizing enduring love and luxury.',
            discount=10,
            price=100.0,
            making_charge=20.0,
            gold_value=80.0,
            gold_weight=5.0,
            stone_cost=10.0,
            gst_rate=5,
            sale_price=90.0,
            status='active',
        )

def test_edit_product_view(self):
    # If your view requires authentication, you can use self.client.login
    # self.client.login(username='testuser', password='testpassword')

    # Get the URL for the edit_product view, providing the product_id
    url = reverse('edit_product', kwargs={'product_id': self.product.product_id})  # Replace 'id' with your actual primary key field name

    # Make a GET request to the edit_product view
    response = self.client.get(url)

    # Check that the response status code is 200 (OK)
    self.assertEqual(response.status_code, 200)

    # Check that the product details are present in the response content
    self.assertContains(response, 'Edit Product')
    self.assertContains(response, self.product.product_name)
    self.assertContains(response, f'value="{self.product.category}" selected')
    self.assertContains(response, f'value="{self.product.subcategory}" selected')
    self.assertContains(response, f'value="{self.product.purity_of_gold}" selected')
    self.assertContains(response, f'value="{self.product.quantity}"')
    self.assertContains(response, self.product.description)
    self.assertContains(response, f'value="{self.product.price}"')
    self.assertContains(response, f'value="{self.product.discount}"')
    self.assertContains(response, f'value="{self.product.making_charge}"')
    self.assertContains(response, f'value="{self.product.gold_value}"')
    self.assertContains(response, f'value="{self.product.gold_weight}"')
    self.assertContains(response, f'value="{self.product.stone_cost}"')
    self.assertContains(response, f'value="{self.product.gst_rate}"')
    self.assertContains(response, f'value="{self.product.sale_price}"')
    self.assertContains(response, f'value="{self.product.status}"')
    
    # If your view requires authentication, you can use self.client.logout
    # self.client.logout()






from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class CustomerListViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='admin'
        )

    # ... rest of your test cases ...

def test_customer_list_view(self):
    # Login the test user
    self.client.login(username='admin', password='admin')

    # Access the customer list view
    response = self.client.get(reverse('customer_list'))

    # Check if the view returns a 200 status code
    self.assertEqual(response.status_code, 200)

    # Check if the rendered template is correct
    self.assertTemplateUsed(response, 'loginview.html')

    # Check if the user's information is present in the rendered HTML
    self.assertContains(response, 'admin')
    # Update the email to match the one you expect
    self.assertContains(response, 'edvin@gmail.com')

def test_customer_list_view_unauthenticated(self):
    # Logout the test user
    self.client.logout()

    # Access the customer list view without authentication
    response = self.client.get(reverse('customer_list'))

    # Check if the view redirects to the login page
    self.assertEqual(response.status_code, 302)  # Ensure it's a redirect
    # Update the URL to match your project structure
    expected_redirect_url = reverse('login') + f'?next={reverse("customer_list")}'
    self.assertRedirects(response, expected_redirect_url)














from selenium.webdriver.common.by import By
import time

def test_submit_contact_form(self):
    # Find the form fields by their names
    username_input = self.driver.find_element(By.NAME, "username")  # Assuming "username" is the name attribute of the username input field
    email_input = self.driver.find_element(By.NAME, "email")  # Assuming "email" is the name attribute of the email input field
    subject_input = self.driver.find_element(By.NAME, "subject")  # Assuming "subject" is the name attribute of the subject input field
    message_input = self.driver.find_element(By.NAME, "message")  # Assuming "message" is the name attribute of the message input field

    # Fill in the form with test data
    username_input.send_keys("benz")
    email_input.send_keys("benzbaby2024a@mca.ajce.in")
    subject_input.send_keys("ytjfhn")
    message_input.send_keys("12345678")

    # Submit the form by clicking the submit button
    send_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
    send_button.click()

    # Wait for the page to load after form submission
    time.sleep(2)

    # Check if the success message is displayed in the page source
    self.assertIn("Thank you for your message", self.driver.page_source)





def test_payment_page(self):
        # Navigate to the payment page
        payment_link = self.driver.find_element(By.XPATH, "//a[@href='#payment']")
        payment_link.click()
        time.sleep(2)

        # Verify if the payment page is displayed
        self.assertIn("Payment", self.driver.title)

        # Verify if payment details are visible
        payment_id = self.driver.find_element(By.NAME, "payment_id")
        razorpay_payment_id = self.driver.find_element(By.NAME, "razorpay_payment_id")
        product_name = self.driver.find_element(By.NAME, "The Beauty and Brilliance ")
        product_image = self.driver.find_element(By.NAME, "")
        price = self.driver.find_element(By.NAME, "2001")
        date = self.driver.find_element(By.NAME, "03/03/2023")
        total_price = self.driver.find_element(By.NAME, "21001")
        generate_pdf_button = self.driver.find_element(By.XPATH, "//button[@id='generate_pdf']")

        self.assertTrue(payment_id.is_displayed())
        self.assertTrue(razorpay_payment_id.is_displayed())
        self.assertTrue(product_name.is_displayed())
        self.assertTrue(product_image.is_displayed())
        self.assertTrue(price.is_displayed())
        self.assertTrue(date.is_displayed())
        self.assertTrue(total_price.is_displayed())
        self.assertTrue(generate_pdf_button.is_displayed())

        # Generate PDF bill
        generate_pdf_button.click()
        time.sleep(2)

        # Check if the PDF bill is generated successfully
        self.assertIn("PDF Bill", self.driver.page_source)