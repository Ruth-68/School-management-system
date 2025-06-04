import json
import os
from datetime import datetime

DATA_DIR = "data"
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
TEACHERS_FILE = os.path.join(DATA_DIR, "teachers.json")
SUBJECTS_FILE = os.path.join(DATA_DIR, "subjects.json")
GRADES_FILE = os.path.join(DATA_DIR, "grades.json")
ENROLLMENTS_FILE = os.path.join(DATA_DIR, "enrollments.json")
SCORES_FILE = os.path.join(DATA_DIR, "scores.json")

def ensure_data_dir():
	if not os.path.exists(DATA_DIR):
		os.makedirs(DATA_DIR)

def load_data(filename):
	if not os.path.exists(filename):
		return []
	with open(filename, "r") as f:
		return json.load(f)

def save_data(filename, data):
	with open(filename, "w") as f:
		json.dump(data, f, indent=2)

def input_nonempty(prompt):
	while True:
		value = input(prompt).strip()
		if value:
			return value
		print("Input cannot be empty.")

def input_numeric(prompt):
	while True:
		value = input(prompt).strip()
		if value.isdigit():
			return value
		print("Input must be numeric.")

def pause():
	input("\nPress Enter to continue...")

class Student:
	@staticmethod
	def add():
		students = load_data(STUDENTS_FILE)
		student_id = input_numeric("Enter Student ID: ")
		if any(s['id'] == student_id for s in students):
			print("Student ID already exists.")
			return
		name = input_nonempty("Enter Name: ")
		grade = input_nonempty("Enter Grade: ")
		dob = input_nonempty("Enter Date of Birth (YYYY-MM-DD): ")
		gender = input_nonempty("Enter Gender: ")
		phone = input_nonempty("Enter Phone: ")
		students.append({
			"id": student_id,
			"name": name,
			"grade": grade,
			"dob": dob,
			"gender": gender,
			"phone": phone
		})
		save_data(STUDENTS_FILE, students)
		print("Student added successfully.")

	@staticmethod
	def view_all():
		students = load_data(STUDENTS_FILE)
		if not students:
			print("No students found.")
			return
		for s in students:
			print(s)

	@staticmethod
	def update():
		students = load_data(STUDENTS_FILE)
		student_id = input_numeric("Enter Student ID to update: ")
		for s in students:
			if s['id'] == student_id:
				print("Leave blank to keep current value.")
				name = input(f"Name ({s['name']}): ").strip() or s['name']
				grade = input(f"Grade ({s['grade']}): ").strip() or s['grade']
				dob = input(f"DOB ({s['dob']}): ").strip() or s['dob']
				gender = input(f"Gender ({s['gender']}): ").strip() or s['gender']
				phone = input(f"Phone ({s['phone']}): ").strip() or s['phone']
				s.update({"name": name, "grade": grade, "dob": dob, "gender": gender, "phone": phone})
				save_data(STUDENTS_FILE, students)
				print("Student updated.")
				return
		print("Student not found.")

	@staticmethod
	def delete():
		students = load_data(STUDENTS_FILE)
		student_id = input_numeric("Enter Student ID to delete: ")
		new_students = [s for s in students if s['id'] != student_id]
		if len(new_students) == len(students):
			print("Student not found.")
		else:
			save_data(STUDENTS_FILE, new_students)
			print("Student deleted.")

	@staticmethod
	def search():
		students = load_data(STUDENTS_FILE)
		term = input_nonempty("Enter Student Name or ID to search: ").lower()
		found = [s for s in students if term in s['id'].lower() or term in s['name'].lower()]
		if not found:
			print("No matching students found.")
		else:
			for s in found:
				print(s)

