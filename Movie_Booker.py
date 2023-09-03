import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hack",
    database="movie_booking"
)

cursor = db.cursor()

# Create tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        ticket_price DECIMAL(10, 2) NOT NULL,
        seats_available INT NOT NULL
    )
""")

# Default admin credentials
default_admin_username = "admin"
default_admin_password = "admin"

# Function to check if admin exists
def admin_exists():
    cursor.execute("SELECT * FROM users WHERE is_admin = 1")
    return cursor.fetchone() is not None

# Initialize admin account if it doesn't exist
if not admin_exists():
    cursor.execute("""
        INSERT INTO users (username, password, is_admin)
        VALUES (%s, %s, %s)
    """, (default_admin_username, default_admin_password, 1))
    db.commit()

# User registration function
def register_user():
    print()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (%s, %s)
    """, (username, password))

    db.commit()
    print("Registration successful!")
    print()

# User login function
def user_login():
    print()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("""
        SELECT * FROM users WHERE username = %s AND password = %s
    """, (username, password))

    user = cursor.fetchone()

    if user:
        return user
    else:
        return None

# Admin login function
def admin_login():
    print()
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    cursor.execute("""
        SELECT * FROM users WHERE username = %s AND password = %s AND is_admin = 1
    """, (username, password))

    admin = cursor.fetchone()

    if admin:
        return admin
    else:
        return None

# Add movie function (only for admin)
def add_movie():
    movie_name = input("Enter movie name: ")
    ticket_price = float(input("Enter ticket price: "))
    seats_available = int(input("Enter seats available: "))

    cursor.execute("""
        INSERT INTO movies (name, ticket_price, seats_available)
        VALUES (%s, %s, %s)
    """, (movie_name, ticket_price, seats_available))

    db.commit()
    print("Movie added successfully!")
    print()

def remove_movie():
    movie_id = int(input("Enter movie ID to remove: "))

    cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    db.commit()
    print("Movie removed successfully!")

# Edit movie function (only for admin)
def edit_movie():
    movie_id = int(input("Enter movie ID to edit: "))
    new_name = input("Enter new movie name: ")
    new_ticket_price = float(input("Enter new ticket price: "))
    new_seats_available = int(input("Enter new seats available: "))

    cursor.execute("""
        UPDATE movies
        SET name = %s, ticket_price = %s, seats_available = %s
        WHERE id = %s
    """, (new_name, new_ticket_price, new_seats_available, movie_id))

    db.commit()
    print("Movie edited successfully!")


# Display movie details function
def display_movie_details():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()

    print("Movie Details:")
    print()
    for movie in movies:
        print(f"Movie ID: {movie[0]}, Name: {movie[1]}, Ticket Price: ${movie[2]}, Seats Available: {movie[3]}")
        print()
# Main program
if __name__ == "__main__":
    while True:
        print("Welcome to the Movie Booking Page!")
        print()
        print("1. Login")
        print("2. Register")
        print()
        choice = input("Enter your choice (1/2): ")
        print()

        if choice == "1":
            print("1. User Login")
            print("2. Admin Login")
            print()
            login_choice = input("Enter your choice (1/2): ")

            if login_choice == "1":
                user = user_login()
                print()
                if user:
                    print(f"Logged in as user: {user[1]}.")
                    print()
                    #me edited -Z403
                    print("1. Display movie details")
                    print()
                    choice = int(input("Enter your choice : "))
                    print()
                    if choice == 1:
                        display_movie_details()
                        print()
                else:
                    print("User login failed. Please try again.")
            elif login_choice == "2":
                admin = admin_login()
                if admin:
                    print()
                    print(f"Logged in as admin: {admin[1]}.")
                    while True:
                        print()
                        print("1. Add Movie")
                        print("2. Remove Movie")
                        print("3. Edit Movie")
                        print("4. Display Movie Details")
                        print("5. Logout")
                        print()
                        admin_choice = input("Enter your choice (1/2/3/4/5): ")
                        print()
                        if admin_choice == "1":
                            add_movie()
                        elif admin_choice == "2":
                            remove_movie()
                        elif admin_choice == "3":
                            edit_movie()
                        elif admin_choice == "4":
                            display_movie_details()
                        elif admin_choice == "5":
                            break
                        else:
                            print("Invalid choice. Please enter a valid option.")
                else:
                    print("Admin login failed. Please try again.")
            else:
                print("Invalid choice. Please enter 1 or 2.")
                print()
        elif choice == "2":
            register_user()
        else:
            print("Invalid choice. Please enter 1 or 2.")

## paisa  ₹ $ 
