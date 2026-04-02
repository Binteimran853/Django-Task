This project is a Django-based E-Commerce platform that allows users to browse products, create accounts, login/logout, manage their profile, and perform other e-commerce operations like adding products to a cart.

The application is designed using Django forms, custom templates, class-based views, and custom user models. Proper exception handling and template inheritance are implemented for a scalable, maintainable codebase

Features
- User registration, login, and logout
- Profile editing with image upload
- Password reset via email
- Product listing and detail pages
- Shopping cart functionality
- Custom Django forms and validation
- Class-based views and URL routing
- Exception handling for robust operation
- Template inheritance for DRY code

## Setup Commands:
`git clone https://github.com/yourusername/django-ecommerce.git
cd django-ecommerce`

`python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows`

`pip install -r requirements.txt`

`python manage.py makemigrations
python manage.py migrate`

`python manage.py createsuperuser`

`python manage.py runserver`
