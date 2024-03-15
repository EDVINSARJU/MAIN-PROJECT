from django.conf import settings
from django.shortcuts import render
from .models import CustomUser,UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import CustomUser
from .models import *
from reportlab.pdfgen import canvas
from thangamproject.settings import BASE_DIR

def loginview(request):
    username = request.session.get('username', None)  # Retrieve the username from the session
    return render(request, 'loginview.html', {'username': username})

 
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        gender = request.POST.get('gender')

        # Perform server-side validation as needed
        if len(username) < 3 or len(password) < 6:
            messages.error(request, 'Invalid input. Please check your username and password.')
            return redirect('register')  # Replace 'registration_page' with your actual registration page URL

        # Check if the username or email already exists
        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Username or email already exists.')
            return redirect('register')

        # Create a new user and save to the database
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            address=address,
            pincode=pincode,
            gender=gender
        )

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')  # Replace 'login' with your actual login page URL

    return render(request, 'register.html')  # Replace 'registration_page.html' with your actual registration page template

# views.py
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from .models import CustomUser  # Import your CustomUser model

@never_cache
def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                if request.user.user_type == CustomUser.CUSTOMER:
                    return redirect('/loginview')  # Redirect to the homepage
                elif request.user.user_type == CustomUser.STAFF:
                    print("user is staff")
                    return redirect('order_list')
                elif request.user.user_type == CustomUser.ADMIN:
                    print("user is admin")
                    return redirect('/adminpage')
            else:
                messages.success(request, "Invalid Username or Password.")
                return redirect('login')  # Make sure this is the correct URL for your login page

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')  # Replace 'login' with the URL name of your login page

@login_required(login_url='login')
def logview(request):
     return render(request,'loginview.html')
 
# Create your views here.
def adminpage(request):
    # Query all User objects (using the custom user model) from the database
    User = get_user_model()
    customer_users = User.objects.filter(user_type=3)    
    # Pass the data to the template
    context = {'user_profiles': customer_users}
    
    # Render the HTML template
    return render(request, 'adminpage.html', context)


def customer_list(request):
    User = get_user_model()
    customer_users = User.objects.filter(user_type=3)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_status = request.POST.get('status')
        user = User.objects.get(id=user_id)
        if new_status in ['active', 'inactive']:
            user.user_status = new_status
            user.save()
            messages.success(request, f'Status for {user.username} has been changed to {new_status}.')
        user.save()

    context = {'user_profiles': customer_users}
    return render(request, 'customer_list.html', context)

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def change_status(request, user_id):
    if request.method == 'POST':
        User = get_user_model()
        user = User.objects.get(id=user_id)
        new_status = request.POST.get('status')

        if new_status == 'active':
            # Activate the user
            user.is_active = True

            # Send an activation email
            subject = 'Account Activation'
            message = render_to_string('activation_email.html', {'user': user})
            from_email = 'mailtoshowvalidationok@gmail.com'  # Update with your email
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        elif new_status == 'inactive':
            # Deactivate the user
            user.is_active = False

            # Send a deactivation email
            subject = 'Account Deactivation'
            message = render_to_string('deactivation_email.html', {'user': user})
            from_email = 'mailtoshowvalidationok@gmail.com'  # Update with your email
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        user.save()
        messages.success(request, f'Status for {user.username} has been changed to {new_status}.')
    
    return redirect('customer_list')

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

def send_deactivation_email(user):
    subject = "Your Account Deactivation"
    from_email = "mailtoshowvalidationok@gmail.com"  # Replace with your email address
    recipient_list = [user.email]

    # Render the deactivation email template
    context = {'user': user}
    html_message = render_to_string('deactivation_email.html', context)

    # Send the email
    msg = EmailMultiAlternatives(subject, strip_tags(html_message), from_email, recipient_list)
    msg.attach_alternative(html_message, "text/html")
    msg.send()


def deactivate_user(request, user_id):
    if request.method == 'POST':
        User = get_user_model()
        user = User.objects.get(id=user_id)
        new_status = request.POST.get('status')

        if new_status == 'inactive':
            # Deactivate the user
            user.is_active = False
            user.save()

            # Send deactivation email
            send_deactivation_email(user)

    return redirect('customer_list')