class Teacher:
	@staticmethod
	def add():
		teachers = load_data(TEACHERS_FILE)
		teacher_id = input_numeric("Enter Teacher ID: ")
		if any(t['id'] == teacher_id for t in teachers):
			print("Teacher ID already exists.")
			return
		name = input_nonempty("Enter Name: ")
		qualification = input_nonempty("Enter Qualification: ")
		subjects = input_nonempty("Enter Subjects (comma separated): ")
		phone = input_nonempty("Enter Phone: ")
		teachers.append({
			"id": teacher_id,
			"name": name,
			"qualification": qualification,
			"subjects": [s.strip() for s in subjects.split(",")],
			"phone": phone,
			"grades": []
		})
		save_data(TEACHERS_FILE, teachers)
		print("Teacher added.")

	@staticmethod
	def assign_to_grade():
		teachers = load_data(TEACHERS_FILE)
		grades = load_data(GRADES_FILE)
		teacher_id = input_numeric("Enter Teacher ID: ")
		grade = input_nonempty("Enter Grade to assign: ")
		if not any(g['name'] == grade for g in grades):
			print("Grade does not exist.")
			return
		for t in teachers:
			if t['id'] == teacher_id:
				if grade not in t.get('grades', []):
					t.setdefault('grades', []).append(grade)
					save_data(TEACHERS_FILE, teachers)
					print("Grade assigned to teacher.")
				else:
					print("Teacher already assigned to this grade.")
				return
		print("Teacher not found.")

	@staticmethod
	def view_update():
		teachers = load_data(TEACHERS_FILE)
		teacher_id = input_numeric("Enter Teacher ID to view/update: ")
		for t in teachers:
			if t['id'] == teacher_id:
				print(t)
				print("Leave blank to keep current value.")
				name = input(f"Name ({t['name']}): ").strip() or t['name']
				qualification = input(f"Qualification ({t['qualification']}): ").strip() or t['qualification']
				subjects = input(f"Subjects ({', '.join(t['subjects'])}): ").strip()
				phone = input(f"Phone ({t['phone']}): ").strip() or t['phone']
				if subjects:
					t['subjects'] = [s.strip() for s in subjects.split(",")]
				t.update({"name": name, "qualification": qualification, "phone": phone})
				save_data(TEACHERS_FILE, teachers)
				print("Teacher updated.")
				return
		print("Teacher not found.")

	@staticmethod
	def delete():
		teachers = load_data(TEACHERS_FILE)
		teacher_id = input_numeric("Enter Teacher ID to delete: ")
		new_teachers = [t for t in teachers if t['id'] != teacher_id]
		if len(new_teachers) == len(teachers):
			print("Teacher not found.")
		else:
			save_data(TEACHERS_FILE, new_teachers)
			print("Teacher deleted.")

class Subject:
	@staticmethod
	def add():
		subjects = load_data(SUBJECTS_FILE)
		name = input_nonempty("Enter Subject Name: ")
		if any(s['name'].lower() == name.lower() for s in subjects):
			print("Subject already exists.")
			return
		subjects.append({"name": name, "grades": []})
		save_data(SUBJECTS_FILE, subjects)
		print("Subject added.")

	@staticmethod
	def view():
		subjects = load_data(SUBJECTS_FILE)
		if not subjects:
			print("No subjects found.")
			return
		for s in subjects:
			print(s)

	@staticmethod
	def assign_to_grade():
		subjects = load_data(SUBJECTS_FILE)
		grades = load_data(GRADES_FILE)
		name = input_nonempty("Enter Subject Name: ")
		grade = input_nonempty("Enter Grade to assign: ")
		if not any(g['name'] == grade for g in grades):
			print("Grade does not exist.")
			return
		for s in subjects:
			if s['name'].lower() == name.lower():
				if grade not in s['grades']:
					s['grades'].append(grade)
					save_data(SUBJECTS_FILE, subjects)
					print("Subject assigned to grade.")
				else:
					print("Subject already assigned to this grade.")
				return
		print("Subject not found.")

class Grade:
	@staticmethod
	def add():
		grades = load_data(GRADES_FILE)
		name = input_nonempty("Enter Grade Name: ")
		if any(g['name'].lower() == name.lower() for g in grades):
			print("Grade already exists.")
			return
		grades.append({"name": name})
		save_data(GRADES_FILE, grades)
		print("Grade added.")

	@staticmethod
	def view():
		grades = load_data(GRADES_FILE)
		if not grades:
			print("No grades found.")
			return
		for g in grades:
			print(g)

	@staticmethod
	def update():
		grades = load_data(GRADES_FILE)
		name = input_nonempty("Enter Grade Name to update: ")
		for g in grades:
			if g['name'].lower() == name.lower():
				new_name = input_nonempty("Enter new Grade Name: ")
				g['name'] = new_name
				save_data(GRADES_FILE, grades)
				print("Grade updated.")
				return
		print("Grade not found.")

	@staticmethod
	def delete():
		grades = load_data(GRADES_FILE)
		name = input_nonempty("Enter Grade Name to delete: ")
		new_grades = [g for g in grades if g['name'].lower() != name.lower()]
		if len(new_grades) == len(grades):
			print("Grade not found.")
		else:
			save_data(GRADES_FILE, new_grades)
			print("Grade deleted.")

