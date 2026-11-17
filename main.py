from functools import total_ordering


def average_grade(grades):
    """Средняя оценка по всем курсам; ноль если оценок ещё нет."""
    all_grades = [grade for course_grades in grades.values()
                  for grade in course_grades]
    if not all_grades:
        return 0
    return sum(all_grades) / len(all_grades)


@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer)
                and course in lecturer.courses_attached
                and course in self.courses_in_progress
                and 1 <= grade <= 10):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: '
                f'{average_grade(self.grades):.1f}\n'
                f'Курсы в процессе изучения: '
                f'{", ".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses)}')

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return average_grade(self.grades) == average_grade(other.grades)

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return average_grade(self.grades) < average_grade(other.grades)


class Mentor:
    """Родительский класс для всех преподавателей."""

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


@total_ordering
class Lecturer(Mentor):
    """Лектор: получает от студентов оценки за лекции."""

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: '
                f'{average_grade(self.grades):.1f}')

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return average_grade(self.grades) == average_grade(other.grades)

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return average_grade(self.grades) < average_grade(other.grades)


class Reviewer(Mentor):
    """Эксперт: ставит студентам оценки за домашние задания."""

    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


def average_hw_grade(students, course):
    """Средняя оценка за домашние задания по всем студентам курса."""
    all_grades = []
    for student in students:
        all_grades += student.grades.get(course, [])
    if not all_grades:
        return 0
    return sum(all_grades) / len(all_grades)


def average_lecture_grade(lecturers, course):
    """Средняя оценка за лекции по всем лекторам курса."""
    all_grades = []
    for lecturer in lecturers:
        all_grades += lecturer.grades.get(course, [])
    if not all_grades:
        return 0
    return sum(all_grades) / len(all_grades)


if __name__ == '__main__':
    # По 2 экземпляра каждого класса
    student_1 = Student('Павел', 'Быстров', 'М')
    student_2 = Student('Ольга', 'Алёхина', 'Ж')
    lecturer_1 = Lecturer('Иван', 'Иванов')
    lecturer_2 = Lecturer('Анна', 'Петрова')
    reviewer_1 = Reviewer('Мария', 'Федоровна')
    reviewer_2 = Reviewer('Пётр', 'Петров')

    # Курсы
    student_1.courses_in_progress += ['Python', 'Git']
    student_2.courses_in_progress += ['Python', 'Git']
    student_1.add_courses('Введение в программирование')
    student_2.add_courses('Введение в программирование')
    lecturer_1.courses_attached += ['Python', 'Git']
    lecturer_2.courses_attached += ['Python', 'Git']
    reviewer_1.courses_attached += ['Python', 'Git']
    reviewer_2.courses_attached += ['Python', 'Git']

    # Эксперты оценивают домашние задания студентов
    reviewer_1.rate_hw(student_1, 'Python', 10)
    reviewer_1.rate_hw(student_1, 'Python', 9)
    reviewer_1.rate_hw(student_1, 'Git', 10)
    reviewer_2.rate_hw(student_2, 'Python', 8)
    reviewer_2.rate_hw(student_2, 'Python', 7)
    reviewer_2.rate_hw(student_2, 'Git', 9)

    # Студенты оценивают лекции
    student_1.rate_lecture(lecturer_1, 'Python', 10)
    student_1.rate_lecture(lecturer_2, 'Python', 8)
    student_1.rate_lecture(lecturer_1, 'Git', 9)
    student_2.rate_lecture(lecturer_1, 'Python', 9)
    student_2.rate_lecture(lecturer_2, 'Python', 7)
    student_2.rate_lecture(lecturer_2, 'Git', 8)

    # Некорректные вызовы
    print(reviewer_1.rate_hw(student_1, 'Java', 10))         # Ошибка
    print(student_1.rate_lecture(reviewer_1, 'Python', 10))  # Ошибка

    # Вывод информации (__str__)
    print('--- Эксперты ---')
    print(reviewer_1, reviewer_2, sep='\n\n')
    print('--- Лекторы ---')
    print(lecturer_1, lecturer_2, sep='\n\n')
    print('--- Студенты ---')
    print(student_1, student_2, sep='\n\n')

    # Сравнение
    print('--- Сравнение ---')
    print(f'lecturer_1 > lecturer_2: {lecturer_1 > lecturer_2}')
    print(f'student_1 > student_2: {student_1 > student_2}')
    print(f'student_1 == student_2: {student_1 == student_2}')

    # Средние оценки по курсу
    students = [student_1, student_2]
    lecturers = [lecturer_1, lecturer_2]
    print('--- Средние оценки по курсам ---')
    for course in ('Python', 'Git'):
        print(f'{course}: ДЗ студентов - '
              f'{average_hw_grade(students, course):.1f}, '
              f'лекции - {average_lecture_grade(lecturers, course):.1f}')
