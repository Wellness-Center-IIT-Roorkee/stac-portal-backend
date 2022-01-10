def get_new_application_mail(application):
    email = """Dear Professor

{}, pursuing PhD from your department, has applied for Financial Aid through StAC. Kindly approve their application from your side by heading  on to https://stac.iitr.ac.in .

Regards

Amit Khantwal
Office of ADOSW (SW)
Phone No. 01332285097
    """

    email = email.format(application.student.user.name)
    return email


def get_update_application_mail(application):
    email = """Dear Professor

{}, pursuing PhD from your department, has updated their application for Financial Aid through StAC. Kindly approve their application from your side by heading  on to https://stac.iitr.ac.in .

Regards

Amit Khantwal
Office of ADOSW (SW)
Phone No. 01332285097
    """

    email = email.format(application.student.user.name)
    return email
