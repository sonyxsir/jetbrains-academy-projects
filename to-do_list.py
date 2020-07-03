from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


Base = declarative_base()
weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default="default")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def print_todays_tasks():
    rows = session.query(Task).filter(Task.deadline == datetime.today().date()).all()
    print(f"\nToday {datetime.today().day} {datetime.today().strftime('%b')}:")
    if rows:
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i]}.")
        print()
    else:
        print("Nothing to do!\n")


def print_weeks_tasks():
    for j in range(7):
        day = datetime.today() + timedelta(days=j)
        print(f"\n{weekdays[day.weekday()]} {day.day} {day.strftime('%b')}:")
        rows = session.query(Task).filter(Task.deadline == day.date()).all()
        if rows:
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i]}.")
        else:
            print("Nothing to do!")
    print()


def print_all_tasks():
    rows = session.query(Task).order_by(Task.deadline).all()
    print("\nAll tasks:")
    if rows:
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i]}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
        print()
    else:
        print("Nothing to do!\n")


def print_missed_tasks():
    rows = session.query(Task).filter(Task.deadline < datetime.today().date()).order_by(Task.deadline).all()
    print("\nMissed tasks:")
    if rows:
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i]}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
        print()
    else:
        print("Nothing is missed!\n")


def add_task():
    print("\nEnter task")
    task = input(">")
    print("Enter deadline")
    deadline = input(">")
    new_task = Task(task=task, deadline=datetime.strptime(deadline, "%Y-%m-%d").date())
    session.add(new_task)
    session.commit()
    print("The task has been added!\n")


def delete_task():
    rows = session.query(Task).order_by(Task.deadline).all()
    print("\nChose the number of the task you want to delete:")
    if rows:
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i]}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
    else:
        print("Nothing to delete!\n")
    id_ = int(input("> "))
    try:
        session.delete(rows[id_ - 1])
        session.commit()
        print("The task has been deleted!\n")
    except IndexError:
        print("Wrong choice!\n")


def perform_action(choice):
    if choice == "1":
        print_todays_tasks()
    elif choice == "2":
        print_weeks_tasks()
    elif choice == "3":
        print_all_tasks()
    elif choice == "4":
        print_missed_tasks()
    elif choice == "5":
        add_task()
    elif choice == "6":
        delete_task()
    elif choice == "0":
        print("\nBye!")
    else:
        print("\nWrong choice!\n")


if __name__ == "__main__":
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    user_choice = ""
    while user_choice != "0":
        print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        user_choice = input("> ")
        perform_action(user_choice)
