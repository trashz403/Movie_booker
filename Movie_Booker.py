
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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (movie_id) REFERENCES movies(id)
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

# Display movie details function
def display_movie_details():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()

    print("Movie Details:")
    for movie in movies:
        print(f"Movie ID: {movie[0]}, Name: {movie[1]}, Ticket Price: ₹{movie[2]}, Seats Available: {movie[3]}")

# Function to book a movie for a user
def book_movie(user_id):
    display_movie_details()
    movie_id = int(input("Enter the Movie ID you want to book: "))

    # Check if the movie exists and has available seats
    cursor.execute("SELECT * FROM movies WHERE id = %s AND seats_available > 0", (movie_id,))
    movie = cursor.fetchone()

    if movie:
        # Check if the user has already booked this movie
        cursor.execute("SELECT * FROM bookings WHERE user_id = %s AND movie_id = %s", (user_id, movie_id))
        existing_booking = cursor.fetchone()

        if existing_booking:
            print("You have already booked this movie.")
        else:
            cursor.execute("INSERT INTO bookings (user_id, movie_id) VALUES (%s, %s)", (user_id, movie_id))
            cursor.execute("UPDATE movies SET seats_available = seats_available - 1 WHERE id = %s", (movie_id,))
            db.commit()
            print("Movie booked successfully!")
    else:
        print("Invalid movie selection or no available seats.")

# Main program
if __name__ == "__main__":
    while True:
        print("Welcome to the Movie Booking Page!")
        print("1. Login")
        print("2. Register")
        print("3. Exit")  # Added option to exit
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            print("1. User Login")
            print("2. Admin Login")
            print("3. Exit")  # Added option to exit
            login_choice = input("Enter your choice (1/2/3): ")

            if login_choice == "1":
                user = user_login()
                if user:
                    print(f"Logged in as user: {user[1]}.")
                    print()
                    while True:
                        print("1. Display movie details")
                        print("2. Book a movie")
                        print("3. Logout")
                        print("4. Exit")  # Added option to exit
                        user_choice = input("Enter your choice (1/2/3/4): ")

                        if user_choice == "1":
                            display_movie_details()
                        elif user_choice == "2":
                            book_movie(user[0])  # Pass user ID to book_movie function
                        elif user_choice == "3":
                            break
                        elif user_choice == "4":  # Added option to exit
                            print("Thank you for using our Movie Booking App!")
                            exit()
                        else:
                            print("Invalid choice. Please enter 1, 2, 3, or 4.")
                else:
                    print("User login failed. Please try again.")
            elif login_choice == "2":
                admin = admin_login()
                if admin:
                    print()
                    print(f"Logged in as admin: {admin[1]}.")
                    while True:
                        print("1. Add Movie")
                        print("2. Display Movie Details")
                        print("3. Logout")
                        print("4. Exit")  # Added option to exit
                        admin_choice = input("Enter your choice (1/2/3/4): ")

                        if admin_choice == "1":
                            add_movie()
                        elif admin_choice == "2":
                            display_movie_details()
                        elif admin_choice == "3":
                            break
                        elif admin_choice == "4":  # Added option to exit
                            print("Thank you for using our Movie Booking App!")
                            exit()
                        else:
                            print("Invalid choice. Please enter 1, 2, 3, or 4.")
                else:
                    print("Admin login failed. Please try again.")
            elif login_choice == "3":  # Added option to exit
                print("Thank you for using our Movie Booking App!")
                exit()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        elif choice == "2":
            register_user()
        elif choice == "3":  # Added option to exit
            print("Thank you for using our Movie Booking App!")
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
