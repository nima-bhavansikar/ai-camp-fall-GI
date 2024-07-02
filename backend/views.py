from django.shortcuts import render

"""
course_direction = {
    "python": {
        "title": "Python Starter Course",
        #"description": "Learn introductory Python concepts with fun themes to prepare yourself for using Python with Data.",
        "embed_url": "https://dpseigel.github.io/JupyterLiteSandbox/lab/index.html",
    },
    "course1": {
        "title": "Course 1: LinkedIn Jobs",
        #"description": "Learn a Linear Regression model with a LinkedIn Data Analytics Jobs dataset.",
        "embed_url": "https://lucasw2025.github.io/MoCourse1/lab/index.html",
    },
    "course2": {
        "title": "Course 2: Credit Card Churn",
        #"description": "Learn a Support Vector Machine with a Credit Card Churn dataset.",
        "embed_url": "https://lucasw2025.github.io/MoCourse2/lab/index.html",
    },
    "course3": {
        "title": "Course 3: Stocks",
        #"description": "Learn a Logistic Regression model with a Stock Data dataset.",
        "embed_url": "https://lucasw2025.github.io/MoCourse3/lab/index.html",
    },
}

def load_course(request, course_identifier):
    course_data = course_direction.get(course_identifier)
    context = {
        "course_data": course_data,
    }
    return render(request, "courses/course.html", context)
"""