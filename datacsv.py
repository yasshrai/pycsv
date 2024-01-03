import csv
import hashlib
import os
import shutil



# current path

current_path = os.getcwd()
file_path = os.path.join(current_path, "userdetail.csv")

# errors


class UserNotFound(Exception):
    def __init__(self, message='user not found'):
        super().__init__(message)


class IncorrectPassword(Exception):
    def __init__(self, message='incorrect password'):
        super().__init__(message)


class NouseridPassword(Exception):
    def __init__(self, message='No userid password provided'):
        super().__init__(message)


class DatabaseNameNotProvided(Exception):
    def __init__(self, message='Database not provided'):
        super().__init__(message)


class UseralreadyExist(Exception):
    def __init__(self, message='user already exist'):
        super().__init__(message)


class DatabasealreadyExist(Exception):
    def __init__(self, message='database already exist'):
        super().__init__(message)


class NotVerfiedUsernamePassword(Exception):
    def __init__(self, message='not verfied username password'):
        super().__init__(message)


class NotValidUsernameAndPassword(Exception):
    def __init__(self, message='not valid username and password'):
        super().__init__(message)


class DatabaseNotSelected(Exception):
    def __init__(self, message=' database not selected'):
        super().__init__(message)


class SomethingWentWrong(Exception):
    def __init__(self, message=''):
        super().__init__(message)


# ----------------main----------------class

