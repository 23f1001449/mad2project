from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from models import db, PlacementDrive, Application, StudentProfile, User, Company
from flask_mail import Message, Mail




def send_deadline_reminders(app, mail: Mail):

    with app.app_context():

        # print("Scheduler job running at:", datetime.now())

        
        today = datetime.now()
        tomorrow = today + timedelta(days=1)

        drives = PlacementDrive.query.filter(
            PlacementDrive.deadline >= today
        ).all()

        print("Scheduler job running at:", datetime.now())

        for drive in drives:
            applications = Application.query.filter_by(drive_id=drive.id).all()

            for appn in applications:
                profile = StudentProfile.query.get(appn.student_id)
                user = User.query.get(profile.user_id)

                msg = Message(
                    subject="Placement Drive Deadline Reminder",
                    recipients=[user.email],
                    body=f"""
                            Hello {user.username},

                            Reminder: The deadline for the placement drive "{drive.job_title}"  is approaching.

                            Deadline: {drive.deadline}

                            Placement Portal
                        """
                )
                print("Sending reminder to:", user.email)
                try:
                    mail.send(msg)
                except Exception as e:
                    print("",flush=True)


# def start_scheduler(app, mail):

#     scheduler = BackgroundScheduler()

    

#     # scheduler.add_job(
#     #     func=lambda: send_deadline_reminders(app, mail),
#     #     trigger="interval",
#     #     seconds=30
#     # )

#     scheduler.start()




def generate_monthly_report(app, mail: Mail):
    with app.app_context():
        
        now = datetime.now()
        first_day_of_last_month = datetime(now.year, now.month-1 if now.month>1 else 12, 1)
        last_day_of_last_month = datetime(now.year, now.month, 1) - timedelta(days=1)

        
        drives = PlacementDrive.query.filter(
            PlacementDrive.deadline >= first_day_of_last_month,
            PlacementDrive.deadline <= last_day_of_last_month
        ).all()

        total_drives = len(drives)
        total_applications = 0
        total_selected = 0

        for drive in drives:
            applications = Application.query.filter_by(drive_id=drive.id).all()
            total_applications += len(applications)
            total_selected += len([a for a in applications if a.status == "Selected"])


        html = f"""
        <html>
        <body>
            <h2>Monthly Placement Activity Report</h2>
            <p>Report Period: {first_day_of_last_month.date()} to {last_day_of_last_month.date()}</p>
            <ul>
                <li><b>Number of Drives Conducted:</b> {total_drives}</li>
                <li><b>Total Applications:</b> {total_applications}</li>
                <li><b>Total Students Selected:</b> {total_selected}</li>
            </ul>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
        </html>
        """

       
        admin = User.query.filter_by(role="admin").first()
        if admin:
            msg = Message(
                subject="Monthly Placement Activity Report",
                recipients=[admin.email],
                html=html
            )
            try:
                mail.send(msg)
                print("Monthly report sent to admin:", admin.email)
            except Exception as e:
                print("")
        else:
            print("No admin found to send report.")



def start_scheduler(app, mail):
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        func=lambda: generate_monthly_report(app, mail),
        trigger="cron",
        day=1,
        hour=9,
        minute=0
    )

    scheduler.add_job(
        func=lambda: send_deadline_reminders(app, mail),
        trigger="cron",
        hour=9,
        minute=0
    )

    # scheduler.add_job(
    #     func=lambda: generate_monthly_report(app, mail),
    #     trigger="interval",
    #     seconds=30
    # )

    scheduler.start()




import csv, io
from models import db, Application, PlacementDrive, Company, User


def export_applications_csv(user_id, mail, app):
    with app.app_context():
        student = User.query.get(user_id)
        if not student:
            print("Student not found")
            return

        profile = StudentProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            print("Student profile not found")
            return
        
        applications = Application.query.filter_by(student_id=profile.id).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Student ID", "Company Name", "Drive Title", "Application Date", "Status", "Interview Date"])
        
        for appn in applications:
            drive = PlacementDrive.query.get(appn.drive_id)
            company = Company.query.get(drive.company_id)
            writer.writerow([student.id, company.company_name, drive.job_title, appn.application_date, appn.status, appn.interview_date])
        
        csv_data = output.getvalue()
        output.close()

        msg = Message(
            subject="Your Placement Applications Export",
            recipients=[student.email],
            body=f"Hello {student.username},\n\nYour applications export is ready.",
        )
        msg.attach("applications.csv", "text/csv", csv_data)
        try:
            print("CSV export sending:", student.email)
            mail.send(msg)
            print("CSV export sent to student:", student.email)
        except Exception as e:
            print("")
        print(f"CSV export sent to {student.email}")

        