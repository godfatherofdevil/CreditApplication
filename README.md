# CreditApplication
A simple Django and DRF based credit web application

There are three kinds of users of this application:
1. Partners - Can create customer profile, credit application etc.
2. Credit Organizations - Can get the details of bids sent to them and change the status of the application
3. Super User - Have all rights

To run this application, follow following steps:
1. git clone https://github.com/godfatherofdevil/CreditApplication.git to local system
2. pip install -all requirements.txt
3. python manage.py createsuperuser
4. python manage.py runserver (from the root project directory)
5. on API root, login with appropriate credentials or create more users from admin (http://localhost:8000/admin)
