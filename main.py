# Import libraries
import os.path
import random


# Function to generate a random password
def generate_password():
    password = ''
    for i in range(16):
        password += chr(random.randint(33, 126))
    return password


# Function to save the password to a file with a specified name
def save_password(password, filename, password_name):
    encrypted_password = encrypt_password(password)
    with open(filename, 'a') as file:
        file.write(f"{password_name},{encrypted_password}\n")
    return password_name


# Function to read the password from a file by a specified name
# Fonction pour lire le mot de passe associé à un nom donné
def read_password_by_name(filename, password_name):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                name, encrypted_password = line.strip().split(',')
                if name == password_name:
                    password = decrypt_password(encrypted_password)
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
                name, encrypted_password = line.strip().split(',', 1)  # Split seulement sur la première virgule
                if name == password_name:
                    password_found = True
                else:
                    file.write(f"{name},{encrypted_password}\n")

        if password_found:
            print(f"Password '{password_name}' deleted successfully!")
        else:
            print(f"Password '{password_name}' not found in the file.")
    else:
        print("File does not exist")


# Function to encrypt the password
def encrypt_password(password):
    encrypted_password = ''
    for char in password:
        encrypted_password += chr(ord(char) + 1)
    return encrypted_password


# Function to decrypt the password
def decrypt_password(encrypted_password):
    decrypted_password = ''
    for char in encrypted_password:
        decrypted_password += chr(ord(char) - 1)
    return decrypted_password


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
    while True:
        choice = display_menu()
        if choice == '1':
            password = generate_password()
            print('Generated Password:', password)
        elif choice == '2':
            filename = input('Enter the filename to save the password: ')
            password_name = input("Enter a name for the password: ")
            encrypted_password = encrypt_password(password)
            save_password(encrypted_password, filename, password_name)
            print('Password saved successfully!')
        elif choice == '3':
            filename = input('Enter the filename to read the password: ')
            password_name = input("Enter the name of the password to read: ")
            encrypted_password = read_password_by_name(filename, password_name)
            if encrypted_password:
                password = decrypt_password(encrypted_password)
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
