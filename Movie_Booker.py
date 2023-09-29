import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(host="localhost",user="root",password="hack")

cursor = db.cursor()
#Create Database if they don't exist
db_name = "movie_booking"
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
cursor.execute(f"USE {db_name}")

# Create tables if they don't exist
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(255) NOT NULL UNIQUE,password VARCHAR(255) NOT NULL,is_admin BOOLEAN NOT NULL DEFAULT 0)")

cursor.execute("CREATE TABLE IF NOT EXISTS movies (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL,ticket_price DECIMAL(10, 2) NOT NULL,seats_available INT NOT NULL)")

cursor.execute("CREATE TABLE IF NOT EXISTS bookings (id INT AUTO_INCREMENT PRIMARY KEY,user_id INT NOT NULL,movie_id INT NOT NULL,FOREIGN KEY (user_id) REFERENCES users(id),FOREIGN KEY (movie_id) REFERENCES movies(id),seats_booked INT NOT NULL DEFAULT 0)")

# Default admin credentials
default_admin_username = "admin"
default_admin_password = "admin"

# Function to check if admin exists
def admin_exists():
    cursor.execute("SELECT * FROM users WHERE is_admin = 1")
    return cursor.fetchone() is not None

# Initialize admin account if it doesn't exist
if not admin_exists():
    cursor.execute("INSERT INTO users (username, password, is_admin)VALUES (%s, %s, %s)", (default_admin_username, default_admin_password, 1))
    db.commit()

# User registration function
def register_user():
    print()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("INSERT INTO users (username, password)VALUES (%s, %s)", (username, password))

    db.commit()
    print("Registration successful!")
    print()

# Edit movie function (only for admin)
def edit_movie():
    print()
    movie_id = int(input("Enter movie ID to edit: "))
    new_name = input("Enter new movie name: ")
    new_ticket_price = float(input("Enter new ticket price: "))
    new_seats_available = int(input("Enter new seats available: "))

    cursor.execute("UPDATE movies SET name = %s, ticket_price = %s, seats_available = %s WHERE id = %s", (new_name, new_ticket_price, new_seats_available, movie_id))

    db.commit()
    print()
    print("Movie edited successfully!")

# Cancel movie function
def cancel_booking(user_id):
    cursor.execute("SELECT * FROM bookings WHERE user_id = %s", (user_id,))
    bookings = cursor.fetchall()

    if not bookings:
        print("You have no bookings to cancel.")
        return
    print()
    print()
    print("Your Bookings:")
    print()
    for booking in bookings:
        print(f"Booking ID: {booking[0]}, Movie ID: {booking[2]}, Seats Booked: {booking[3]}")
        
    print()
    booking_id = int(input("Enter the Booking ID you want to cancel: "))
    num_seats_to_cancel = int(input("Enter the number of seats you want to cancel: "))

    cursor.execute("SELECT seats_booked, movie_id FROM bookings WHERE id = %s AND user_id = %s", (booking_id, user_id))
    booking_info = cursor.fetchone()

    if booking_info:
        seats_booked, movie_id = booking_info

        cursor.execute("SELECT seats_available FROM movies WHERE id = %s", (movie_id,))
        seats_available = cursor.fetchone()[0]

        if seats_booked >= num_seats_to_cancel:
            cursor.execute("UPDATE bookings SET seats_booked = seats_booked - %s WHERE id = %s AND user_id = %s", (num_seats_to_cancel, booking_id, user_id))
            cursor.execute("UPDATE movies SET seats_available = seats_available + %s WHERE id = %s", (num_seats_to_cancel, movie_id))
            db.commit()
            print()
            print(f"{num_seats_to_cancel} seat(s) canceled successfully!")
            print()
        else:
            print(f"You can cancel up to {seats_booked} seat(s) for this booking.")
    else:
        print("Invalid booking ID or this booking does not belong to you.")


# Remove movie functon (only for admin) 
def remove_movie():
    movie_id = int(input("Enter movie ID to remove: "))

    cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    db.commit()
    print()
    print("Movie removed successfully!")


# User login function
def user_login():
    print()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))

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

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND is_admin = 1", (username, password))

    admin = cursor.fetchone()

    if admin:
        return admin
    else:
        return None

