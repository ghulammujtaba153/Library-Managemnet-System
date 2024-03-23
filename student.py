import mysql.connector
from person import Person
from datetime import datetime

class Student(Person):
    def __int__(self):
        self.id
        self.name
        self.password
        self.email
        self.gender

    def connection(self):
        global mycursor
        global mydb
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="gmujtaba",
            database="lms_test"
        )

        mycursor = mydb.cursor()
        return mycursor

    def validate_email(self, email):

        if "@gmail.com" not in email:
            return False

        return True

    def register(self, name,password,gender,email):
        mycursor = self.connection()
        if self.validate_email(email):

            try:
                sql = "INSERT INTO useraccount (name, password, gender, email) VALUES (%s, %s, %s, %s)"
                val = (name, password, gender, email)
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                return True
            except Exception as e:
                print("An error occurred:", str(e))
                return False
        else:
            return False

    def login(self, email, password):
        mycursor = self.connection()
        try:
            sql = "SELECT * FROM useraccount WHERE email = %s AND password = %s"
            val = (email, password)
            mycursor.execute(sql, val)
            user = mycursor.fetchone()

            if user:
                # Login successful
                print("Login successful.")

                self.id=user.__getitem__(0)
                return True
            else:
                # Login failed
                print("Login failed. Invalid email or password.")
                return False
        except Exception as e:
            print("An error occurred:", str(e))
            return False

    def get_all_assets(self):
        mycursor = self.connection()
        try:
            sql = "SELECT * FROM Asset"
            mycursor.execute(sql)
            assets = mycursor.fetchall()
            return assets
        except Exception as e:
            print("An error occurred:", str(e))
            return []

    def get_all_Requests(self, id):
        mycursor = self.connection()
        try:
            sql = "SELECT * FROM Requests INNER JOIN Asset ON Requests.AssetId= Asset.AssetId WHERE RequestedEmployee=%s"
            val = (id,)
            mycursor.execute(sql, val)
            assets = mycursor.fetchall()
            return assets
        except Exception as e:
            print("An error occurred:", str(e))
            return []

    def request(self, asset,employee):
        mycursor = self.connection()
        try:
            sql = "INSERT INTO Requests (RequestedEmployee, AssetID, DateNow) VALUES (%s, %s, %s)"
            val = (employee,asset, datetime.now().date())
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
            return True
        except Exception as e:
            print("An error occurred:", str(e))
            return False

    def check_dublicate_request(self, asset,employee):
        mycursor = self.connection()
        try:
            sql = "SELECT * FROM Requests WHERE RequestedEmployee = %s AND AssetId = %s AND Status='processing'"
            val = (employee, asset)
            mycursor.execute(sql, val)
            duplicate = mycursor.fetchone()

            if duplicate:
                return True
            else:
                return False
        except Exception as e:
            print("An error occurred:", str(e))
            return False

    def get_new_messages(self, employee):
        mycursor = self.connection()
        try:
            sql = "SELECT * FROM Requests WHERE RequestedEmployee = %s AND message_status = %s"
            val = (employee, "Approved")
            mycursor.execute(sql, val)
            duplicate = mycursor.fetchall()

            if duplicate:
                return duplicate
            else:
                return None
        except Exception as e:
            print("An error occurred:", str(e))
            return None

    def update_message_status(self, employee):
        mycursor = self.connection()
        try:
            sql = "UPDATE Requests SET Message_Status = 'sent' WHERE RequestedEmployee = %s AND Message_Status = %s"
            val = (employee, "Approved")
            mycursor.execute(sql, val)
            mydb.commit()
            rows_affected = mycursor.rowcount

            return rows_affected
        except Exception as e:
            print("An error occurred:", str(e))
            return 0


    def update_asset_status(self, asset_id, new_status, new_assigned_employee):
        mycursor = self.connection()
        try:
            sql = "UPDATE Asset SET Status = %s, AssignedEmployee = %s WHERE AssetID = %s"
            val = (new_status, new_assigned_employee, asset_id)
            mycursor.execute(sql, val)
            mydb.commit()

            if mycursor.rowcount > 0:
                print("Asset status updated successfully.")
                return True
            else:
                print("Asset with the given ID not found.")
                return False
        except Exception as e:
            print("An error occurred:", str(e))
            return False




    def get_all_personel_assets(self, id):
        mycursor = self.connection()
        try:
            sql = "SELECT * FROM Asset where assignedemployee= %s"
            val = (id,)
            mycursor.execute(sql, val)
            assets = mycursor.fetchall()
            return assets
        except Exception as e:
            print("An error occurred:", str(e))
            return []



