from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import User, db
from config import ApplicationConfig

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
db.init_app(app)


def handle_errors(err):
    errors = 'User could not be created'
    if isinstance(err, IntegrityError) and 'unique constraint' in str(err):
        return 'email address is already registered'
    if 'user validation failed' in str(err):
        return 'user validation failed'
    return errors


@app.route('/signup', methods=['POST'])
def signup_post():
    try:
        data = request.form
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        email = data.get("email")
        phone = data.get("phone")
        company = data.get("company")
        plan = data.get("plan")

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

        # Redirect based on the selected plan
        # Starter plans
        if plan == 'RMS1000M':
            return redirect('https://buy.stripe.com/fZefZecfHcVbeLC8wy')
        # Starter Yearly
        elif plan == 'RMS1000Y':
            return redirect('https://buy.stripe.com/aEU4gw4Nf08peLC8wx')

        # Growth plans
        elif plan == 'RMG1000M':
            return redirect('https://buy.stripe.com/bIYdR6enPcVb46Y148')
        # Growth Yearly
        elif plan == 'RMG1000Y':
            return redirect('https://buy.stripe.com/4gw4gw5RjcVb5b2dQT')

        # Profesional plans
        elif plan == 'RMP1000M':
            return redirect('https://buy.stripe.com/aEU14kcfH1ct7ja288')
        elif plan == 'RMP1000Y':
            return redirect('https://buy.stripe.com/14kdR61B33kB6f6bIN')

        # Add more conditions for other plans as needed

        return jsonify({"message": "User created successfully", "user_id": new_user.id})

    except Exception as e:
        print(f"Exception: {e}")
        errors = handle_errors(e)
        return jsonify({"errors": errors}), 400


if __name__ == '__main__':
    app.run(debug=True)
