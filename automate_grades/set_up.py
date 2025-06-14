import time
from sheets_config import SHEET_ID, WORKSHEET_NAME
from sheets_service import get_worksheet
from utils import get_courses, get_students_by_sections, get_sections


def set_up_sheet():
    sheet = get_worksheet(SHEET_ID, WORKSHEET_NAME)
    sheet.clear()

    sheet.append_row([
        "ID Materia", "Grupo", "Materia", "ID Alumno", "Nombre Alumno",
        "Semana 1", "Semana 2", "Semana 3", "Semana 4", "Integradora - Fase 1", "Examen 1", 
        "Semana 6", "Semana 7", "Semana 8", "Semana 9", "Integradora - Fase 2", "Examen 2",
        "Semana 11", "Semana 12", "Semana 13", "Integradora - Fase 3", "Examen 3",
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