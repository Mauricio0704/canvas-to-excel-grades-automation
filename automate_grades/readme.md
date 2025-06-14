Changed from a thing like this:
for student in students:
  update_cell(student_info)

to somethin like this:

updates = []
for student in students:
  updates.append(student_info)

batch update(updates)



Previous code of sheets.py:
sheet_id = sheet._properties['sheetId']
    assignment_col = column + 6

    for student_id, student_info in grades.items():
        for _ in range(4):
            try:
                student_row = student_rows.get(student_id, None)
            except Exception:
                print("Trying to get student row...")
                time.sleep(15)
            else:
                break
                
        print(f"Student ID: {student_id}, Row: {student_row}, Grade: {student_info['grade']}")
        if student_row: 
            for _ in range(4):
                try:
                    if student_info['grade'] == -1:
                        grade_to_write = ''
                    elif student_info['grade'] == -2:
                        grade_to_write = 'p'
                    else:
                        grade_to_write = student_info['grade']
                        
                    sheet.update_cell(student_row, assignment_col, grade_to_write)

                    apply_format(student_info['grade'], assignment_col, student_row)

                    if int(float(student_info['grade'])) <= 50 and 'comment' in student_info:
                        add_note_to_cell(
                            service=service,
                            spreadsheet_id=SHEET_ID,
                            sheet_id=sheet_id,
                            row_index=student_row - 1,       
                            col_index=assignment_col - 1,
                            note=student_info['comment']
                        )
                except (APIError, HttpError) as e:  
                    print("Retrying to update cell...")
                    time.sleep(15)
                except ValueError as e_val:
                    raise e_val
                else:
                    break



this allowed me to pass from ~6hours to less than 20mins