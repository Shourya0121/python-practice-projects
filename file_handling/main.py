import json

# text file write

def write_text_file():
    with open("users.txt", "w") as file:
        file.write("Shourya\n")
        file.write("Rahul\n")
        file.write("Amit\n")

    print("users written to users.txt")


#text file read 


def read_text_file():
    with open("users.txt", "r") as file:
        data = file.read()

    print("\nUsers from text file:")
    print(data)

#text file append 

def append_text_file():
    with open("users.txt", "a") as file:
        file.write("Rohit\n")

    print("Rohit added to Users.txt")

# JSON file write

def write_json_file():
    users = [
        {  
            "id": 1,
            "name": "Shourya",
            "age": 21
        },

        {
            "id": 2,
            "name": "Rahul",
            "age": 21
        },

        {
            "id": 3,
            "name": "Amit",
            "age": 21
        }
    ]

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

    print("Users written to users.json")


def read_json_file():
    with open("users.json", "r") as file:
        users = json.load(file)

    for user in users:
        print(user)


#SHOW ONE USER

def show_one_user():
    with open("users.json", "r") as file:
        users = json.load(file)

    print("\nFirst user's information:")

    print("\nFirst Users Information:")
    print("ID:", users[0]["id"])
    print("Name:", users[0]["name"])
    print("Age:", users[0]["age"])

# add USER 

def add_user():
    with open("users.json", "r") as file:
        users = json.load(file)

    name = input("Enter your name: ")
    age = int(input("Enter your age: "))

    new_id =len(users) +1

    new_user = {
        "id": new_id,
        "name": name,
        "age": age
    }

    users.append(new_user)

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

    print("User added Successfully!")


# DELETE USERS

def delete_user():
    with open("users.json", "r") as file:
        users = json.load(file)

    user_id = int(input("Enter user id to delete: "))

    new_users = []

    for user in users:
        if user["id"] != user_id:
            new_users.append(user)

    if len(new_users) == len(users):
        print("User not found!")
    else:
        with open("users.json", "w") as file:
            json.dump(new_users, file, indent=4)

        print("User deleted Successfully!")


# UPDATE USER

def update_user():
    with open("users.json", "r") as file:
        users = json.load(file)

    user_id =int(input("Enter user Id to update: "))

    found = False

    for user in users:
        if user["id"] == user_id:
            new_name = input("Enter new name: ")
            new_age = int(input("Enter new age: "))
            user["name"] = new_name
            user["age"] = new_age
            found = True
            break
    if found:
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

        print("User updated Successfully!")

    else:
        print("User not found!")

# SHOW ALL USERS

def show_users():
    with open("users.json", "r") as file:
        users = json.load(file)

    print("\nusers")

    for user in users:
        print(
            f"ID: {user['id']}"
            f"Name: {user['name']}"
            f"Age: {user['age']}"
        )

    print()

#MAIN MENU

def main():
    try:
        with open("users.json", "r") as file:
            json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = [
            {
                "id": 1,
                "name": "Shourya",
                "age": 21
            },

            {
                "id": 2,
                "name": "Rahul",
                "age": 23
            },

            {
                "id": 3,
                "name": "Aman",
                "age": 21
            }
        ]

        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

    while True:
        print("\n========== USER MANAGEMENT ==========")
        print("1. Write users to TXT")
        print("2. Read users from TXT")
        print("3. Append user to TXT")
        print("4. Write users to JSON")
        print("5. Read users from JSON")
        print("6. Show one user")
        print("7. Show all users")
        print("8. Add user")
        print("9. Update user")
        print("10. Delete user")
        print("11. Exit")
        print("=====================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            write_text_file()
        elif choice == "2":
            read_text_file()
        elif choice == "3":
            append_text_file()
        elif choice == "4":
            write_json_file()
        elif choice == "5":
            read_json_file()
        elif choice == "6":
            show_one_user()
        elif choice == "7":
            show_users()
        elif choice == "8":
            add_user()
        elif choice == "9":
            update_user()
        elif choice == "10":
            delete_user()
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# START PROGRAM
if __name__ == "__main__":
    main()

                    

                
        
