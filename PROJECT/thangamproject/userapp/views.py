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

# views.py

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
                    # return redirect(reverse('therapist'))
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




def staff_list(request):
    staff_members = UserProfile.objects.filter(user__user_type=2)  # Filter for staff members
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



def add_product(request):
    if request.method == 'POST':
        # Handle the form submission
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
        gold_weight = float(request.POST.get('gold-weight', 0))  # Fetch gold_weight from the form

        # Calculate discounted price
        discounted_price = price - (price * (discount / 100))

        # Calculate sale_price
        sale_price = discounted_price + making_charge + (gold_value * gold_weight) + stone_cost  # Include gold_weight in the calculation

        # Calculate GST amount
        gst_amount = sale_price * (gst_rate / 100)

        # Calculate sale_price_with_gst
        sale_price_with_gst = sale_price + gst_amount

        # Retrieve the purity of gold
        purity_of_gold = request.POST.get('purity-of-gold')

        # Create a new Product object and save it to the database
        product = Product(
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            quantity=quantity,
            description=description,
            price=price,
            discount=discount,
            sale_price=sale_price_with_gst,
            status=status,
            product_image=product_image,
            purity_of_gold=purity_of_gold,
            making_charge=making_charge,
            gold_value=gold_value,
            stone_cost=stone_cost,
            gst_rate=gst_rate,
            gold_weight=gold_weight,  # Include gold_weight in the model field
        )
        product.save()

        # Redirect to a success page or any other desired action
        return redirect('adminpage')

    return render(request, 'adminpage.html')


def view_product(request):
    products = Product.objects.all()  # Retrieve all products from the database
    return render(request, 'viewproduct.html', {'products': products})







# views.py
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


def product_details(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'product_details.html', {'product': product})









# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from .models import Product, ShoppingCart

# def view_cart(request, product_id=None):
#     cart_items = ShoppingCart.objects.filter(user=request.user)

#     if request.method == 'POST':
#         item_id = request.POST.get('item_id')
#         new_quantity = request.POST.get('new_quantity')

#         # Update the quantity in the database
#         cart_item = ShoppingCart.objects.get(id=item_id)
#         cart_item.quantity = new_quantity
#         cart_item.save()

#         # Redirect to the shopping cart page after updating quantity
#         return render(request, 'view_cart.html', {'cart_items': cart_items, 'product_id': product_id})

#     total_price = calculate_total_price(cart_items)
#     return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price, 'product_id': product_id})

from django.shortcuts import render, redirect
from .models import ShoppingCart

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


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Product, ShoppingCart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user

        # Check if the product is already in the user's cart
        cart_item, created = ShoppingCart.objects.get_or_create(user=user, product=product)

        # If the product is already in the cart, increment the quantity
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, 'Item added to the cart.')
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

































from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from razorpay import Client

razorpay_api_key = settings.RAZORPAY_API_KEY
razorpay_secret_key = settings.RAZORPAY_API_SECRET

razorpay_client = Client(auth=(razorpay_api_key, razorpay_secret_key))

@csrf_exempt
def rentnxt(request):
    # Amount to be paid (in paisa), you can change this dynamically based on your logic
    amount = 100

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
    }

    return render(request, 'payment.html', context)
