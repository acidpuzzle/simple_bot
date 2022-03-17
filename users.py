import sqlite3
import logging


# Class for managing users in the database
class UserDataBase(object):
    def __init__(self):
        try:
            self.logger = logging.getLogger(__name__)
            self.__user_db_file: str = 'users_db.sqlite'
            self.__connection = sqlite3.connect(self.__user_db_file)
            self.__cursor = self.__connection.cursor()
            self.__group: list = ['admin', 'user', 'guest']
            self.__user: str = 'Telegram_id: {}\nGroup: {}\nDescription: {}\nActive: {}\n========================\n'
            self.__msg_default: str = 'Something went wrong.'
            self.__msg_telegram_id: str = 'telegram_id - required argument. 6 to 10 digits.'
            self.__msg_user_exist: str = 'User with ID: {} already exists.\n'
            self.__msg_user_not_exist: str = 'User with ID: {} is not in the database.\n'
            self.__msg_user_not_found: str = 'No results found for:  {} \n'
            self.__msg_group: str = f'The group should be: {", ".join(self.__group)}.'

        except Exception as err:
            self.logger.exception(err)

    def __check_telegram_id(self, telegram_id: str):
        """
        :param telegram_id:
        :return: True or False
        """
        self.logger.debug('Checking that telegram_id is a number, from 6 to 10 characters.')
        return telegram_id.isdigit() and 6 <= len(telegram_id) <= 10

    def __check_user_exist(self, telegram_id: str):
        """
        :param telegram_id:
        :return: True or False
        """

        self.logger.debug('Check if there is such a user in the database?')
        return len(self.list_user(int(telegram_id))) != 0

    def __check_group(self, group: str):
        """
        Chek input argument group.
        :param group: string must be admin, user or guest
        :return: True or False
        """
        self.logger.debug('Checking that the group is correct.')
        return group.lower() in self.__group

    def __check_user_created_recently(self, minutes: int = 5):
        """
        The function checks how many users have been created in the last time. Default 5 minutes.
        :return: Int
        """
        task: tuple = (minutes,)
        sql: str = """
        SELECT strftime('%s','now') - strftime('%s', main.users.creation_data) 
        as time 
        FROM main.users 
        WHERE time < 60*?;
        """
        self.logger.debug(f'Checking how many users have been created in the last {minutes} minutes.')
        return len(self.__sql_executor(sql, task))

    def __beauty_out(self, user_list: list):
        """
        The function converts a list of tuples to a string for printing.
        :param user_list: list of tuples
        :return:
        """
        try:
            output: str = ''
            for item in user_list:
                active = item[3]
                if active == 1:
                    active = 'Yes'
                else:
                    active = 'No'
                output += self.__user.format(item[0], item[1], item[2], active)
            return output
        except Exception as err:
            self.logger.exception(err)
            return self.__msg_default

    def __sql_executor(self, sql, task=('',)):
        """

        :param sql:
        :param task:
        :return:
        """
        def changes_in_database(inquiry: str):
            """
            Does this change the database?
            :param inquiry:
            :return: True or False
            """
            return 'UPDATE' in inquiry or 'INSERT' in inquiry or 'DELETE' in inquiry

        try:
            self.__cursor.execute(sql, task)
            if changes_in_database(sql):
                self.__connection.commit()
                self.logger.debug('Making changes to the database.')
                return 'The database has been changed'
            else:
                output = self.__cursor.fetchall()
                self.logger.debug('Reading from the database.')
                self.logger.debug(output)
                return output

        except Exception as err:
            self.logger.exception(err)
            return self.__msg_default

    def add_user(self, telegram_id: str, group: str = 'guest', description: str = ''):
        """

        :return:
        """
        MAX_USER_CREATED_RECENTLY = 3
        if self.__check_user_created_recently() >= MAX_USER_CREATED_RECENTLY:
            return f'You cannot create more than {MAX_USER_CREATED_RECENTLY} users within five minutes.'

        if not self.__check_telegram_id(telegram_id):
            return self.__msg_telegram_id

        if self.__check_user_exist(telegram_id):
            return self.__msg_user_exist.format(telegram_id)

        if not self.__check_group(group):
            return self.__msg_group

        task: tuple = (telegram_id, group.lower(), description, description.lower())

        sql: str = """
        INSERT 
        INTO main.users (telegram_id, group_id, description, lower_description) 
        VALUES (?, ?, ?, ?)
        """

        return self.__sql_executor(sql, task)

    def list_user(self, *args):
        """
        :return: String
        """
        if len(args) == 0:
            sql = """
            SELECT telegram_id,group_id,description,active 
            from users
            """
            return self.__beauty_out(self.__sql_executor(sql))
        else:
            task = (f"{args[0]}", f"%{args[0]}%".lower())
            sql = """
            SELECT telegram_id,group_id,description,active
            from main.users
            WHERE telegram_id 
            LIKE ?
            OR lower_description 
            LIKE ?
            """
            return = self.__beauty_out(self.__sql_executor(sql, task))

    def __edit_user(self, sql: str, telegram_id: str):
        """

        :param sql:
        :param telegram_id:
        :return:
        """
        if not self.__check_telegram_id(telegram_id):
            return self.__msg_telegram_id

        if not self.__check_user_exist(telegram_id):
            return self.__msg_user_not_exist.format(telegram_id)

        task: tuple = (telegram_id,)
        return self.__sql_executor(sql, task)

    def off_user(self, telegram_id: str):
        """

        :param telegram_id:
        :param action:
        :return:
        """
        sql: str = """
        UPDATE main.users 
        SET active=0, deactivation_data=CURRENT_TIMESTAMP, activation_data=NULL
        WHERE telegram_id=?
        """
        return self.__edit_user(sql, telegram_id)

    def on_user(self, telegram_id: str = ''):
        """

        :param telegram_id:
        :param action:
        :return:
        """
        sql: str = """
        UPDATE main.users 
        SET active=1, activation_data=CURRENT_TIMESTAMP
        WHERE telegram_id=?
        """
        return self.__edit_user(sql, telegram_id)

    def del_user(self, telegram_id: str):
        """

        :param telegram_id:
        :param action:
        :return:
        """
        sql: str = """
        DELETE 
        FROM main.users 
        WHERE telegram_id=?
        """
        return self.__edit_user(sql, telegram_id)

    def list_user_in_group(self, group: str):
        """
        List of users ID in group.
        :param group: root, admin, user or guest
        :return: list[ig,id,id...]
        """
        if not self.__check_group(group):
            return self.__msg_group

        sql = """
        SELECT telegram_id 
        from main.users 
        WHERE (group_id=? and active=1);
        """
        task = (group.lower(),)
        output = []

        for row in self.__sql_executor(sql, task):
            output.append(row[0])
        return output

    def move_user_to_group(self, telegram_id: str, group: str):
        """
        Move User to group.
        :param telegram_id:
        :param group: admin, user or guest
        :return: None
        """
        if not self.__check_telegram_id(telegram_id):
            return self.__msg_telegram_id

        if not self.__check_user_exist(telegram_id):
            return self.__msg_user_not_exist.format(telegram_id)

        if not self.__check_group(group):
            return self.__msg_group

        sql = """
        UPDATE main.users 
        SET group_id=? 
        WHERE telegram_id=?
        """
        task = (group.lower(), telegram_id)

        return self.__sql_executor(sql, task)
