#### Установить модуль "python-telegram-bot":

```shell
pip install python-telegram-bot --upgrade
```

#### Создать базу данных:

```python
import sqlite3


sql_command = """
DROP TABLE IF EXISTS groups; 
DROP TABLE IF EXISTS users;
create table users
(
    telegram_id       INTEGER      not null
        primary key
        unique,
    active            int       default 1 not null,
    group_id          VARCHAR(255) not null,
    description       VARCHAR(255),
    lower_description VARCHAR(255),
    creation_data     TIMESTAMP default CURRENT_TIMESTAMP,
    deactivation_data TIMESTAMP
);
INSERT INTO users (telegram_id, group_id, description, lower_description) 
values (300552413, "admin", "@AleksPavlov", lower("@AleksPavlov"));
"""

conn = sqlite3.connect('users_db.sqlite')
cur = conn.cursor()
cur.executescript(sql_command)
conn.commit()
```