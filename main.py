# Import libraries
import os.path
import random
from cryptography.fernet import Fernet


# Generate a key for AES encryption
def generate_key():
    return Fernet.generate_key()


# Initialize the Fernet object with the generated key
def init_fernet(key):
    return Fernet(key)


# Function to encrypt the password with Fernet
def encrypt_password(password, fernet):
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password.decode()


# Function to decrypt the password with Fernet
def decrypt_password(encrypted_password, fernet):
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password


# Function to generate a random password
def generate_password():
    password = ''
    for _ in range(16):
        password += chr(random.randint(33, 126))
    return password


# Function to save the password to a file with a specified name
def save_password(password, filename, password_name, fernet):
    encrypted_password = encrypt_password(password, fernet)
    with open(filename, 'a') as file:
        file.write(f"{password_name},{encrypted_password}\n")
    return password_name


# Function to read the password from a file by a specified name
def read_password_by_name(filename, password_name, fernet):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                name, encrypted_password = line.strip().split(',')
                if name == password_name:
                    password = decrypt_password(encrypted_password.encode(), fernet)
                    return password
        print(f"Password with name '{password_name}' not found.")
    else:
        print("File does not exist")
    return None


# Function to delete the password from a file by a specified name
def delete_password(filename, password_name):
    if os.path.exists(filename):
        password_found = False
        with open(filename, 'r') as file:
            lines = file.readlines()

        with open(filename, 'w') as file:
            for line in lines:
                name, _ = line.strip().split(',', 1)  # Split only on the first comma
                if name == password_name:
                    password_found = True
                else:
                    file.write(f"{name},{_}\n")

        if password_found:
            print(f"Password '{password_name}' deleted successfully!")
        else:
            print(f"Password '{password_name}' not found in the file.")
    else:
        print("File does not exist")


# Function to display the menu
def display_menu():
    print('1. Generate Password')
    print('2. Save Password')
    print('3. Read Password by Name')
    print('4. Delete Password by Name')
    print('5. Exit')
    choice = input('Enter your choice: ')
    return choice


# Main function
def main():
    key = generate_key()  # Generate a Fernet key
    fernet = init_fernet(key)  # Initialize Fernet with the generated key

    while True:
        choice = display_menu()
        if choice == '1':
            password = generate_password()
            print('Generated Password:', password)
        elif choice == '2':
            filename = input('Enter the filename to save the password: ')
            password_name = input("Enter a name for the password: ")
            save_password(password, filename, password_name, fernet)
            print('Password saved successfully!')
        elif choice == '3':
            filename = input('Enter the filename to read the password: ')
            password_name = input("Enter the name of the password to read: ")
            password = read_password_by_name(filename, password_name, fernet)
            if password:
                print(f'Password for {password_name}: {password}')
        elif choice == '4':
            filename = input('Enter the filename from which to delete the password: ')
            password_name = input("Enter the name of the password to delete: ")
            delete_password(filename, password_name)
        elif choice == '5':
            break
        else:
            print('Invalid choice! Try again.')


if __name__ == '__main__':
    main()
    print('Thanks for using the password manager!')