from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

def send_activation_email(user):
    subject = "Your Account Activation"  # Update the subject to match activation
    from_email = "mailtoshowvalidationok@gmail.com"  # Replace with your email address
    recipient_list = [user.email]

    # Render the activation email template
    context = {'user': user}
    html_message = render_to_string('activation_email.html', context)  # Update template name

    # Send the email
    msg = EmailMultiAlternatives(subject, strip_tags(html_message), from_email, recipient_list)
    msg.attach_alternative(html_message, "text/html")
    msg.send()


def activate_user(request, user_id):  # Update the function name to be consistent
    if request.method == 'POST':
        User = get_user_model()
        user = User.objects.get(id=user_id)
        new_status = request.POST.get('status')

        if new_status == 'active':  # Update the condition to match activation
            # Activate the user
            user.is_active = True  # Update the activation action
            user.save()

            # Send activation email
            send_activation_email(user)  # Update the email function name

    return redirect('customer_list')


def contact(request):
    return render(request, 'contact.html')

def adminprofile(request):
    return render(request, 'adminprofile.html')


def delete_product(request, product_id):
    if request.method == 'POST':
        # Delete the product from the database
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return redirect('viewproduct')
        except Product.DoesNotExist:
            pass
    return redirect('viewproduct')  # Redirect back to the product list view

from .models import GoldItemNew

def add_product(request):
    if request.method == 'POST':
        # Extract data from the form
        product_name = request.POST.get('product-name')
        category = request.POST.get('category-name')
        subcategory = request.POST.get('subcategory-name')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        price = float(request.POST.get('price', 0))
        discount = float(request.POST.get('discount', 0))
        status = request.POST.get('status')
        product_image = request.FILES.get('product-image')
        making_charge = float(request.POST.get('making-charge', 0))
        gold_value = float(request.POST.get('gold-value', 0))
        stone_cost = float(request.POST.get('stone-cost', 0))
        gst_rate = float(request.POST.get('gst-rate', 0))
        gold_weight = float(request.POST.get('gold-weight', 0))
        volume = float(request.POST.get('volume', 1.0))  # Retrieve volume from the form, default to 1.0 if not provided

        # Calculate discounted price
        discounted_price = price - (price * (discount / 100))

        # Calculate sale_price
        sale_price = discounted_price + making_charge + (gold_value * gold_weight) + stone_cost

        # Calculate estimated purity
        known_density = 19.32  # Known density of pure gold (in g/cm^3)
        density = gold_weight / volume
        estimated_purity = (density / known_density) * 100

        # Save product data
        product = Product(
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            quantity=quantity,
            description=description,
            status=status,
            product_image=product_image,
            price=price,
            discount=discount,
            making_charge=making_charge,
            gold_value=gold_value,
            stone_cost=stone_cost,
            gst_rate=gst_rate,
            sale_price=sale_price,
            gold_weight=gold_weight,
            estimated_purity=estimated_purity
        )

        # Calculate purity of gold and save it
        if estimated_purity:
            if estimated_purity >= 95:
                product.purity_of_gold = '24k'
            elif estimated_purity >= 91:
                product.purity_of_gold = '22k'
            else:
                product.purity_of_gold = '18k'

        product.save()

        # Save gold item data
        gold_item = GoldItemNew(
            product=product,  # Assign the product to the gold item
            weight=gold_weight,
            volume=volume,
            calculated_purity=estimated_purity  # Save the calculated purity
        )
        gold_item.save()

        return redirect('adminpage')  # Redirect to admin page after successful addition

    return render(request, 'adminpage.html')



def view_product(request):
    products = Product.objects.all()  # Retrieve all products from the database
    return render(request, 'viewproduct.html', {'products': products})

from django.shortcuts import render, get_object_or_404
from .models import Product
from django.http import JsonResponse

