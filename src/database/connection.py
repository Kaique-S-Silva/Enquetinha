import aiosqlite as ai
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH: str = os.getenv("DB_PATH", "data/enquetinha_dev.db")

async def create_tables():
    # print("Iniciando tabelas") # debug
    with open("./src/database/schema.sql") as f:
        sqlscript = f.read()
        async with ai.connect(DB_PATH) as db:
            await db.executescript(sqlscript)
            await db.commit()
    # print("Tabelas criadas") # debug

async def create_poll(pergunta: str, options: list[str], 
                      criador_id: int, guild_id: int) -> tuple[int, dict[str, int]]:
    async with ai.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO polls (pergunta, criador_id, guild_id) VALUES (?, ?, ?)",
            (pergunta, criador_id, guild_id)
        )
        options_id = {}

        for option in options:
            options_cursor = await db.execute(
                "INSERT INTO poll_options (poll_id, texto) VALUES (?,?)",
                (cursor.lastrowid, option)
            )
            options_id[option] = options_cursor.lastrowid
        await db.commit()
    if not cursor.lastrowid:
        raise
    return (cursor.lastrowid, options_id)

async def get_user_vote(poll_id: int, user_id: int) -> int | None:
    async with ai.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT option_id FROM votes WHERE poll_id = ? AND user_id = ?",
            (poll_id, user_id)
        )

        row = await cursor.fetchone()

        if row:
            return row[0]
        else:
            return None

async def get_vote_counts(poll_id: int) -> dict[str, int]:
    async with ai.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT poll_options.texto, COUNT(votes.id) " \
            "FROM poll_options " \
            "LEFT JOIN votes ON votes.option_id = poll_options.id " \
            "WHERE poll_options.poll_id = ? " \
            "GROUP BY poll_options.id",
            (poll_id,)
        )

        row = await cursor.fetchall()
        return {r[0]: r[1] for r in row}

async def register_vote(poll_id: int, option_id: int, user_id: int) -> None:
    voted = await get_user_vote(poll_id, user_id)
    async with ai.connect(DB_PATH) as db:
        if not voted:
            await db.execute(
                "INSERT INTO votes (poll_id, option_id, user_id) " \
                "VALUES (?, ?, ?)",
                (poll_id, option_id, user_id)
            )
            await db.commit()
        else:
            await db.execute(
                "UPDATE votes " \
                "SET option_id = ? " \
                "WHERE poll_id = ? AND user_id = ?",
                (option_id, poll_id, user_id)
            )
            await db.commit()

async def close_poll_db(poll_id: int) -> None:
    async with ai.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE polls " \
            "SET encerrada = 1, data_encerramento = CURRENT_TIMESTAMP " \
            "WHERE id = ?",
            (poll_id,)
        )
        await db.commit()