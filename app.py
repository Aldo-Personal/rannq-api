import base64
from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt_sha256
import requests
from config import ApplicationConfig
from models import User, db
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
db.init_app(app)


@app.after_request
def add_cors_headers(response):
    frontend_domains = [
        'http://localhost:3000',
        'https://www.enetworksagencybanking.com.ng',
        'https://enetworks-update.vercel.app',
        'https://jobs-admin.vercel.app'
    ]

    origin = request.headers.get('Origin')
    if origin in frontend_domains:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


def handle_errors(err):
    print(err)
    errors = 'User could not be created'

    # duplicate
    if isinstance(err, IntegrityError) and 'unique constraint' in str(err):
        return 'email address is already registered'

    # validation errors
    if 'user validation failed' in str(err):
        return 'user validation failed'

    return errors


@app.route('/signup', methods=['POST'])
def signup_post():
    try:
        data = request.form
        # hashed_password = bcrypt_sha256.hash(data['password'])
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        email = data.get("email")
        phone = data.get("phone")
        company = data.get("company")

        new_user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            company=company
        )

        db.session.add(new_user)
        db.session.commit()

        print(f"User created successfully. User ID: {new_user.id}")

        # Create seat on rannq
        rannq_url = "https://server.onlinereviews.tech/public-api/v1.0.0/seat/add"
        rannq_payload = {
            "seat_name": data['company'],
            "email": data['email'],
            "full_name": f"{data['firstname']} {data['lastname']}",
            "purchase": False,
            "email_subject": "Email Subject",
            "email_text": "Email Text content"
        }
        rannq_headers = {
            "x-api-key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiNjRlYzc3N2Y1MzdkZWIxNGEwMDZlZDM1Iiwic2VydmVyX2VudiI6IlByb2QiLCJzZXJ2ZXJfdXJsIjoiaHR0cHM6Ly9zZXJ2ZXIub25saW5lcmV2aWV3cy50ZWNoL2FwaS92MC4wLjkifQ.rQzAkXnWspWzT81XiF7LJAEUjR3znxxJ-MW371x5tnI"
        }
        rannq_response = requests.post(
            rannq_url, json=rannq_payload, headers=rannq_headers)

        print(
            f"Seat Creation Response - Status Code: {rannq_response.status_code}")
        print(f"Seat Creation Response Headers: {rannq_response.headers}")
        try:
            print(f"Seat Creation Response Body: {rannq_response.json()}")
        except ValueError:
            print(f"Seat Creation Response Body: {rannq_response.text}")

        seat_id = rannq_response.json().get("seat_id")

        # Create user on rannex
        rainex_url = "https://api.rainex.io/projects/rannq/customers"
        rainex_payload = {
            "id": new_user.id,
            "firstName": new_user.firstname,
            "lastName": new_user.lastname,
            "company": new_user.company,
            "phone": new_user.phone,
            "language": "en",
            "billingAddress": {
                "email": new_user.email,
                "phone": new_user.phone,
                "organizationName": new_user.company,
                "house": new_user.house,
                "street": new_user.street,
                "apartment": new_user.apartment,
                "city": new_user.city,
                "zipCode": new_user.zipCode,
                "country": new_user.country,
                "vatNumber": new_user.vatNumber,
                "tax": "13"
            }
        }

        credentials = f"{ApplicationConfig.RAINEX_API_ID}:{ApplicationConfig.RAINEX_API_KEY}"
        basic_auth = base64.b64encode(
            credentials.encode('utf-8')).decode('utf-8')
        rainex_headers = {
            "Authorization": f"Basic {basic_auth}"
        }

        rainex_response = requests.post(
            rainex_url, json=rainex_payload, headers=rainex_headers)

        print(
            f"Rannex User Creation Response - Status Code: {rainex_response.status_code}")
        print(
            f"Rannex User Creation Response Headers: {rainex_response.headers}")
        try:
            print(
                f"Rannex User Creation Response Body: {rainex_response.json()}")
        except ValueError:
            print(
                f"Rannex User Creation Response Body: {rainex_response.text}")

        # Create subscription for user
        subscription_url = "https://api.rainex.io/projects/rannq/subscriptions"
        subscription_payload = {
            "customerId": new_user.id,
            "productFamilyId": "your_product_family_id",
            "channel": "Web",
            "billingCycles": "Forever",
            "billingPeriod": None,
            "autoCollection": "off",
            "usePendingPaymentFlow": True,
            "items": [
                {
                    "itemPriceId": "your_item_price_id",
                    "freeQuantity": None,
                    "amount": "your_amount"
                }
            ],
            "currencyCode": "USD",
            "frequencyId": 1207,
            "includeVat": True
        }
        subscription_response = requests.post(
            subscription_url, json=subscription_payload, headers=rainex_headers)

        print(
            f"Subscription Creation Response - Status Code: {subscription_response.status_code}")
        print(
            f"Subscription Creation Response Headers: {subscription_response.headers}")
        try:
            print(
                f"Subscription Creation Response Body: {subscription_response.json()}")
        except ValueError:
            print(
                f"Subscription Creation Response Body: {subscription_response.text}")

        # Return a success response
        return jsonify({
            "message": "User created successfully",
            "seat_id": seat_id,
            "user_id": new_user.id,
            "rannex_user_id": rainex_response.json().get('id'),
            "subscription_id": subscription_response.json().get('id')
        })

    except Exception as e:
        # Handle exceptions
        print(f"Exception: {e}")

        if hasattr(e, 'response') and e.response is not None:
            try:
                # Try to parse the response as JSON
                api_response = e.response.json()
                print(f"API Response Status Code: {e.response.status_code}")
                print(f"API Response Headers: {e.response.headers}")
                print(f"API Response Body: {api_response}")
            except ValueError:
                # If parsing as JSON fails, print the raw response text
                print(f"API Response Status Code: {e.response.status_code}")
                print(f"API Response Headers: {e.response.headers}")
                print(f"API Response Body: {e.response.text}")

        errors = handle_errors(e)
        return jsonify({"errors": errors}), 400


if __name__ == '__main__':
    app.run(debug=True)
