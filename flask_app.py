from flask import Flask, render_template, request

app = Flask(__name__)

# Grade conversion
grade_to_gpa = {
    "AA": 4.0, "BA": 3.5, "BB": 3.0, "CB": 2.5, "CC": 2.0,
    "DC": 1.5, "DD": 1.0, "FD": 0.5, "FF": 0.0
}
# Elective courses with variable credits (add these to your existing core_courses)
variable_credit_courses = [
    "Free Elective",
    "Technical Elective",
    "Restricted Elective",
    "Nondepartmental Elective"
]
# Core courses (8 semesters)
core_courses = {
    1: [("PHYS107", 2), ("PHYS109", 5), ("CHEM101", 5), ("MATH119", 5), ("ENG101", 4)],
    2: [("PHYS108", 2), ("PHYS110", 5), ("CHEM102", 5), ("MATH120", 5), ("ENG102", 4)],
    3: [("PHYS200", 3), ("PHYS203", 4), ("PHYS209", 4), ("PHYS221", 4), ("MATH260", 3)],
    4: [("PHYS202", 4), ("PHYS210", 4), ("PHYS222", 3), ("ENG211", 3), ("Free Elective", 6)],
    5: [("PHYS307", 3), ("PHYS331", 4), ("PHYS335", 4), ("Nondepartmental Elective", 6)],
    6: [("PHYS300", 4), ("PHYS332", 4), ("PHYS336", 4), ("ENG311", 3), ("Restricted Elective", 6)],
    7: [("PHYS400", 3), ("PHYS430", 4), ("PHYS431", 4), ("Restricted Elective", 6), ("Technical Elective", 6)],
    8: [("Nondepartmental Elective", 6), ("Restricted Elective", 6), ("Restricted Elective", 6), ("Free Elective", 6), ("Technical Elective", 6)]
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        semester = int(request.form['semester'])
        courses = []
        for i in range(1, semester + 1):
            courses.extend(core_courses[i])
        return render_template('courses.html',
                           semester=semester,
                           courses=courses,
                           grades=list(grade_to_gpa.keys()))

    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
@app.route('/calculate', methods=['POST'])
def calculate():
    semester = int(request.form['semester'])
    total_points = 0
    total_credits = 0

    for i in range(1, semester + 1):
        for course in core_courses[i]:
            course_code, default_credits = course
            grade = request.form.get(f'grade_{course_code}')

            # Get credits - fixed or variable
            if course_code in variable_credit_courses:
                credits = int(request.form.get(f'credits_{course_code}', default_credits))
            else:
                credits = default_credits

            if grade and grade in grade_to_gpa:
                total_points += grade_to_gpa[grade] * credits
                total_credits += credits

    cgpa = total_points / total_credits if total_credits > 0 else 0
    return render_template('result.html', cgpa=cgpa, semester=semester)

    for i in range(1, semester + 1):
        for course_code, credits in core_courses[i]:
            grade = request.form.get(f'grade_{course_code}')
            if grade and grade in grade_to_gpa:
                total_points += grade_to_gpa[grade] * credits
                total_credits += credits

    cgpa = total_points / total_credits if total_credits > 0 else 0
    return render_template('result.html',
                         cgpa=cgpa,
                         semester=semester)

if __name__ == '__main__':
    app.run(debug=True)