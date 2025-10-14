from collections import defaultdict
from canvas_service import make_canvas_request

def get_courses(): 
    return make_canvas_request("/courses", {"per_page": 100})

def get_sections(course_id):
    return make_canvas_request(f"/courses/{course_id}/sections", {"per_page": 100})


def get_students_by_sections(section_id):
    enrollments = make_canvas_request(
        f"/sections/{section_id}/enrollments",
        params={"role": "StudentEnrollment", "state[]": "active", "per_page": 50}
    )
    if not enrollments:
        return None
    return [e for e in enrollments if e["enrollment_state"] == "active"]

def get_students_by_course(course_id):
    return make_canvas_request(f"/courses/{course_id}/users", params={"type[]": "StudentEnrollment", "status[]": "active", "per_page": 100}) 

def get_assignments(course_id):
    return make_canvas_request(f"/courses/{course_id}/assignments", {"per_page": 16})
    

def get_submissions_of_assingment(course_id, assignment_id):
    return make_canvas_request(f"/courses/{course_id}/assignments/{assignment_id}/submissions?include[]=submission_comments", params={"per_page": 100})


def get_grades_of_assignment(course_id, assignment):
    if not assignment: return None

    submissions = get_submissions_of_assingment(course_id, assignment['id'])
    if not submissions: return None

    grades_dict = defaultdict(dict)

    for submission in submissions:
        if submission['grade']:
            grades_dict[submission['user_id']]['grade'] = float(submission['grade'])
        elif submission['submitted_at'] is None:
            grades_dict[submission['user_id']]['grade'] = -1
        else:
            grades_dict[submission['user_id']]['grade'] = -2

        if len(submission["submission_comments"]) > 0 and grades_dict[submission['user_id']]['grade'] != -1:
            grades_dict[submission['user_id']]['comment'] = get_tutor_first_comment(submission)
             

    return grades_dict

def get_tutor_first_comment(submission):
    for comment in submission["submission_comments"]:
        if comment['author_id'] != submission['user_id']:
            return comment['comment']
    return ''