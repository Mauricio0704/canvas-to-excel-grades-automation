import argparse
from set_up import set_up_sheet
from write_grades_logic import *


def main():
    parser = argparse.ArgumentParser(description="Fetch and store student grades from Canvas.")
    parser.add_argument("--setup", action="store_true", help="Run Google Sheets setup")
    parser.add_argument("--course_id", help="Course ID from Canvas")
    parser.add_argument("--assignment_id", help="List of Assignment IDs")
    args = parser.parse_args()
    
    if args.setup:
        print("Setting up sheet...")
        set_up_sheet()
        return

    course_id = args.course_id
    assignment_id = args.assignment_id

    if not course_id:
        print("Error: --course_id is required unless using --setup.")
        return
    
    if not assignment_id:
        print("Error: --assignment_id is required unless using --setup.")
        return
    
    if assignment_id == "all" and course_id == "all":
        print("Writing grades of all assignments of all courses...")
        write_grades_of_all_assignments_of_all_courses()
    elif assignment_id == "all":
        print(f"Writing grades of all assignments of course {course_id}...")
        write_grades_of_all_assignments_of_course(course_id)
    elif course_id == "all":
        print(f"Writing grades of assignment {assignment_id} of all courses...")
        write_grades_of_assignment_of_all_courses(int(assignment_id))
    else:
        print(f"Writing grades of assignment {assignment_id} of course {course_id}...")
        write_grades_of_assignment_of_course(course_id, int(assignment_id))
    print("Done.")
       

if __name__ == "__main__":
    main()