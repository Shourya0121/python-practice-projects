class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("animal makes sound!")

class dog(Animal):
        def speak(self):
            print("wooff!")

class cat(Animal):
        def speak(self):
            print("meow")

dog = dog("Bruno")
cat = cat("Kitty")

print(dog.name)
dog.speak()

print(cat.name)
cat.speak()
