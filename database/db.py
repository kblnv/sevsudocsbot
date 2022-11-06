import sqlite3

# Открываем базу данных
con = sqlite3.connect("bot.db")
cur = con.cursor()


def init():
    """ Функция создания новой таблицы (инициализации), если она еще не была создана """

    con.execute(
        """CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_title TEXT NOT NULL CHECK(question_title != ''),
            question_description TEXT NOT NULL CHECK(question_description != '')
        )    
        """
    )

    con.commit()

def fetch_all_questions() -> list:
    """ Функция получения всех вопросов из БД """
    cur.execute(""" SELECT * FROM questions """)
    # Получаем СПИСОК кортежей с данными из таблицы вида
    # [(1, вопрос1, описание1), (2, вопрос2, описание2), ...]
    questions = cur.fetchall()

    return questions

def fetch_one_question(question_id: int) -> set:
    """ Функция получения вопроса по id из БД """
    cur.execute(f""" SELECT * from questions WHERE id={question_id} """)
    question = cur.fetchone()
    return question

def add_question(question_title: str, question_text: str) -> None:
    """ Функция добавления нового вопроса в БД """
    pass

def correct_question(question_id: int, question_title: str, question_text: str) -> None:
    """ Функция корректировки существующего вопроса в БД """
    pass

def delete_question(question_id: int) -> None:
    """ Функция удаления вопроса из БД """
    pass