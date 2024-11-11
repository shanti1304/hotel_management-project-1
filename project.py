import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1326",
        database="hotel_management"
    )

    if conn.is_connected():
        print("Connected to MySQL database")
    
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_number INT PRIMARY KEY,
            capacity INT NOT NULL,
            price_per_night DECIMAL(10, 2) NOT NULL,
            availability BOOLEAN DEFAULT TRUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            guest_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            contact_number VARCHAR(15) NOT NULL,
            room_number INT,
            check_in_date DATE,
            check_out_date DATE,
            FOREIGN KEY (room_number) REFERENCES rooms(room_number)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            service_id INT AUTO_INCREMENT PRIMARY KEY,
            service_name VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            price DECIMAL(10, 2) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_bookings (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            guest_id INT,
            service_id INT,
            FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
            FOREIGN KEY (service_id) REFERENCES services(service_id)
        )
    ''')

    conn.commit()

except Error as e:
    print(f"Error: {e}")
    exit(1)

# Function to add a room
def add_room(room_number, capacity, price_per_night):
    try:
        cursor.execute('''
            INSERT INTO rooms (room_number, capacity, price_per_night, availability)
            VALUES (%s, %s, %s, TRUE)
        ''', (room_number, capacity, price_per_night))
        conn.commit()
        print(f"Room {room_number} added successfully!")
    except Error as e:
        print(f"Error: {e}")

# Function to view rooms
def view_rooms():
    try:
        cursor.execute('SELECT * FROM rooms')
        rooms = cursor.fetchall()
        print("\nRoom List:")
        for room in rooms:
            availability_status = "Available" if room[3] else "Occupied"
            print(f"Room Number: {room[0]}, Capacity: {room[1]}, Price per Night: ${room[2]}, "
                  f"Availability: {availability_status}")
    except Error as e:
        print(f"Error: {e}")

# Function to make a reservation
def make_reservation(guest_name, contact_number, room_number, check_in_date, check_out_date):
    try:
        cursor.execute('SELECT availability FROM rooms WHERE room_number=%s', (room_number,))
        availability = cursor.fetchone()[0]
        
        if availability:
            cursor.execute('''
                INSERT INTO guests (name, contact_number, room_number, check_in_date, check_out_date)
                VALUES (%s, %s, %s, %s, %s)
            ''', (guest_name, contact_number, room_number, check_in_date, check_out_date))
            cursor.execute('UPDATE rooms SET availability = FALSE WHERE room_number=%s', (room_number,))
            conn.commit()
            print(f"Reservation for {guest_name} made successfully!")
        else:
            print(f"Room {room_number} is not available for the selected dates.")
    except Error as e:
        print(f"Error: {e}")

# Function to view reservations
def view_reservations():
    try:
        cursor.execute('SELECT * FROM guests')
        reservations = cursor.fetchall()
        print("\nReservation List:")
        for reservation in reservations:
            print(f"Guest ID: {reservation[0]}, Name: {reservation[1]}, Contact Number: {reservation[2]}, "
                  f"Room Number: {reservation[3]}, Check-in Date: {reservation[4]}, Check-out Date: {reservation[5]}")
    except Error as e:
        print(f"Error: {e}")

# Function to check out
def check_out(guest_id):
    try:
        cursor.execute('SELECT room_number FROM guests WHERE guest_id=%s', (guest_id,))
        room_number = cursor.fetchone()[0]
        cursor.execute('DELETE FROM guests WHERE guest_id=%s', (guest_id,))
        cursor.execute('UPDATE rooms SET availability = TRUE WHERE room_number=%s', (room_number,))
        conn.commit()
        print(f"Guest with ID {guest_id} checked out successfully.")
    except Error as e:
        print(f"Error: {e}")

# Function to calculate revenue
def calculate_revenue():
    try:
        cursor.execute('SELECT SUM(price_per_night) FROM rooms WHERE availability = FALSE')
        total_revenue = cursor.fetchone()[0]
        print(f"\nTotal Revenue: ${total_revenue}")
    except Error as e:
        print(f"Error: {e}")

# Main menu
def main():
    while True:
        print("\nHotel Management System")
        print("1. Add Room")
        print("2. View Rooms")
        print("3. Make Reservation")
        print("4. View Reservations")
        print("5. Check-Out")
        print("6. Calculate Revenue")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            room_number = int(input("Enter room number: "))
            capacity = int(input("Enter room capacity: "))
            price_per_night = float(input("Enter price per night: "))
            add_room(room_number, capacity, price_per_night)
        elif choice == '2':
            view_rooms()
        elif choice == '3':
            guest_name = input("Enter guest name: ")
            contact_number = input("Enter contact number: ")
            room_number = int(input("Enter room number for reservation: "))
            check_in_date = input("Enter check-in date (yyyy-mm-dd): ")
            check_out_date = input("Enter check-out date (yyyy-mm-dd): ")
            make_reservation(guest_name, contact_number, room_number, check_in_date, check_out_date)
        elif choice == '4':
            view_reservations()
        elif choice == '5':
            guest_id = int(input("Enter guest ID for check-out: "))
            check_out(guest_id)
        elif choice == '6':
            calculate_revenue()
        elif choice == '7':
            print("Exiting Hotel Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed")

if __name__ == "__main__":
    main()
