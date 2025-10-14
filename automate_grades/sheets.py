import time
from gspread.exceptions import APIError
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv
load_dotenv()

SHEET_ID = os.getenv("SHEET_ID")
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME")

from sheets_service import get_worksheet, get_service

sheet = get_worksheet(SHEET_ID, WORKSHEET_NAME)
service = get_service()

def get_rows_of_students(courseID, students_ids):
    student_rows = {}

    for _ in range(4):
        try:
            course_rows = sheet.findall(f"{courseID}")
        except Exception:
            # print("Retrying to find course rows...")
            time.sleep(15)
        else:
            break


    if not course_rows: return None

    row_range = range(course_rows[0].row, course_rows[-1].row + 1)

    for student_id in students_ids:
        for _ in range(4):
            try:
                student_possible_cell = sheet.findall(f"{student_id}", in_column=4)
            except Exception:
                # print("Retrying to find student possible cell...")
                time.sleep(15)
            else:
                break

        student_cell = [student for student in student_possible_cell if student.row in row_range]

        if student_cell: student_rows[student_id] = student_cell[0].row

    return student_rows

def write_grades_of_assignment(column, grades, student_rows):
    sheet_id = sheet._properties['sheetId']
    assignment_col = column + 5
    
    baseTextFormatDict = {
        "bold": False,
        "fontSize": 10,
        "fontFamily": "Calibri"
    }

    full_cell_requests = []

    for student_id, student_info in grades.items():
        textFormatDict = baseTextFormatDict.copy()

        for _ in range(4):
            try:
                student_row = student_rows.get(student_id, None)
            except APIError:
                print("Trying to get student row...")
                time.sleep(15)
            else:
                break

        if not student_row: 
            print(f"El estudiante con ID: {student_id} no se encontró en la hoja de datos")
            continue

        # print(f"Student ID: {student_id}, Row: {student_row}, Grade: {student_info['grade']}")

        textFormatDict["bold"] = False
        note = ''
        
        if student_info['grade'] == -1:
            valueDict = {"stringValue": ''}
            backgroundColorDict = {"red": 1, "green": 0.67843137, "blue": 0.67843137} if assignment_col not in [11, 17, 22] else {
                "red": 0.9254901960784314,
                "green": 0.8941176470588236,
                "blue": 0.9764705882352941
            }
        elif student_info['grade'] == -2:
            valueDict = {"stringValue": 'p'}
            backgroundColorDict = {"red": 0.639, "green": 0.769, "blue": 0.953}
            textFormatDict["bold"] = True
        else:
            valueDict = {"numberValue": student_info['grade']}
            backgroundColorDict = {"red": 1, "green": 1, "blue": 1}

        formatDict = {
            "backgroundColor": backgroundColorDict,
            "textFormat": textFormatDict,
            "horizontalAlignment": "CENTER"
        }

        if isinstance(student_info['grade'], (int, float)) and student_info['grade'] < 50 and 'comment' in student_info:
            note = student_info['comment']

        full_cell_requests.append({
            "updateCells": {
                "rows": [{
                    "values": [{
                        "userEnteredValue": valueDict,
                        "userEnteredFormat": formatDict,
                        "note": note
                    }]
                }],
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment),userEnteredValue,note",
                "start": {
                    "sheetId": sheet_id,
                    "rowIndex": student_row - 1,
                    "columnIndex": assignment_col - 1
                }
            }
        })

    if full_cell_requests:
        for _ in range(4):
            try:
                service.spreadsheets().batchUpdate(
                    spreadsheetId=SHEET_ID,
                    body={"requests": full_cell_requests}
                ).execute()
            except HttpError as e:
                # print("Rate limit exceeded. Retrying...")
                time.sleep(15)
            else:
                break