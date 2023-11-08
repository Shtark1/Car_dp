import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, username):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `username`) VALUES (?, ?)", (user_id, username,))

    def del_user(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM users WHERE user_id = (?)", (user_id,))

    def select_all(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users").fetchall()

    def select_all_user_id(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users").fetchall()

    def select_all_car(self, car, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT {car} FROM users WHERE user_id = (?)", (user_id,)).fetchone()

    def there_is_user(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = (?)", (user_id,)).fetchone()

    def add_car_user(self, user_id, division, name_car):
        with self.connection:
            all_car_user = self.cursor.execute(f"SELECT {division} FROM users WHERE user_id = (?)", (user_id,)).fetchone()
            if all_car_user[0]:
                name_car += all_car_user[0]

            return self.cursor.execute(f"UPDATE users SET {division} = (?) WHERE user_id = (?)", (name_car, user_id))

    def del_car_user(self, user_id, name_car):
        with self.connection:
            all_car_d1 = self.cursor.execute(f"SELECT car_d1 FROM users WHERE user_id = (?)", (user_id,)).fetchone()
            all_car_d2 = self.cursor.execute(f"SELECT car_d2 FROM users WHERE user_id = (?)", (user_id,)).fetchone()
            all_car_d3 = self.cursor.execute(f"SELECT car_d3 FROM users WHERE user_id = (?)", (user_id,)).fetchone()

            if all_car_d1[0]:
                if name_car in all_car_d1[0].split(","):
                    name_car = all_car_d1[0].replace(f"{name_car},", "")
                    division = "car_d1"
                    self.cursor.execute(f"UPDATE users SET {division} = (?) WHERE user_id = (?)", (name_car, user_id))

            if all_car_d2[0]:
                if name_car in all_car_d2[0].split(","):
                    name_car = all_car_d2[0].replace(f"{name_car},", "")
                    division = "car_d2"
                    self.cursor.execute(f"UPDATE users SET {division} = (?) WHERE user_id = (?)", (name_car, user_id))

            if all_car_d3[0]:
                if name_car in all_car_d3[0].split(","):
                    name_car = all_car_d3[0].replace(f"{name_car},", "")
                    division = "car_d3"
                    self.cursor.execute(f"UPDATE users SET {division} = (?) WHERE user_id = (?)", (name_car, user_id))
