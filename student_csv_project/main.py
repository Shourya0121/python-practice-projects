import csv


def read_students():
    students = []
    try:
        with open("students.csv", "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                students.append(row)
                
    except FileNotFoundError:
        print("Error: students.csv file not found.")
    return students


def process_students(students):
    processed_students = []

    for student in students:
        name = student["name"]
        age = int(student["age"])
        marks = int(student["marks"])

        if marks >= 90:
            grade = "A"
        elif marks >= 75:
            grade = "B"
        elif marks >= 60:
            grade = "C"
        elif marks >= 40:
            grade = "D"
        else:
            grade = "F"

        result = "Pass" if marks >= 40 else "Fail"

        processed_student = {
            "name": name,
            "age": age,
            "marks": marks,
            "grade": grade,
            "result": result,
        }
        processed_students.append(processed_student)

    return processed_students


def display_students(students):
    print("\n======= STUDENTS RESULTS =======")

    for student in students:
        print(
            f"Name: {student['name']} | "
            f"Age: {student['age']} | "
            f"Marks: {student['marks']} | "
            f"Grade: {student['grade']} | "
            f"Result: {student['result']}"
        )

    print("=================================")


def write_output(students):
    with open("output.csv", "w", newline="") as file:
        fieldnames = ["name", "age", "marks", "grade", "result"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)

    print("\nOutput successfully written to output.csv")


def main():
    students = read_students()

    if not students:
        print("No students data found.")
        return

    processed_students = process_students(students)
    display_students(processed_students)
    write_output(processed_students)


if __name__ == "__main__":
    main()
