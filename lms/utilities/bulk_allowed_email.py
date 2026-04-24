import pandas as pd
from account.models import AllowedEmail
from course.models import Course


def process_bulk_allowed_email(file_path):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    for index, row in df.iterrows():
        email = row['Email Id']
        name = row['Name']
        course = row['Course']

        try:
            course = Course.objects.get(code=course)
        except Exception as e:
            print(f"Error creating allowed email: {e}")
            return

        allowed_email, created = AllowedEmail.objects.get_or_create(email=email,course=course)
        allowed_email.is_allowed = True
        allowed_email.save()

        if not created:
            print(f"Email {email} already exists")
        else:
            print(f"Email {email} created successfully")


if __name__ == "__main__":
    path = 'utilities\\test_allowed_email.xlsx'
    path_main = 'utilities\\LordsUniversityBBAISem2025-26_.xlsx'
    process_bulk_allowed_email(path_main)