class connect:
   

    def __init__(self, username=None, password=None, databasename=None):
        self.username = username
        self.password = password
        self.databasename = databasename
        global check
        global databasechecker
        check = False
        databasechecker = False
        if username is not None and password is not None:
            tempobj = connect()
            tempobj.VerfiyDetails(username, password)

    def CreateUsernamePassword(self, newuserid=None, newpassword=None):

        if newuserid is not None and newpassword is not None:
            self.username = newuserid
            self.password = newpassword

        if self.username == '' or self.password == '':
            raise NotValidUsernameAndPassword()
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*',
                   '(', ')', '-', '=', '+', '[', ']', '{', '}', ';', ':', '"', "'", ',', '|']

        for i in symbols:
            if i in self.username:
                raise NotValidUsernameAndPassword()

        file_path = os.path.join(current_path, "userdetail.csv")
        row = []
        with open(file_path, 'a+') as fh:
            fh.seek(0)
            er = csv.reader(fh)
            for rec in er:
                row.extend(rec)
                if self.username in row:
                    raise UseralreadyExist()

        if newuserid == None and newpassword == None:
            try:
                with open(file_path, 'a+') as fh:
                    hasedpass = HashPassword(self.password)
                    data = [self.username, hasedpass]
                    ew = csv.writer(fh)
                    ew.writerow(data)
                    fh.seek(0)
                    fh.close()
                return True
            except Exception as e:
                raise e
        else:
            try:
                with open(file_path, 'a+') as fh:
                    hasedpass = HashPassword(self.password)
                    data = [self.username, hasedpass]
                    ew = csv.writer(fh)
                    ew.writerow(data)
                    fh.seek(0)
                    fh.close()
                return True
            except Exception as e:
                raise e

    def CreateDatabase(self, newdatabasename=None):
        if check:
            self.databasename = newdatabasename
            try:
                if newdatabasename is None or self.databasename is None:
                    raise DatabaseNameNotProvided()
                elif type(self.databasename) == str:
                    database_path = os.path.join(
                        current_path, "databasenames.csv")
                    with open(database_path, 'a+') as fh:
                        fh.seek(0)
                        ewrite = csv.writer(fh)
                        names = [self.databasename]
                        ewrite.writerow(names)
                        fh.seek(0)
                        fh.close()
                    try:
                        temp_path = os.path.join(
                            current_path, f'{self.databasename}')
                        os.mkdir(temp_path)
                    except Exception as e:
                        raise DatabasealreadyExist(e)

            except Exception as e:
                raise e
        else:
            raise NotVerfiedUsernamePassword()

    def VerfiyDetails(self, userid_, password_):
        global check
        self.username = userid_
        self.password = password_
        if self.username == '' or self.password == '':
            raise NotValidUsernameAndPassword()
        try:
            with open(file_path, 'a+', newline='\r\n') as f_file:
                f_file.seek(0)
                er = csv.reader(f_file)
                row = []
                for rec in er:
                    if userid_ in rec:
                        row.extend(rec)
                        break
                try:
                    if VerfiyPassword(self.password, row[1]):
                        check = True
                        return check
                    else:
                        check = False
                        return check
                except Exception as e:
                    check = False
                    raise IncorrectPassword(e)
        except Exception as e:
            raise e

    def CurrentUser(self):
        if check:
            if self.username is None:
                raise NotVerfiedUsernamePassword("not enter username password")
            else:
                return f'User: {self.username}'
        else:
            raise NotVerfiedUsernamePassword()

    def ChangePassword(self, username_, oldpassword, newpassword):
        if check:
            file_path = os.path.join(current_path, "userdetail.csv")
            with open(file_path, 'a+') as fh:
                fh.seek(0)
                er = csv.reader(fh)
                row = []
                for rec in er:
                    row.extend(rec)
                    if username_ in row:
                        if VerfiyPassword(oldpassword, row[1]):
                            temp = row[1]
                            temp = HashPassword(temp)
                            UpdateCsvValue(file_path, temp, newpassword)
                        else:
                            raise IncorrectPassword()
                    else:
                        raise UserNotFound()
        else:
            raise NotVerfiedUsernamePassword()

    def CreateTable(self, tablename):
        if databasechecker and check:
            try:
                table_path = os.path.join(current_path, f"{self.databasename}")
                table_path = os.path.join(table_path, f'{tablename}.csv')
                with open(table_path, 'a+') as fh:
                    writere = csv.writer(fh)
                    fh.close()
                return True
            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            if check == False:
                raise NotVerfiedUsernamePassword()
            elif databasechecker == False:
                raise DatabaseNotSelected()

    def RemoveDatabase(self, removedatabasename):
        if check:
            try:
                current_path = os.getcwd()
                databasenamesfilepath = os.path.join(
                    current_path, f'databasenames.csv')
                databasepath = os.path.join(
                    current_path, f'{removedatabasename}')
                UpdateCsvValue(databasenamesfilepath,
                               old_value=removedatabasename, new_value=None)
                shutil.rmtree(databasepath)

            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            raise NotVerfiedUsernamePassword()

    def RemoveTable(self, databasename, removetablename):
        if check and databasechecker:
            current_path = os.getcwd()
            databasepath = os.path.join(current_path, f'{databasename}')
            tablepath = os.path.join(databasepath, f'{removetablename}.csv')
            os.remove(tablepath)
        else:
            if check:
                raise DatabaseNotSelected()
            else:
                raise NotVerfiedUsernamePassword()

    def UpdateTableValues(self, tablename, oldvalue, newvalue):

        if check:
            current_path = os.getcwd()
            databasepath = os.path.join(current_path, f'{self.databasename}')
            tablepath = os.path.join(databasepath, f'{tablename}.csv')
            UpdateCsvValue(file_path=tablepath,
                           old_value=oldvalue, new_value=newvalue)
        else:
            if check:
                raise DatabaseNotSelected()
            else:
                raise NotVerfiedUsernamePassword()

    def ConnectTable(self, tablename1, tablename2):
        if databasechecker and check:
            try:
                current_path = os.getcwd()
                databasepath = os.path.join(
                    current_path, f'{self.databasename}')
                tablepath1 = os.path.join(databasepath, f'{tablename1}.csv')
                tablepath2 = os.path.join(databasepath, f'{tablename2}.csv')
                with open(tablepath1, 'r', newline='\r\n') as fh1, open(tablepath2, 'r', newline='\r\n') as fh2:
                    eread1 = csv.reader(fh1)
                    data1 = list(eread1)
                    for i in data1:
                        if i == []:
                            data1.remove(i)
                    eread2 = csv.reader(fh2)
                    data2 = list(eread2)
                    for i in data2:
                        if i == []:
                            data2.remove(i)
                # Render logic here using data1 and data2
                    for i in range(min(len(data1), len(data2))):
                        row1 = data1[i]
                        row2 = data2[i]
                        if row1 != row2:
                            # Yield the result for different rows
                            yield f"Row {i + 1}: {row1} - {row2}"

            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            if check:
                raise DatabaseNotSelected()
            else:
                raise NotVerfiedUsernamePassword()

    def InsertIntoTable(self, tablename, values=[]):

        if databasechecker and check:
            try:
                table_path = os.path.join(current_path, f'{self.databasename}')
                table_path = os.path.join(table_path, f'{tablename}.csv')
                with open(table_path, 'a+') as fh:
                    fh.seek(0)
                    write = csv.writer(fh)
                    write.writerow(values)
            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            if check == False:
                raise NotVerfiedUsernamePassword()
            elif databasechecker == False:
                raise DatabaseNotSelected()

    def FetchTable(self, tablename):
        if databasechecker and check:
            try:
                table_path = os.path.join(current_path, f'{self.databasename}')
                table_path = os.path.join(table_path, f'{tablename}.csv')
                with open(table_path, 'a+', newline='\r\n') as fh:
                    fh.seek(0)
                    eread = csv.reader(fh)
                    for i in eread:
                        if i == []:
                            pass
                        else:
                            yield i
            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            if check == False:
                raise NotVerfiedUsernamePassword()
            elif databasechecker == False:
                raise DatabaseNotSelected()

    def UseDatabase(self, databasen=None):
        global databasechecker
        if databasen is None and self.databasename is None:
            raise DatabaseNameNotProvided()
        elif databasen is not None and self.databasename is None:
            self.databasename = databasen

        file_path = os.path.join(current_path, "databasenames.csv")
        with open(file_path, 'r', newline='\r\n') as fh:
            reade = csv.reader(fh)
            for rec in reade:
                try:
                    if rec[0] == self.databasename:
                        databasechecker = True
                        break
                    else:
                        databasechecker = False
                        continue
                except IndexError:
                    continue

# ----------------helper function----------------


def HashPassword(password):
    "return hash value of string or any value"
    try:
        hash_obj = hashlib.sha256((password).encode('utf-8'))
        return hash_obj.hexdigest()
    except Exception as e:
        raise e


def VerfiyPassword(password, stored_password):
    "return True if password match otherwise false"
    try:
        hashed_password = HashPassword(password)
        return hashed_password == stored_password
    except Exception:
        raise Exception


def UserDetails(user='', passs=''):
    with open(file_path, 'a+', newline='\r\n') as f_user:
        writer = csv.writer(f_user)

        if user == '' and passs == '':
            raise NouseridPassword()
        else:
            hashed_password = HashPassword(passs)
            data = [user, hashed_password]
            writer.writerow(data)
            f_user.close()


def UpdateCsvValue(file_path, old_value, new_value=None):

    # Read the CSV file and store the data in a list
    with open(file_path, 'r') as file:
        reade = csv.reader(file)
        data = list(reade)

    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == old_value:
                data[row][col] = new_value
                break
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
