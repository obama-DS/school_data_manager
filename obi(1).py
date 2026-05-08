from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import time
console = Console()
"""
Student Grade Management System
"""
# STUDENT CLASS
class Student:
    def __init__( self , name , sid ):
        self.name = name
        self.student_id = sid
        self.grades = {}
    def add_grade(self, subject, grade):
        if subject in self.grades:
            self.grades[subject].append(grade)
        else:
             self.grades[subject] = [grade]
    def get_subject_average(self, subject):
        if subject not in self.grades:
            return 0
        total = 0
        count = 0
        for g in self.grades[subject]:
            total += g
            count += 1
        if count == 0:
            return 0
        return total / count
    def get_overall_average(self):
        total = 0
        count = 0
        for sub in self.grades:
            for g in self.grades[sub]:
                total += g
                count += 1
        if count == 0:
            return 0
        return total / count
    def get_total_grades_count(self):
        count = 0
        for sub in self.grades:
            count += len(self.grades[sub])
        return count
    def get_letter_grade(self):
        avg = self.get_overall_average()
        if avg >= 90: return "A"
        elif avg >= 80: return "B"
        elif avg >= 70: return "C"
        elif avg >= 60: return "D"
        return "F"
    def is_passing(self):
        if self.get_total_grades_count()==0:
            return False
        avg = self.get_overall_average()
        return avg >= 60
    def get_strongest_subject(self):

        best_sub = None
        best_avg = -1
        for sub in self.grades:
            avg = self.get_subject_average(sub)

            if avg > best_avg:
                best_avg = avg
                best_sub = sub
        if best_sub == None:
            return None
        return (best_sub, best_avg)
    def get_weakest_subject(self):
        worst_sub = None
        worst_avg = 999
        for sub in self.grades:
            avg = self.get_subject_average(sub)
            if avg < worst_avg:
                worst_avg = avg
                worst_sub = sub
        if worst_sub == None:
            return None
        return (worst_sub, worst_avg)
    def display_info(self):
        print("===========================")
        print("STUDENT PROFILE")
        print("============================")
        avg = self.get_overall_average()
        print("Name:", self.name)
        print("ID:", self.student_id)
        print("Average:", round(avg,2), "(", self.get_letter_grade(), ")")
        if self.is_passing():
            console.print("Status: [bright_green]PASSED![/bright_green]")
        else:
           console.print("Status: [bright_red]FAILED![/bright_red]")
        print("\nSubjects:")

        for sub in self.grades:
            print(sub, self.grades[sub], "Avg:", round(self.get_subject_average(sub),2))

        s = self.get_strongest_subject()
        w = self.get_weakest_subject()

        if s:
            print("Strongest:", s[0], round(s[1],2))
        if w:
            print("Weakest:", w[0], round(w[1],2))
    def display_row(self):
        avg = self.get_overall_average()
        name = self.name
        sid = self.student_id
        subj = len(self.grades)
        grade = self.get_letter_grade()
        if self.is_passing():
            status = "PASS"
        else:
            status = "FAIL"
        return f"{name:<20} {sid:<10} {subj:<5} {round(avg,2):<7} {grade:<6} {status}"


