from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import User, db
from config import ApplicationConfig

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
db.init_app(app)

# with app.app_context():
#     db.drop_all()
#     db.create_all()


def handle_errors(err):
    errors = 'User could not be created'
    if isinstance(err, IntegrityError) and 'unique constraint' in str(err):
        return 'email address is already registered'
    if 'user validation failed' in str(err):
        return 'user validation failed'
    return errors


def clean_item_price_id(item_price_id):
    # Remove any quotes from the item_price_id
    return item_price_id.strip('"\'')


@app.route('/signup', methods=['POST'])
def signup_post():
    try:
        data = request.form
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        email = data.get("email")
        phone = data.get("phone")
        company = data.get("company")
        plan = clean_item_price_id(data.get("itemPriceId"))

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

        # Define a default redirect URL in case no plan is selected
        redirect_url = '/'

        # Map plans to their respective URLs
        plan_urls = {
            'RMS1000M': 'https://buy.stripe.com/fZefZecfHcVbeLC8wy',
            'RMS1000Y': 'https://buy.stripe.com/aEU4gw4Nf08peLC8wx',
            'RMG1000M': 'https://buy.stripe.com/bIYdR6enPcVb46Y148',
            'RMG1000Y': 'https://buy.stripe.com/4gw4gw5RjcVb5b2dQT',
            'RMP1000M': 'https://buy.stripe.com/aEU14kcfH1ct7ja288',
            'RMP1000Y': 'https://buy.stripe.com/14kdR61B33kB6f6bIN',
        }

        # Check if the cleaned plan exists in the mapping
        if plan in plan_urls:
            redirect_url = plan_urls[plan]

        return redirect(redirect_url)  # Redirect to the appropriate URL

    except Exception as e:
        print(f"Exception: {e}")
        errors = handle_errors(e)
        return jsonify({"errors": errors}), 400


if __name__ == '__main__':
    app.run(debug=True)