class Enrollment:
	@staticmethod
	def enroll():
		enrollments = load_data(ENROLLMENTS_FILE)
		students = load_data(STUDENTS_FILE)
		grades = load_data(GRADES_FILE)
		student_id = input_numeric("Enter Student ID: ")
		grade = input_nonempty("Enter Grade to enroll: ")
		if not any(s['id'] == student_id for s in students):
			print("Student not found.")
			return
		if not any(g['name'] == grade for g in grades):
			print("Grade not found.")
			return
		if any(e['student_id'] == student_id and e['grade'] == grade for e in enrollments):
			print("Student already enrolled in this grade.")
			return
		enrollments.append({
			"student_id": student_id,
			"grade": grade,
			"date": datetime.now().strftime("%Y-%m-%d")
		})
		save_data(ENROLLMENTS_FILE, enrollments)
		print("Student enrolled.")

	@staticmethod
	def view_history():
		enrollments = load_data(ENROLLMENTS_FILE)
		student_id = input_numeric("Enter Student ID: ")
		history = [e for e in enrollments if e['student_id'] == student_id]
		if not history:
			print("No enrollment history found.")
		else:
			for e in history:
				print(e)

class Score:
	@staticmethod
	def view_all():
		scores = load_data(SCORES_FILE)
		students = load_data(STUDENTS_FILE)
		if not scores:
			print("No scores found.")
			return
		for s in students:
			student_scores = [sc for sc in scores if sc['student_id'] == s['id']]
			print(f"Student {s['name']} ({s['id']}):")
			for sc in student_scores:
				print(f"  Subject: {sc['subject']}, Score: {sc['score']}, Teacher: {sc['teacher_id']}")

	@staticmethod
	def view_by_student():
		scores = load_data(SCORES_FILE)
		student_id = input_numeric("Enter Student ID: ")
		student_scores = [sc for sc in scores if sc['student_id'] == student_id]
		if not student_scores:
			print("No scores found for this student.")
		else:
			for sc in student_scores:
				print(sc)

	@staticmethod
	def view_by_teacher():
		scores = load_data(SCORES_FILE)
		teacher_id = input_numeric("Enter Teacher ID: ")
		teacher_scores = [sc for sc in scores if sc['teacher_id'] == teacher_id]
		if not teacher_scores:
			print("No scores found for this teacher.")
		else:
			for sc in teacher_scores:
				print(sc)

class Reports:
	@staticmethod
	def students_by_grade():
		students = load_data(STUDENTS_FILE)
		grade = input_nonempty("Enter Grade: ")
		filtered = [s for s in students if s['grade'] == grade]
		if not filtered:
			print("No students found in this grade.")
		else:
			for s in filtered:
				print(s)

	@staticmethod
	def student_report_card():
		scores = load_data(SCORES_FILE)
		students = load_data(STUDENTS_FILE)
		student_id = input_numeric("Enter Student ID: ")
		student = next((s for s in students if s['id'] == student_id), None)
		if not student:
			print("Student not found.")
			return
		print(f"Report Card for {student['name']} ({student['id']}):")
		student_scores = [sc for sc in scores if sc['student_id'] == student_id]
		if not student_scores:
			print("No scores found.")
		else:
			for sc in student_scores:
				print(f"Subject: {sc['subject']}, Score: {sc['score']}")

	@staticmethod
	def totals():
		students = load_data(STUDENTS_FILE)
		teachers = load_data(TEACHERS_FILE)
		subjects = load_data(SUBJECTS_FILE)
		print(f"Total Students: {len(students)}")
		print(f"Total Teachers: {len(teachers)}")
		print(f"Total Subjects: {len(subjects)}")

