from utils import get_courses, get_students_by_course, get_assignments, get_grades_of_assignment
from sheets import write_grades_of_assignment, get_rows_of_students

def write_grades_of_all_assignments_of_course(course_id):
    print(f"Writing grades for all assignments of course {course_id}")
    assignments = get_assignments(course_id)
    students = get_students_by_course(course_id)

    if not students: return None

    students_ids = [student['id'] for student in students]
    student_rows = get_rows_of_students(course_id, students_ids)

    for column, assignment in enumerate(assignments):
        grades = get_grades_of_assignment(course_id, assignment)
        write_grades_of_assignment(column, grades, student_rows)

def write_grades_of_assignment_of_course(courseID, assignmentID):
    students = get_students_by_course(courseID)

    if not students: return None

    students_ids = [student['id'] for student in students]
    student_rows = get_rows_of_students(courseID, students_ids)
    grades = get_grades_of_assignment(courseID, get_assignments(courseID)[assignmentID])
    write_grades_of_assignment(assignmentID, grades, student_rows)

def write_grades_of_all_assignments_of_all_courses():
    courses = get_courses()
    print(f"Writing grades for all assignments of all courses")

    for course in courses:
        write_grades_of_all_assignments_of_course(course['id'])

def write_grades_of_assignment_of_all_courses(assignmentID):
    courses = get_courses()

    for course in courses:
        write_grades_of_assignment_of_course(course['id'], assignmentID)