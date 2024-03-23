import mysql.connector
import csv
import datetime
from datetime import datetime

from person import Person


class Admin(Person):


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


    def insert_asset(self, asset_name, asset_type, status):
        mycursor = self.connection()
        try:
            sql = "INSERT INTO Asset (AssetName, AssetType, Status, DateNow) VALUES (%s, %s, %s, %s)"
            val = (asset_name, asset_type, status, datetime.now().date())
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
            return True
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


    def get_all_requests(self):
        mycursor = self.connection()
        try:
            sql = "SELECT * FROM Asset INNER JOIN Requests ON Asset.AssetId=Requests.AssetId WHERE Requests.Status='processing'"
            mycursor.execute(sql)
            req = mycursor.fetchall()
            print(req)
            return req
        except Exception as e:
            print("An error occurred:", str(e))
            return []


    def update_asset_status(self, asset_id, new_status):
        mycursor = self.connection()
        try:
            sql = "UPDATE Asset SET Status = %s WHERE AssetID = %s"
            val = (new_status, asset_id)
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



    def accept_request(self, asset_id, new_status, employee_id, requestId, request_status):
        mycursor = self.connection()
        try:
            sql = "UPDATE Asset SET Status = %s, AssignedEmployee = %s WHERE AssetID = %s"
            val = (new_status, employee_id, asset_id)
            mycursor.execute(sql, val)
            mydb.commit()

            if mycursor.rowcount > 0:
                print("Asset has been updated and assigned.")

                mycursor = self.connection()
                try:
                    update_request_sql = "UPDATE Requests SET Status = %s, Message_Status='Approved' WHERE requestID = %s"
                    update_request_val = (request_status, requestId)
                    mycursor.execute(update_request_sql, update_request_val)
                    mydb.commit()
                    print("Request status has been updated.")
                    return True
                except Exception as update_error:
                    print('Error updating request status:', str(update_error))
            else:
                print("Asset with ID not found.")
                return False
        except Exception as e:
            print("An error occurred:", str(e))
            return False


    def reject_requests(self,  requestId, status):
        mycursor = self.connection()
        try:
            delete_request_sql = "UPDATE Requests SET Status = %s, message_status='Approved' WHERE RequestID = %s"
            delete_request_val = (status, requestId)
            mycursor.execute(delete_request_sql, delete_request_val)
            mydb.commit()
            print("request rejected")
            return True

        except Exception as e:
            print("An error occurred:", str(e))
            return False

    def get_new_messages(self):
        mycursor = self.connection()
        try:
            sql = "SELECT * FROM Requests WHERE Message_Arrival_Status = %s "
            val = ( "new",)
            mycursor.execute(sql, val)
            duplicate = mycursor.fetchall()

            if duplicate:
                return duplicate
            else:
                return None
        except Exception as e:
            print("An error occurred:", str(e))
            return None

    def update_message_status(self):
        mycursor = self.connection()
        try:
            sql = "UPDATE Requests SET Message_Arrival_Status = 'old' WHERE Message_Arrival_Status = 'new'"
            mycursor.execute(sql)
            mydb.commit()
            rows_affected = mycursor.rowcount

            return rows_affected
        except Exception as e:
            print("An error occurred:", str(e))
            return 0




    def save_assets_to_csv(self):
        mycursor = self.connection()
        try:
            sql = "SELECT * FROM Asset LEFT JOIN useraccount ON Asset.assignedemployee = useraccount.userid"
            mycursor.execute(sql)
            assets = mycursor.fetchall()
            current_datetime = datetime.datetime.now()
            filename = f"assets_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.csv"

            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ["AssetID", "AssetName", "AssetType", "Status", "AssignedEmployeeId", "Employee Name", "Email"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for asset in assets:
                    writer.writerow(
                        {"AssetID": asset[0], "AssetName": asset[1], "AssetType": asset[2], "Status": asset[3],
                         "AssignedEmployeeId": asset[4], "Employee Name": asset [7], "Email": asset[10]})

            print(f"Asset information saved to {filename} successfully.")
        except Exception as e:
            print("An error occurred:", str(e))



    def save_users_to_csv(self):
        mycursor = self.connection()
        try:
            sql = "SELECT * FROM useraccount"
            mycursor.execute(sql)
            users = mycursor.fetchall()


            current_datetime = datetime.datetime.now()
            filename = f"users_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.csv"

            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ["UserID", "Name", "Gender", "Email"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for user in users:
                    writer.writerow({"UserID": user[0], "Name": user[1], "Gender": user[3], "Email": user[4]})

            print("User information saved to successfully.")
        except Exception as e:
            print("An error occurred:", str(e))



    def generate_request_report(self, report_date):
        mycursor = self.connection()
        try:
            sql = "SELECT Requests.RequestID, Asset.AssetName, Asset.Status " \
                  "FROM Requests " \
                  "INNER JOIN Asset ON Requests.AssetID = Asset.AssetID " \
                  "WHERE DATE(Requests.DateNow) = %s"
            val = (report_date,)
            mycursor.execute(sql, val)
            requests = mycursor.fetchall()

            if not requests:
                print("No requests found for the given date.")
                return False

            current_datetime = datetime.now()
            filename = f"request_report_{report_date}_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.csv"

            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ["RequestID", "AssetName", "AssetStatus"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for request in requests:
                    writer.writerow({"RequestID": request[0], "AssetName": request[1], "AssetStatus": request[2]})

            print(f"Request report for {report_date} saved to {filename} successfully.")
            return True
        except Exception as e:
            print("An error occurred:", str(e))
            return False

