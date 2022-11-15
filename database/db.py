import aiosqlite

# TODO проверить все на await
# TODO проверять все ошибки при операциях с БД (try, catch)
# TODO поменять нэйминг FSM
# TODO сделеать полнофункциональное меню (кнопки назад), админка

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
            category_title VARCHAR(64) NOT NULL,
            question_title VARCHAR(64) UNIQUE NOT NULL,
            question_description VARCHAR(4096) NOT NULL,

            FOREIGN KEY (category_title) REFERENCES categories (category_title) ON DELETE CASCADE
        )
        """
    )

    await con.execute(
        """CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_title VARCHAR(64) UNIQUE NOT NULL
        )
        """
    )
    
    # Чтобы нормально работало удаление категории (со всеми дочерними вопросами)
    await con.execute("""PRAGMA foreign_keys = ON""")

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

async def fetch_all_questions() -> list:
    await cur.execute("""SELECT * FROM questions""")
    questions = await cur.fetchall()

    return questions

async def fetch_one_question_by_id(question_id: int) -> set:
    """ Функция получения вопроса по id """
    await cur.execute("""SELECT * from questions WHERE id=?""", (question_id, ))
    question = await cur.fetchone()

    return question

async def fetch_all_questions_by_category_title(category_title: str) -> list:
    """ Функция получения всех вопросов, относящихся к определенной категории """
    await cur.execute("""SELECT * from questions WHERE category_title=?""", (category_title, ))
    questions = await cur.fetchall()

    return questions

async def add_question(
    category_title: str,
    question_title: str,
    question_description: str
) -> None:
    """ Функция добавления нового вопроса """
    await cur.execute(
        """INSERT INTO questions
        (category_title, question_title, question_description)
        VALUES (?, ?, ?)""", (category_title, question_title, question_description)
    )
    await con.commit()

async def delete_category(category_title: str) -> None:
    """ Функция удаления категории """
    await cur.execute("""DELETE FROM categories WHERE category_title=?""", (category_title, ))
    await con.commit()

async def delete_question(question_title: str) -> None:
    """ Функция удаления вопроса """
    await cur.execute("""DELETE FROM questions WHERE question_title=?""", (question_title, ))
    await con.commit()