class Classroom:
    def __init__(self, name):
        self.name = name
        self.students = []
    def add_student(self, name,sid):
        for s in self.students:
            if s.student_id == sid:
                return False
        self.students.append(Student(name, sid))
        return True
    def find_student(self, sid):
        for s in self.students:
            if s.student_id == sid:
                return s
        return None
    def remove_student(self, sid):
        for i in range(len(self.students)):
            if self.students[i].student_id == sid:
                self.students.pop(i)
                return True
        return False
    def search_students(self, keyword):
        result = []
        for s in self.students:
            if keyword.lower() in s.name.lower():
                result.append(s)
        return result
    def get_top_student(self):
        if not self.students:
            return None
        best = self.students[0]

        for s in self.students:
            if s.get_overall_average() > best.get_overall_average():
                best = s

        return best
    def get_lowest_student(self):

        if not self.students:
          return None
        worst = self.students[0]

        for s in self.students:
            if s.get_overall_average() < worst.get_overall_average():
                worst = s

        return worst
    def get_class_average(self):

        if len(self.students) == 0:
            return 0
        total = 0

        for s in self.students:
            total += s.get_overall_average()

        return total / len(self.students)
    def get_passing_count(self):
        count = 0
        for s in self.students:
            if s.is_passing():
                count += 1

        return count

    def get_subject_ranking(self, sub):
        ranking = []

        for s in self.students:
          if sub in s.grades:
            ranking.append([s, s.get_subject_average(sub)])

        # simple selection sort
        for i in range(len(ranking)):

            max_i = i

            for j in range(i+1, len(ranking)):
                if ranking[j][1] > ranking[max_i][1]:
                    max_i = j

            temp = ranking[i]
            ranking[i] = ranking[max_i]
            ranking[max_i] = temp

        return ranking
    def get_all_subjects(self):

        subs = []

        for s in self.students:
            for sub in s.grades:
                if sub not in subs:
                    subs.append(sub)

        return subs
    def class_report(self):
        if not self.students:
          print("No student in the class")
          return

        print("==============================================================")
        print("CLASS REPORT -", self.name)
        print("==============================================================")

        print(f"{'Name':<20} {'ID':<10} {'Subj':<5} {'Avg':<7} {'Grade':<6} Status")
        print("--------------------------------------------------------------")

        # selection sort (highest average first)
        sorted_students = self.students[:]

        for i in range(len(sorted_students)):
          max_i = i
          for j in range(i+1, len(sorted_students)):
            if sorted_students[j].get_overall_average() > sorted_students[max_i].get_overall_average():
              max_i = j

          temp = sorted_students[i]
          sorted_students[i] = sorted_students[max_i]
          sorted_students[max_i] = temp

        for s in sorted_students:
          print(s.display_row())
        print("--------------------------------------------------------------")
        total = len(self.students)
        avg = self.get_class_average()
        passing = self.get_passing_count()

        print("\nTotal Students:", total)
        print("Class Average:", round(avg,2))
        console.print("[green]Passing:[/green]", passing)
        console.print("[red]Failing:[/red]", total - passing)
        top = self.get_top_student()
        low = self.get_lowest_student()
        if top:
            print("Top Student:", top.name, round(top.get_overall_average(),2))
        if low:
            print("Needs Support:", low.name, round(low.get_overall_average(),2))

        print("=============================================================\n")

    def subject_report(self, subject):

        ranking = self.get_subject_ranking(subject)

        print("--- SUBJECT:", subject, "---")

        rank = 1
        total = 0

        for item in ranking:
            s = item[0]
            avg = item[1]
            print(rank, s.name, round(avg,2))
            total += avg
            rank += 1

        if len(ranking) > 0:
            print("Subject Avg:", round(total/len(ranking),2))

    #BONUS used
    def edit_grade(self, sid, subject):
        s = self.find_student(sid)
        if s == None:
            print("Not found")
            return
        if subject not in s.grades:
            print("No subject")
            return

        print("Grades:", s.grades[subject])

        try:
          index = int(input("Index to change: "))
          new = float(input("New grade: "))
        except:
          print("Invalid input")
          return

        if 0 <= index < len(s.grades[subject]):
            s.grades[subject][index] = new
            print("Updated")
    def compare_student(self,sid1,sid2):
      s1 = self.find_student(sid1)
      s2 = self.find_student(sid2)
      if not s1 or not s2:
        print("Student not found")
        return
      avg1 = s1.get_overall_average()
      avg2 = s2.get_overall_average()
      print("Comparision")
      print(f"{s1.name}: {avg1:.2f}")
      print(f"{s2.name}: {avg2:.2f}")
      if avg1 > avg2:
        print(f"{s1.name} has better performance than {s2.name}")
      elif  avg1 < avg2:
        print(f"{s2.name} has better performance than {s1.name}")
      else:
        print(f"{s1.name} and {s2.name} have the same average")
    def export_report(self):
      with open("class_report.txt", "w") as file:
          file.write("CLASS REPORT - " + self.name + "\n")
          file.write("=====================================\n")
          file.write(f"{'Name':<20} {'ID':<10} {'Avg':<7} Grade\n")

          for s in self.students:
            avg = round(s.get_overall_average(), 2)
            file.write(f"{s.name:<20} {s.student_id:<10} {avg:<7} {s.get_letter_grade()}\n")

          file.write("\nTotal Students: " + str(len(self.students)) + "\n")
          file.write("Class Average: " + str(round(self.get_class_average(),2)) + "\n")
      print("Report saved as class_report.txt")