def product_grid(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def adminpage(request):
    # Query all User objects (using the custom user model) from the database
    User = get_user_model()
    customer_users = User.objects.filter(user_type=3)    
    # Pass the data to the template
    context = {'user_profiles': customer_users}
    
    # Render the HTML template
    return render(request, 'adminpage.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm

@login_required
def profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {'user': user, 'user_profile': user_profile, 'form': form})

from .models import Product

def featured_product(request):
    products = Product.objects.all()
    return render(request, 'loginview.html', {'products': products})



from django.shortcuts import render, redirect
from .models import Product

def edit_product(request, product_id):
    # Retrieve the product based on the product_id
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        try:
            # Handle the form submission
            product.product_name = request.POST.get('product-name')
            product.category = request.POST.get('category-name')
            product.subcategory = request.POST.get('subcategory-name')
            product.quantity = request.POST.get('quantity')
            product.description = request.POST.get('description')
            product.price = float(request.POST.get('price', 0))
            product.discount = float(request.POST.get('discount', 0))
            product.status = request.POST.get('status')
            product_image = request.FILES.get('product-image')

            # Only update the product image if a new image is provided
            if product_image:
                product.product_image = product_image

            product.making_charge = float(request.POST.get('making-charge', 0))
            product.gold_value = float(request.POST.get('gold-value', 0))
            product.gold_weight = float(request.POST.get('gold-weight', 0))  # Add this line for gold weight
            product.stone_cost = float(request.POST.get('stone-cost', 0))
            product.gst_rate = float(request.POST.get('gst-rate', 0))

            # Retrieve the purity of gold
            product.purity_of_gold = request.POST.get('purity-of-gold')

            # Calculate sale price
            product.calculate_sale_price()

            # Save the updated product to the database
            product.save()

            # Redirect to a success page or any other desired action
            return redirect('adminpage')

        except Exception as e:
            # Print the exception for debugging
            print(f"An error occurred: {e}")

    return render(request, 'edit_product.html', {'product': product})






from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ShoppingCart

@login_required
def view_cart(request, product_id=None):
    cart_items = ShoppingCart.objects.filter(user=request.user)

    total_price = calculate_total_price(cart_items)
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_quantity = request.POST.get('new_quantity')

        # Update the quantity in the database
        cart_item = ShoppingCart.objects.get(id=item_id)
        cart_item.quantity = new_quantity
        cart_item.save()

        # Redirect back to the cart page
        return redirect('view_cart')

    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


def calculate_total_price(cart_items):
    total_price = 0
    for item in cart_items:
        total_price += item.product.sale_price * item.quantity
    return total_price












from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ShoppingCart

def remove_from_cart(request, item_id):
    # Get the shopping cart item or raise a 404 error if not found
    cart_item = get_object_or_404(ShoppingCart, id=item_id, user=request.user)

    # Delete the item from the cart
    cart_item.delete()

    # Redirect to the shopping cart page after removing the item
    messages.success(request, 'Item removed from the cart.')
    return redirect('view_cart', product_id=cart_item.product.product_id)




from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product, ShoppingCart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user

        # Check if the product is already in the user's cart
        cart_item, created = ShoppingCart.objects.get_or_create(user=user, product=product)

        # No need to increment quantity, just add the product to the cart
        if created:
            messages.success(request, 'Item added to the cart.')
        else:
            messages.warning(request, 'Item is already in the cart.')

        return redirect('view_cart', product_id=product_id)
    else:
        messages.warning(request, 'Please log in to add items to your cart.')
        return redirect('login')  # Redirect to the login page if the user is not authenticated






from django.shortcuts import render, redirect
from .models import Category, Subcategory

def load_add_product_form(request):
    categories = Category.objects.all()
    return render(request, 'your_template.html', {'categories': categories})


from django.shortcuts import render
from .models import Category, Subcategory

def category_view(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})

def subcategory_view(request):
    subcategories = Subcategory.objects.all()
    return render(request, 'subcategory.html', {'subcategories': subcategories})




from django.shortcuts import render, redirect
from .models import Feedback

