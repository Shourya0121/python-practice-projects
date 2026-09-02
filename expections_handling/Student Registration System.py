class InvalidAgeError(Exception):
    pass
class InvalidMarksError(Exception):
    pass

def register_student():
    try:
        name = input("Enter your name: ")
        age = int(input("Enter your age here: "))
        marks = float(input("Enter marks here: "))

        if age < 0 or age > 100 :
            raise InvalidAgeError("Age must be between 0 and 100!")

        if marks < 0 or marks > 100:
            raise InvalidMarksError("Marks must be between 0 ans 100!")

    except ValueError:
        print("Error: Please enter valid age and marks.")

    except InvalidAgeError as error:
        print("Error:", error)

    except InvalidMarksError as error:
        print("Error:", error)

    else:
        
        print("Name:", name)
        print("Age:", age)
        print("Marks:", marks)

    finally:
        print("Student registration successful!")

def main():

    while True:
        print("\n++++++STUDENT REGISTRATION++++++")
        print("1. Register Student")
        print("2. Exit")
        print("+++++++++++++++++++++++++++++++++++++")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_student()

        elif choice == "2":
            print("GoodBye!!")
            break

        else:
            print("Choose any of these options.")

if __name__ == "__main__":
    main()