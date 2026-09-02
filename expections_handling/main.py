class NegativeAgeError(Exception):
    pass

try:
    age = int(input("Enter your age: "))

    if age < 0:
      raise NegativeAgeError("Age cannot be negative")

    print("Your age is: ", age)

except ValueError:
   print("Please eneter valid age")

except NegativeAgeError as error:
   print(error)
finally:
   print("Age checking completed!")