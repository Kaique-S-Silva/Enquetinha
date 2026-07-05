CREATE TABLE IF NOT EXISTS polls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pergunta TEXT NOT NULL,
    criador_id INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    data_criacao DATE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    data_encerramento DATE,
    encerrada BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS poll_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_id INTEGER NOT NULL,
    texto TEXT NOT NULL,
    FOREIGN KEY (poll_id) REFERENCES polls(id)
);

CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_id INTEGER NOT NULL,
    option_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (poll_id) REFERENCES polls(id),
    FOREIGN KEY (option_id) REFERENCES poll_options(id)
);