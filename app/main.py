
from app import create_app
from app.extensions import db

app = create_app()


if __name__ == "__main__":

    # Create database tables
    with app.app_context():
        db.create_all()

    # Start Flask development server
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
