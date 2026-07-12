from app import create_app
from app.models.user import User

app = create_app()

with app.app_context():
    u = User(
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        password="secret123"
    )

    print("Hash:", u.password)
    print("Correct:", u.verify_password("secret123"))
    print("Wrong:", u.verify_password("wrong"))
