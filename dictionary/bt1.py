def student_input():
    n = int(input("Nhập số lượng sinh viên cần quản lý: "))
    students = []

    for i in range(n):
        print(f"Nhập sinh viên thứ {i + 1}: ")
        name = input("Tên sinh viên: ")
        while True:
            try:
                grade = float(input("Nhập điểm của sinh viên: "))
                if 0 < grade <= 10:
                    break
                else:
                    print("Điểm phải lớn hơn 0 và nhỏ hơn hoặc bằng 10. Vui lòng nhập lại.")
            except ValueError:
                print("Vui lòng nhập số hợp lệ cho điểm.")

        students.append({
            "name": name,
            "grade": grade
        })
    return students

def find_max_grade(students):
    if not students:
        print("Danh sách sinh viên trống.")
        return

    maxGrade = students[0]
    for student in students[1:]:
        if student["grade"] > maxGrade["grade"]:
            maxGrade = student
    print(f"Sinh viên có điểm cao nhất là: {maxGrade['name']}, điểm: {maxGrade['grade']}")

students = student_input()

print("--------------------------------------------------")
for student in students:
    print(f"Thông tin của sinh viên: {student['name']}, điểm {student['grade']}.")
print("--------------------------------------------------")
find_max_grade(students)
