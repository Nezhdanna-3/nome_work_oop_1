from functools import total_ordering


class Mentor:
    """Родительский класс для лекторов и экспертов."""

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


@total_ordering
class Lecturer(Mentor):
    """Лектор. Получает оценки за лекции от студентов."""

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # {название курса: [оценки]}

    def average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.average_grade():.1f}')

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() == other.average_grade()

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Reviewer(Mentor):
    """Эксперт, проверяющий домашние задания."""

    def rate_hw(self, student, course, grade):
        if not isinstance(student, Student):
            raise ValueError('Оценку можно выставить только студенту')
        if course not in self.courses_attached:
            raise ValueError(f'Курс "{course}" не закреплён за экспертом')
        if course not in student.courses_in_progress:
            raise ValueError(f'Студент не записан на курс "{course}"')
        student.grades.setdefault(course, []).append(grade)

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')


@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}  # {название курса: [оценки за ДЗ]}

    def rate_lecture(self, lecturer, course, grade):
        """Студент ставит оценку лектору за лекцию."""
        if not isinstance(lecturer, Lecturer):
            raise ValueError('Оценку за лекцию можно выставить только лектору')
        if course not in lecturer.courses_attached:
            raise ValueError(f'Курс "{course}" не закреплён за лектором')
        if course not in self.courses_in_progress:
            raise ValueError(f'Студент не записан на курс "{course}"')
        lecturer.grades.setdefault(course, []).append(grade)

    def average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        courses_in_progress = ', '.join(self.courses_in_progress) or '—'
        finished_courses = ', '.join(self.finished_courses) or '—'
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {self.average_grade():.1f}\n'
                f'Курсы в процессе изучения: {courses_in_progress}\n'
                f'Завершенные курсы: {finished_courses}')

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() == other.average_grade()

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() < other.average_grade()


# ---------- Функции для подсчёта средних оценок ----------

def average_hw_by_course(students, course):
    """Средняя оценка за ДЗ по всем студентам в рамках курса."""
    grades = []
    for student in students:
        grades.extend(student.grades.get(course, []))
    return sum(grades) / len(grades) if grades else 0


def average_lecture_by_course(lecturers, course):
    """Средняя оценка за лекции всех лекторов в рамках курса."""
    grades = []
    for lecturer in lecturers:
        grades.extend(lecturer.grades.get(course, []))
    return sum(grades) / len(grades) if grades else 0


# ---------- Задание № 4. Полевые испытания ----------

if __name__ == '__main__':
    lecturer_1 = Lecturer('Иван', 'Иванов')
    lecturer_2 = Lecturer('Сергей', 'Сергеев')

    reviewer_1 = Reviewer('Пётр', 'Петров')
    reviewer_2 = Reviewer('Анна', 'Смирнова')

    student_1 = Student('Алёхина', 'Ольга', 'Ж')
    student_2 = Student('Борисов', 'Дмитрий', 'М')

    # Закрепляем курсы
    lecturer_1.courses_attached += ['Python', 'C++']
    lecturer_2.courses_attached += ['Python', 'Java']

    reviewer_1.courses_attached += ['Python', 'C++']
    reviewer_2.courses_attached += ['Python', 'Java']

    student_1.courses_in_progress += ['Python', 'Java']
    student_1.finished_courses += ['Введение в программирование']

    student_2.courses_in_progress += ['Python', 'C++']

    # Студенты ставят оценки лекторам
    student_1.rate_lecture(lecturer_1, 'Python', 7)
    student_1.rate_lecture(lecturer_2, 'Python', 10)
    student_1.rate_lecture(lecturer_2, 'Java', 9)
    student_2.rate_lecture(lecturer_1, 'Python', 8)
    student_2.rate_lecture(lecturer_1, 'C++', 9)

    # Эксперты ставят оценки студентам
    reviewer_1.rate_hw(student_1, 'Python', 9)
    reviewer_1.rate_hw(student_1, 'Python', 8)
    reviewer_1.rate_hw(student_2, 'Python', 10)
    reviewer_1.rate_hw(student_2, 'C++', 9)
    reviewer_2.rate_hw(student_1, 'Java', 10)

    print(lecturer_1, end='\n\n')
    print(lecturer_2, end='\n\n')
    print(reviewer_1, end='\n\n')
    print(student_1, end='\n\n')
    print(student_2, end='\n\n')

    # Сравнения
    print('lecturer_1 < lecturer_2:', lecturer_1 < lecturer_2)
    print('student_1 > student_2 :', student_1 > student_2)
    print('lecturer_1 == lecturer_1:', lecturer_1 == lecturer_1)

    students = [student_1, student_2]
    lecturers = [lecturer_1, lecturer_2]

    print('\nСредняя оценка за ДЗ по Python:',
          round(average_hw_by_course(students, 'Python'), 2))
    print('Средняя оценка за лекции по Python:',
          round(average_lecture_by_course(lecturers, 'Python'), 2))
