import aiosqlite

# TODO сделать вывод соответсвующего сообщения, если вопросов нет
# TODO добавить ограничения в длине строк
# TODO добавить отмену ввода в FSM
# TODO проверить все на await

async def init():
    """ Функция создания новой таблицы (инициализации), если она еще не была создана """
    global con
    global cur

    # Открываем базу данных
    con = await aiosqlite.connect("bot.db")
    cur = await con.cursor()

    await con.execute(
        """CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_title VARHCAR(64) NOT NULL,
            question_title VARHCAR(64) UNIQUE NOT NULL,
            question_description VARHCAR(4096) NOT NULL,

            FOREIGN KEY(category_title) REFERENCES categories (category_title) ON DELETE CASCADE
        )
        """
    )

    await con.execute(
        """CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_title VARHCAR(64) UNIQUE NOT NULL
        )
        """
    )

    await con.commit()

async def fetch_all_categories() -> list:
    """ Функция получения всех категорий """
    await cur.execute("""SELECT * FROM categories""")
    categories = await cur.fetchall()

    return categories

async def add_category(category_title: str) -> None:
    """ Функция добавления новой категории """
    await cur.execute("""INSERT INTO categories (category_title) VALUES (?)""", (category_title, ))
    await con.commit()

async def fetch_one_question_by_id(question_id: int) -> set:
    """ Функция получения вопроса по id """
    await cur.execute(f"""SELECT * from questions WHERE id=?""", (question_id, ))
    question = await cur.fetchone()

    return question

async def fetch_all_questions_by_category_title(category_title: str) -> list:
    """ Функция получения всех вопросов, относящихся к определенной категории """
    await cur.execute(f"""SELECT * from questions WHERE category_title=?""", (category_title, ))
    questions = await cur.fetchall()

    return questions

async def add_question(
    category_title: str,
    question_title: str,
    question_description: str
) -> None:
    """ Функция добавления нового вопроса """
    await cur.execute(
        f"""INSERT INTO questions
        (category_title, question_title, question_description)
        VALUES (?, ?, ?)""", (category_title, question_title, question_description)
    )
    await con.commit()