def student_menu():
	while True:
		print("\n--- Student Menu ---")
		print("1. Add Student")
		print("2. View All Students")
		print("3. Update Student")
		print("4. Delete Student")
		print("5. Search Student")
		print("6. Back to Main Menu")
		choice = input("Choose an option: ")
		if choice == "1":
			Student.add()
		elif choice == "2":
			Student.view_all()
		elif choice == "3":
			Student.update()
		elif choice == "4":
			Student.delete()
		elif choice == "5":
			Student.search()
		elif choice == "6":
			break
		else:
			print("Invalid choice.")
		pause()

def teacher_menu():
	while True:
		print("\n--- Teacher Menu ---")
		print("1. Add Teacher")
		print("2. Assign Teacher to Grade")
		print("3. View/Update Teacher")
		print("4. Delete Teacher")
		print("5. Back to Main Menu")
		choice = input("Choose an option: ")
		if choice == "1":
			Teacher.add()
		elif choice == "2":
			Teacher.assign_to_grade()
		elif choice == "3":
			Teacher.view_update()
		elif choice == "4":
			Teacher.delete()
		elif choice == "5":
			break
		else:
			print("Invalid choice.")
		pause()

def subject_menu():
	while True:
		print("\n--- Subject Menu ---")
		print("1. Add Subject")
		print("2. View Subjects")
		print("3. Assign Subject to Grade")
		print("4. Back to Main Menu")
		choice = input("Choose an option: ")
		if choice == "1":
			Subject.add()
		elif choice == "2":
			Subject.view()
		elif choice == "3":
			Subject.assign_to_grade()
		elif choice == "4":
			break
		else:
			print("Invalid choice.")
		pause()

def grade_menu():
	while True:
		print("\n--- Grade Menu ---")
		print("1. Add Grade")
		print("2. View Grades")
		print("3. Update Grade")
		print("4. Delete Grade")
		print("5. Back to Main Menu")
		choice = input("Choose an option: ")
		if choice == "1":
			Grade.add()
		elif choice == "2":
			Grade.view()
		elif choice == "3":
			Grade.update()
		elif choice == "4":
			Grade.delete()
		elif choice == "5":
			break
		else:
			print("Invalid choice.")
		pause()

def enrollment_menu():
	while True:
		print("\n--- Enrollment Menu ---")
		print("1. Enroll Student")
		print("2. View Enrollment History")
		print("3. Back to Main Menu")
		choice = input("Choose an option: ")
		if choice == "1":
			Enrollment.enroll()
		elif choice == "2":
			Enrollment.view_history()
		elif choice == "3":
			break
		else:
			print("Invalid choice.")
		pause()

def score_menu():
	while True:
		print("\n--- Score Menu ---")
		print("1. View All Scores")
		print("2. View Scores by Student")
		print("3. View Scores by Teacher")
		print("4. Back to Main Menu")
		choice = input("Choose an option: ")
		if choice == "1":
			Score.view_all()
		elif choice == "2":
			Score.view_by_student()
		elif choice == "3":
			Score.view_by_teacher()
		elif choice == "4":
			break
		else:
			print("Invalid choice.")
		pause()

def reports_menu():
	while True:
		print("\n--- Reports Menu ---")
		print("1. List Students by Grade")
		print("2. Student Report Card")
		print("3. Totals")
		print("4. Back to Main Menu")
		choice = input("Choose an option: ")
		if choice == "1":
			Reports.students_by_grade()
		elif choice == "2":
			Reports.student_report_card()
		elif choice == "3":
			Reports.totals()
		elif choice == "4":
			break
		else:
			print("Invalid choice.")
		pause()

def main_menu():
	ensure_data_dir()
	while True:
		print("\n=== School Management System ===")
		print("1. Student Management")
		print("2. Teacher Management")
		print("3. Subject Management")
		print("4. Grade Management")
		print("5. Enrollment System")
		print("6. Score Management")
		print("7. Reports & Summaries")
		print("8. Exit")
		choice = input("Choose an option: ")
		if choice == "1":
			student_menu()
		elif choice == "2":
			teacher_menu()
		elif choice == "3":
			subject_menu()
		elif choice == "4":
			grade_menu()
		elif choice == "5":
			enrollment_menu()
		elif choice == "6":
			score_menu()
		elif choice == "7":
			reports_menu()
		elif choice == "8":
			print("Goodbye!")
			break
		else:
			print("Invalid choice.")
		pause()

if __name__ == "__main__":
	main_menu()