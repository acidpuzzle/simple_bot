separator = """
============================
"""

adduser = """
/adduser

Команда добавляет пользователя
Пример: 
/adduser 12345678 admin description
             
Где:
12345678 - telegram_id пользователя

admin - Группа для пользователя, опциональный параметр, если не указать то пользователь попадет в группу 'guest'

description - Комментарий, необязательный параметр

"""

listuser = """
/listuser

Команда выводит список пользователей или информацию по конкретному пользователю
Пример: 
/listuser 12345678

Где:
12345678 - telegram_id пользователя, необязательный параметр

"""

offuser = """
/offuser

Команда отключает пользователя
Пример: 
/offuser 12345678
             
Где:
12345678 - telegram_id пользователя

"""

onuser = """
/onuser

Команда включает пользователя
Пример: 
/onuser 12345678
             
Где:
12345678 - telegram_id пользователя

"""

deluser = """
/deluser

Команда удаляет пользователя
Пример: 
/deluser 12345678
             
Где:
12345678 - telegram_id пользователя

"""

movuser = """
/movuser

Команда меняет группу пользователя
Пример: 
/movuser 12345678 admin
             
Где:
12345678 - telegram_id пользователя

admin - Новая группа для пользователя

"""

full_help_admin = (
        adduser + separator +
        listuser + separator +
        offuser + separator +
        onuser + separator +
        deluser + separator +
        movuser
)


full_help_user = separator

full_help_guest = separator