# Add movie function (only for admin)
def add_movie():
    print()
    movie_name = input("Enter movie name: ")
    ticket_price = float(input("Enter ticket price: "))
    seats_available = int(input("Enter seats available: "))

    cursor.execute("INSERT INTO movies (name, ticket_price, seats_available) VALUES (%s, %s, %s)", (movie_name, ticket_price, seats_available))

    db.commit()
    print("Movie added successfully!")
    print()

# Display movie details function
def display_movie_details():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    print()
    print("Movie Details:")
    print()
    for movie in movies:
        print(f"Movie ID: {movie[0]}, Name: {movie[1]}, Ticket Price: ₹{movie[2]}, Seats Available: {movie[3]}")
        
# Function to book a movie for a user
def book_movie(user_id):
    display_movie_details()
    print()
    movie_id = int(input("Enter the Movie ID you want to book: "))
    num_seats = int(input("Enter the number of seats you want to book: "))

    cursor.execute("SELECT * FROM movies WHERE id = %s AND seats_available >= %s", (movie_id, num_seats))
    movie = cursor.fetchone()

    if movie:
        cursor.execute("SELECT seats_available FROM movies WHERE id = %s", (movie_id,))
        seats_available = cursor.fetchone()[0]

        if seats_available >= num_seats:
            cursor.execute("INSERT INTO bookings (user_id, movie_id, seats_booked) VALUES (%s, %s, %s)", (user_id, movie_id, num_seats))
            cursor.execute("UPDATE movies SET seats_available = seats_available - %s WHERE id = %s", (num_seats, movie_id))
            db.commit()
            print()
            print(f"{num_seats} seat(s) booked successfully!")
            print()
        else:
            print(f"Not enough seats available. Maximum available seats: {seats_available}")
    else:
        print("Invalid movie selection or not enough available seats.")


# Main program
if __name__ == "__main__":
    while True:
        print()
        print("Welcome to the Movie Booking Page!")
        print()
        print("1. Login")
        print("2. Register")
        print("3. Exit")  # Added option to exit
        print()
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            print()
            print("1. User Login")
            print("2. Admin Login")
            print("3. Exit")  # Added option to exit
            print()
            login_choice = input("Enter your choice (1/2/3): ")

            if login_choice == "1":
                user = user_login()
                if user:
                    print()
                    print(f"Logged in as user: {user[1]}.")
                    
                    while True:
                        print()
                        print("1. Display movie details")
                        print("2. Book a movie")
                        print("3. Cancel a booked movie")
                        print("4. Logout")
                        print("5. Exit")  # Added option to exit
                        print()
                        user_choice = input("Enter your choice (1/2/3/4): ")

                        if user_choice == "1":
                            display_movie_details()
                        elif user_choice == "2":
                            book_movie(user[0])# Pass user ID to book_movie function
                        elif user_choice == "3":
                            cancel_booking(user[0])
                        elif user_choice == "4":
                            break   #25/09/23 added book & cancel                             break
                        elif user_choice == "5":  # Added option to exit
                            print("Thank you for using our Movie Booking App!")
                            exit()
                        else:
                            print("Invalid choice. Please enter 1, 2, 3, or 4.")
                else:
                    print()
                    print("User login failed. Please try again.")
            elif login_choice == "2":
                admin = admin_login()
                if admin:
                    print()
                    print(f"Logged in as admin: {admin[1]}.")
                    print()
                    while True:
                        print()
                        print("1. Add Movie")
                        print("2. Edit Movie")
                        print("3. Remove Movie")
                        print("4. Display Movie Details")
                        print("5. Logout")
                        print("6. Exit")  # Added option to exit
                        print()
                        admin_choice = input("Enter your choice (1/2/3/4): ")

                        if admin_choice == "1":
                            add_movie()
                        elif admin_choice == "2":
                            edit_movie()
                        elif admin_choice == "3":
                            remove_movie()
                        elif admin_choice == "4":
                            display_movie_details()
                        elif admin_choice == "5":
                            break
                        elif admin_choice == "6":  # Added option to exit
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