def feedback_submit(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        feedback = Feedback.objects.create(
            username=username,
            email=email,
            subject=subject,
            message=message
        )
        # Optionally, you can add some logic here such as sending a confirmation email or redirecting to a thank you page.
        return redirect('contact')  # Replace 'thank_you_page' with the name of your thank you page URL
    else:
        # Handle GET request if needed
        pass


from django.shortcuts import render
from .models import Feedback

def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})

from django.shortcuts import render
from .models import UserProfile

def staff_list(request):
   User = get_user_model()
   staff_members = User.objects.filter(user_type=2)
   context = {'staff_members': staff_members}
   return render(request, 'staff_list.html', context)





def change_staff_status(request, staff_id):
    User = get_user_model()

    if request.method == 'POST':
        new_status = request.POST.get('status')
        staff_member = User.objects.get(id=staff_id)

        if new_status == 'active':
            staff_member.is_active = True
            messages.success(request, f'{staff_member.username} is now active.')
        elif new_status == 'inactive':
            staff_member.is_active = False
            messages.success(request, f'{staff_member.username} is now inactive.')

        staff_member.save()

    return redirect('staff_list')


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

def change_staff_status(request, staff_id):
    if request.method == 'POST':
        User = get_user_model()
        try:
            staff = User.objects.get(id=staff_id)
        except User.DoesNotExist:
            messages.error(request, "Staff member does not exist.")
            return redirect('staff_list')

        new_status = request.POST.get('status')

        if new_status == 'active':
            # Activate the staff member
            staff.is_active = True

            # Send an activation email
            subject = 'Staff Account Activation'
            message = render_to_string('activation_email.html', {'user': staff})
            from_email = 'mailtoshowvalidationok@gmail.com'  # Update with your email
            recipient_list = [staff.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        elif new_status == 'inactive':
            # Deactivate the staff member
            staff.is_active = False

            # Send a deactivation email
            subject = 'Staff Account Deactivation'
            message = render_to_string('deactivation_email.html', {'user': staff})
            from_email = 'mailtoshowvalidationok@gmail.com'  # Update with your email
            recipient_list = [staff.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        staff.save()
        messages.success(request, f'Status for {staff.username} has been changed to {new_status}.')
    
    return redirect('staff_list')

def send_activation_email(user):
    subject = "Your Account Activation"
    from_email = "mailtoshowvalidationok@gmail.com"
    recipient_list = [user.email]

    # Render the activation email template
    context = {'user': user}
    html_message = render_to_string('activation_email.html', context)

    # Send the email
    send_mail(subject, strip_tags(html_message), from_email, recipient_list, html_message=html_message)

def send_deactivation_email(user):
    subject = "Your Account Deactivation"
    from_email = "mailtoshowvalidationok@gmail.com"
    recipient_list = [user.email]

    # Render the deactivation email template
    context = {'user': user}
    html_message = render_to_string('deactivation_email.html', context)

    # Send the email
    send_mail(subject, strip_tags(html_message), from_email, recipient_list, html_message=html_message)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def update_customer_info(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone')
        user.pincode = request.POST.get('pincode')
        user.address = request.POST.get('address')
        user.save()
        messages.success(request, 'Your information has been updated successfully.')
        return redirect('loginview')  # Redirect to the user's profile page
    else:
        return redirect('loginview')  # Redirect to home if accessed via GET request
    
    
    
    
from django.shortcuts import render
from .models import CustomUser

def order_list(request):
    # Retrieve customers
    customers = CustomUser.objects.filter(user_type=CustomUser.CUSTOMER)
    return render(request, 'order_list.html', {'customers': customers})






    
    

from django.shortcuts import render
from django.http import HttpResponse
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Define the path to your dataset file
DATASET_PATH = 'D:/new product db update/thangamproject/gold_purity_dataset.csv'

# Define the path to save the trained model
MODEL_PATH = 'D:/new product db update/thangamproject/trained_model.pkl'

def train_model():
    try:
        # Load dataset
        df = pd.read_csv(DATASET_PATH)

        # Split data into features (X) and target (y)
        X = df[['Chemical_Composition', 'Density']]
        y = df['Purity']

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Save the trained model
        joblib.dump(model, MODEL_PATH)
        return True
    except Exception as e:
        print(f"Error training model: {e}")
        return False




def purity(request):
    if request.method == 'POST':
        # Get user inputs from the form
        chemical_composition = request.POST.get('chemical_composition')
        density = request.POST.get('density')
        
        # Train the model if it's not already trained
        if not os.path.exists(MODEL_PATH):
            if not train_model():
                return HttpResponse("Error training model. Please try again.")
        
        try:
            # Load the trained model
            model = joblib.load(MODEL_PATH)
            
            # Make predictions using the model
            predicted_purity = model.predict([[float(chemical_composition), float(density)]])[0]
            
            # Render HTML template with predicted purity
            return render(request, 'result.html', {'predicted_purity': predicted_purity})
        except Exception as e:
            return HttpResponse(f"Error making predictions: {e}")
    else:
        return render(request, 'purity.html')



def calculate_purity(request):
    if request.method == 'POST':
        weight = float(request.POST.get('weight'))
        volume = float(request.POST.get('volume'))
        density = weight / volume
        # Known density of pure gold (in g/cm^3)
        known_density = 19.32
        # Estimate purity based on density comparison
        estimated_purity = (density / known_density) * 100
        
        # Save the GoldItem to the database
        gold_item = GoldItemNew.objects.create(weight=weight, volume=volume)
        gold_item.save()
        
        return render(request, 'result.html', {'estimated_purity': estimated_purity})
    else:
        return render(request, 'calculate_purity.html')

    
    
  

def golditem_list(request):
    # Retrieve all GoldItemNew objects from the database
    gold_items = GoldItemNew.objects.all()

    # Pass gold_items queryset to the template context
    return render(request, 'calculate_purity.html', {'gold_items': gold_items})



from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.template.loader import render_to_string
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(request, gold_item_id):
    gold_item = get_object_or_404(GoldItemNew, pk=gold_item_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="gold_item_details_{gold_item_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    gold_item_details = [
        ["Product Name", gold_item.product.product_name],
        ["Weight", gold_item.weight],
        ["Volume", gold_item.volume],
        ["Calculated Purity (%)", gold_item.calculated_purity],
        
    ]

    table = Table(gold_item_details)

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)
    elements.append(table)


    doc.build(elements)

    return response


    
def product_details(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'product_details.html', {'product': product})

from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def product_pdf(request, gold_item_id):
    gold_item = get_object_or_404(GoldItemNew, pk=gold_item_id)
    product = gold_item.product 

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="gold_item_details_{gold_item_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=inch/2, leftMargin=inch/2, topMargin=inch/2, bottomMargin=inch/2)
    elements = []

    header_text = '<font size="24" color="red"><b>THANGAM JEWELLERY</b></font>'
    header_style = getSampleStyleSheet()['Title']
    header_paragraph = Paragraph(header_text, header_style)
    elements.append(header_paragraph)
 
    elements.append(Spacer(1, 24))  

    product_image = Image(product.product_image.path, width=100, height=100)
    elements.append(product_image)

    elements.append(Spacer(1, 12))  

    product_details = [
        ["Product Name", product.product_name],
        ["Gold Weight", f"{gold_item.weight} Grams"],
        ["Purity of Gold", product.purity_of_gold],
        ["Volume", gold_item.volume],
        ["Estimated Purity (%)", f"{product.estimated_purity}%"],
    ]
    details_table = Table(product_details, style=[
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONT_SIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
    ])
    elements.append(details_table)
    elements.append(Spacer(1, 12)) 

    description_text = """
    <b>Gold Weight:</b><br/>
    Refers to the mass of the gold, typically measured in grams (g) or ounces (oz).<br/>
    The weight of gold determines its value, with heavier pieces generally being more valuable.<br/>
    Used in calculations to determine the overall value of gold items.<br/><br/>

    <b>Purity of Gold:</b><br/>
    Denoted in karats (K) or fineness, indicating the proportion of pure gold in an alloy.<br/>
    Common purities include 24K (99.9% pure), 22K (91.7% pure), and 18K (75% pure), among others.<br/>
    Higher purity gold typically has a brighter yellow color and is more valuable but may also be softer and less durable.<br/><br/>

    <b>Volume of Gold:</b><br/>
    Represents the space occupied by the gold, measured in cubic centimeters (cm³) or milliliters (ml).<br/>
    Determined by measuring the length, width, and height of the gold object or by displacement in a liquid.<br/>
    Used in density calculations to estimate purity when combined with weight.<br/><br/>

    <b>Estimated Purity (%):</b><br/>
    Calculated based on the gold's weight, volume, and density.<br/>
    Provides an approximation of the gold's purity, often expressed as a percentage.<br/>
    Helpful for assessing the value and quality of gold items, especially when purity testing methods are unavailable or impractical.<br/>
    """
    description_box = Paragraph(description_text, getSampleStyleSheet()['Normal'])
    elements.append(description_box)

    # Build the PDF
    doc.build(elements)

    return response













from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from razorpay import Client
from .models import ShoppingCart, RazorpayPayment  # Import RazorpayPayment model

razorpay_api_key = settings.RAZORPAY_API_KEY
razorpay_secret_key = settings.RAZORPAY_API_SECRET

razorpay_client = Client(auth=(razorpay_api_key, razorpay_secret_key))

@csrf_exempt
def rentnxt(request):
    cart_items_data = request.POST.getlist('cart_items[]')
    user = request.user

    for item_data in cart_items_data:
        product_id = int(item_data)
        product = Product.objects.get(pk=product_id)
        total_price = product.sale_price
        # Create a RazorpayPayment instance instead of OrderedProduct
        RazorpayPayment.objects.create(
            user=user,
            product=product,
            total_price=total_price
        )
    
    cart_items = ShoppingCart.objects.filter(user=request.user)
    total_price = calculate_total_price(cart_items)

    amount = int(total_price * 100)

    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    order = razorpay_client.order.create(data=order_data)
    callback_url = 'paymenthandler/'

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
        'callback_url' : callback_url
    }
    
    return render(request, 'payment.html', context)

from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import RazorpayPayment  # Import RazorpayPayment model

@csrf_exempt
def paymenthandler(request):
    # Only accept POST request.
    if request.method == "POST":
        try:
            # Get the required parameters from the post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                try:
                    # Capture the payment.
                    razorpay_client.payment.capture(payment_id)

                    # Fetch the cart items from the session or database, and create RazorpayPayment instances.
                    cart_items = ShoppingCart.objects.filter(user=request.user)
                    for cart_item in cart_items:
                        RazorpayPayment.objects.create(
                            user=request.user,
                            product=cart_item.product,
                            total_price=cart_item.total_price
                        )
                        # Optionally, you can remove the cart items from the database or session.
                        cart_item.delete()

                    # Redirect to the payment success page.
                    return render(request, 'payment_success.html')
                except:
                    # If there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
                # If signature verification fails.
                return render(request, 'paymentfail.html')
        except:
            # If the required parameters are not found in POST data.
            return HttpResponseBadRequest()
    else:
        # If other than POST request is made.
        return HttpResponseBadRequest()




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import RazorpayPayment  # Import RazorpayPayment model

@login_required
def process_payment(request):
    if request.method == 'POST':
        # Fetch the order associated with the current user
        order = RazorpayPayment.objects.filter(user=request.user).first()
        if order:
            # Update the order status or perform any necessary action
            order.status = 'PAID'  # For example, updating the order status
            order.save()
            return redirect('order_confirmation')  # Redirect to the order confirmation page
    return render(request, 'payment_fail.html') 


from django.shortcuts import render
from .models import RazorpayPayment

def payment_success(request):
    if request.method == 'POST':
        try:
            
            razorpay_payments = RazorpayPayment.objects.filter(user=request.user)

            context = {
                'razorpay_payments': razorpay_payments,
            }
            return render(request, 'payment_success.html', context)
        except Exception as e:
            print(e)
            return render(request, 'payment_fail.html')
    else:
        return HttpResponseBadRequest()