# MAIN PROGRAM

def main():
    classroom = Classroom("Grade 10 - Section A")
    running = True
    import os
    print("Current save folder:", os.getcwd())
    while running:
        with console.status("[white]Loading....[/white]", spinner = 'earth'):
            time.sleep(2)
        table = Table(show_header = True,header_style = "white",border_style = "white",  box = box.DOUBLE)
        table.add_column("           MAIN MENU",style = "bright_cyan",justify = "left")
        table.add_row("1.Add New Student")
        table.add_row('2.Record a Grade')
        table.add_row("3.View Student Info")
        table.add_row("4. Search Student by Name")
        table.add_row("5. Remove a Student")
        table.add_row("6. View Class Report")
        table.add_row("7. View Subject Report")
        table.add_row("8. Find Top Student")
        table.add_row("9. Find Student Needing Support")
        table.add_row("10. Group name")
        table.add_row("[cyan]  Bonus Features[/cyan]")
        table.add_row("11. Compare Two Students")
        table.add_row("12. Edit Student Grade")
        table.add_row("13. Export Class Report")
        table.add_row("14. Exit")
        #table.add_row('2.Record a Grade',style = 'blue')
        console.print(table)
        try:
            choice = int(input("Choice: "))
        except:
            console.print("[red]Invalid input![/red]")
            continue
        if choice == 1:
          while True:
            name = input("Name: ")
            if name == '':
                break
            sid = input("ID: ")
            if classroom.add_student(name, sid):
                console.print("[bright_green]Added successfully![/bright_green]")
            else:
                print("ID already exists!")
        elif choice == 2:
            while True:
              sid = input("Student ID: ")
              if sid == "":
                  break
              s = classroom.find_student(sid)
              if s:
                sub = input("Subject: ")
                try:
                    g = float(input("Grade: "))
                    if g < 0 or g> 100:
                        print('Grade must be between 0 amd 100.')
                        continue
                    s.add_grade(sub, g)
                    console.print('[green]Added[/green]')
                except:
                    console.print("[red]Invalid Grade[/red]")
                    continue
              else:
                console.print("[dim red]Student not found![/dim red]")
        elif choice == 3:

            sid = input("Student ID: ")
            s = classroom.find_student(sid)

            if s:
                s.display_info()
            else:
                console.print("Not found!")
        elif choice == 4:

            key = input("Search name: ")
            res = classroom.search_students(key)

            if len(res) == 0:
                console.print("[red]Not found![/red]")
            else:
                for s in res:
                    console.print(f"Name: {s.name}   ID: {s.student_id}")
        elif choice == 5:

            sid = input("Student ID: ")

            if classroom.remove_student(sid):
                console.print("[red]Removed![/red]")
            else:
               console.print("[red]Not found![/red]")
        elif choice == 6:

            classroom.class_report()
        elif choice == 7:

            sub = input("Subject: ")
            classroom.subject_report(sub)
        elif choice == 8:

            s = classroom.get_top_student()
            if s:
                print("Top Student:", s.name)

        elif choice == 9:

            s = classroom.get_lowest_student()
            if s:
                print("Needs Support:", s.name)
        elif choice == 14:
            print("Final Summery")
            classroom.class_report()
            running = False

        elif choice == 11:
            sid1 = input("Enter the first student ID:")
            sid2 =input("Enter the second student Id:")
            classroom.compare_student(sid1,sid2)

        elif choice == 12:
          sid = input("Student ID: ")
          subject = input("Subject: ")
          classroom.edit_grade(sid, subject)
        elif choice == 13:
          classroom.export_report()
        elif choice == 10:

          print("Goodbye")
          table = Table(show_header= True, border_style= 'bold white', header_style= 'bright_cyan', box = box.DOUBLE)
          table.add_column("Num", style = "white", justify='left')
          table.add_column('Group Name', style = 'white')
          table.add_column("Grade", style = 'white')
          table.add_row("1", "Obama Abraham", "11th A")
          table.add_row("2", "Tinsae Alemu", "11th A")
          table.add_row("3", "Girum Teshale", "11th B")
          console.print(table)
        else:
          print("Invalid Choice")
if __name__ == "__main__":
    main()

