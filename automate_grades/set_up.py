import time
from sheets_service import get_worksheet
from utils import get_courses, get_students_by_sections, get_sections
import os
from dotenv import load_dotenv
load_dotenv()

SHEET_ID = os.getenv("SHEET_ID")
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME")

def set_up_sheet():
    sheet = get_worksheet(SHEET_ID, WORKSHEET_NAME)
    sheet.clear()

    sheet.append_row([
        "ID Materia", "Gpo", "Materia", "ID Alumno", "Nombre del Alumno",
        "Sem 1 (2.5 %)", "Sem 2 (2.5 %)", "Sem 3 (2.5 %)", "Sem 4 (2.5 %)", "Integ 1 (10 %)", "1° Examen Parc (10 %)", 
        "Sem 6 (2.5 %)", "Sem 7 (2.5 %)", "Sem 8 (2.5 %)", "Sem 9 (2.5 %)", "Integ 2 (10 %)", "2° Examen Parc (10 %)",
        "Sem 11 (2.5 %)", "Sem 12 (2.5 %)", "Sem 13 (2.5 %)", "Integ 3 (10 %)", "Final (20 %)",
    ])
    courses = get_courses()

    for course in courses:
        course_id, course_name = course["id"], course["name"]
        
        sections = get_sections(course_id)

        if sections:
            for i, section in enumerate(sections):
                section_id = section["id"]
                section_number = i
                
                students = get_students_by_sections(section_id)

                if students:
                    for student in students:
                        student_id, student_name = student["user"]["id"], student["user"]["name"]

                        for _ in range(4):
                            try:
                                sheet.append_row([course_id, section_number, course_name, student_id, student_name])
                            except Exception:
                                print("Retrying to append row...")
                                time.sleep(15)
                                pass
                            else:
                                break