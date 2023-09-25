from my_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
from my_app import app
from my_app.models import user as usr
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PRICE_REGEX = re.compile ('^[-]?([1-9]{1}[0-9]{0,}(\.[0-9]{0,2})?|0(\.[0-9]{0,2})?|\.[0-9]{1,2})$')
# https://regexlib.com/(X(1)A(fH_1Zt9K-8cpSgQTkrRifgmQGG9_C-Q_nLDDM0bZ_HAJyCPjikPUVkFmyDSRfXHd0y0l-1fub1ngpEjEmN6CdLADFL85f4_7YNGUIdhRrF7Fmy5NFeACH6yBudcBPgI9IhxXaIm_en0YE53IcuWaDHWQdi6uGqzLzoxxwJyHkOo0Xvq3grGx5WVaa4hXAj_E0))/Search.aspx?k=currency&AspxAutoDetectCookieSupport=1



class Painting:
    db = "painters_db"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.users = None


    @classmethod
    def get_one_painting(cls, data):
        query = "SELECT * FROM paintings WHERE paintings.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])


    @classmethod
    def get_all_paintings_with_users(cls):
        query = "SELECT * FROM users JOIN paintings ON users.id = paintings.user_id WHERE users.id = paintings.user_id;"
        paintings_from_db = connectToMySQL(cls.db).query_db(query)
        all = []
        print("JOIN QUERY", paintings_from_db)
        #painting_instance = cls(paintinges_from_db[0])
        if not paintings_from_db:
            print("NO RESULTS FROM JOIN QUERY")
            return False
            # print("USER_INSTANCE:", painting_instance)
            # print("USERS_FROM_DB:", paintinges_from_db)
            # return painting_instance
        for painting in paintings_from_db:

            user_data= {
                'id':painting['id'],
                'first_name':painting['first_name'],
                'last_name':painting['last_name'],
                'email':painting['email'],
                'password':painting['password'],
                'created_at':painting['created_at'],
                'updated_at':painting['updated_at']
            }

            painting_data = {
                'id' : painting['paintings.id'],
                'title' : painting['title'],
                'description' : painting['description'],
                'price' : painting['price'],
                'user_id' : painting['user_id'],
                'created_at' : painting['paintings.created_at'],
                'updated_at' : painting['paintings.updated_at']
            }

            painting_inst = cls(painting_data)
            painting_inst.users = usr.User(user_data)
            all.append(painting_inst)
        return all


    @classmethod
    def get_painting_with_user(cls, data):
        query = "SELECT * FROM users JOIN paintings ON users.id = paintings.user_id WHERE paintings.id = %(id)s;"
        painting_from_db = connectToMySQL(cls.db).query_db(query, data)
        if not painting_from_db:
            print("NO RESULTS FROM JOIN QUERY")
            return False
            # print("USER_INSTANCE:", painting_instance)
            # print("USERS_FROM_DB:", paintinges_from_db)
            # return painting_instance
        print("PAINTING FROM DB: ", painting_from_db)
        user_data= {
            'id':painting_from_db[0]['id'],
            'first_name':painting_from_db[0]['first_name'],
            'last_name':painting_from_db[0]['last_name'],
            'email':painting_from_db[0]['email'],
            'password':painting_from_db[0]['password'],
            'created_at':painting_from_db[0]['created_at'],
            'updated_at':painting_from_db[0]['updated_at']
        }

        painting_data = {
            'id' : painting_from_db[0]['paintings.id'],
            'title' : painting_from_db[0]['title'],
            'description' : painting_from_db[0]['description'],
            'price' : painting_from_db[0]['price'],
            'user_id' : painting_from_db[0]['user_id'],
            'created_at' : painting_from_db[0]['paintings.created_at'],
            'updated_at' : painting_from_db[0]['paintings.updated_at']
        }

        painting_inst = cls(painting_data)
        painting_inst.users = usr.User(user_data)
        return painting_inst



    @classmethod
    def get_user_paintings(cls, data):
        query = "SELECT * FROM users LEFT JOIN paintings ON users.id = paintings.user_id WHERE paintings.user_id = %(id)s;"
        paintings_from_db = connectToMySQL(cls.db).query_db(query, data)
        print('PAINTINGS FROM DB',paintings_from_db)
        if not paintings_from_db:
            print("NO RESULTS FROM JOIN QUERY")
            return False
            # print("USER_INSTANCE:", painting_instance)
            # print("USERS_FROM_DB:", paintinges_from_db)
            # return painting_instance
        print("PAINTING FROM DB: ", paintings_from_db)
        all = []
        for painting in paintings_from_db:
            user_data= {
                'id':painting['id'],
                'first_name':painting['first_name'],
                'last_name':painting['last_name'],
                'email':painting['email'],
                'password':painting['password'],
                'created_at':painting['created_at'],
                'updated_at':painting['updated_at']
            }

            painting_data = {
                'id' : painting['paintings.id'],
                'title' : painting['title'],
                'description' : painting['description'],
                'price' : painting['price'],
                'user_id' : painting['user_id'],
                'created_at' : painting['paintings.created_at'],
                'updated_at' : painting['paintings.updated_at']
            }

            painting_inst = cls(painting_data)
            painting_inst.users = usr.User(user_data)
            all.append(painting_inst)
        return all


    @staticmethod
    def validate_painting(data):
        is_valid = True # we assume this is true
        if data['title'] == "":
            flash("A title is required")
            is_valid = False
        elif len(data['title']) < 2:
            flash("Title must be at least 2 characters.")
            is_valid = False

        if data['description'] == "":
            flash("A description is required")
            is_valid = False
        elif len(data['description']) < 11:
            flash("Description must be at least 10 characters.")
            is_valid = False

        if data['price'] == "":
            flash("A price is required")
            is_valid = False
        elif not PRICE_REGEX.match(data['price']):
            flash("Price must be numeric")
            is_valid = False
            return is_valid
        elif float(data['price']) < 0:
                flash("Price can not be less than 0")
                is_valid = False

        return is_valid


    @classmethod
    def save_painting(cls, data):
        print("data:", data)
        query = "INSERT INTO paintings(title, description, price, user_id, created_at, updated_at) VALUES(%(title)s, %(description)s, %(price)s, %(user_id)s, NOW(), NOW());"

        data = {
            'title':data['title'],
            'description':data['description'],
            'price':data['price'],
            'user_id':data['user_id']
        }
        return connectToMySQL(cls.db).query_db(query, data) # returns id of object created/inserted



    @classmethod
    def update_painting(cls, data):
        data = {
            'title' : data['title'],
            'description' : data['description'],
            'price' : data['price'],
            'user_id' : data['user_id'],
            'id': data['id']
        }
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, user_id = %(user_id)s, updated_at = NOW() WHERE paintings.id =  %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)



    @classmethod
    def delete_painting(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)







##########################################################
######   NONE EDITED ROUTES BELOW     ###################
##########################################################





#     @classmethod
#     def get_email(cls,data):
#         query = "SELECT * FROM paintings WHERE email = %(email)s;"
#         result = connectToMySQL("mydb").query_db(query,data)
#         if len(result) < 1:
#             return False
#         return cls(result[0])


#     @classmethod
#     def save_new_painting(cls, data):
#         pw_hash = bcrypt.generate_password_hash(data['password'])
#         print("pw_hash", pw_hash)
#         data = {
#             "first_name": data['first_name'],
#             "last_name" : data['last_name'],
#             "email" : data['email'],
#             "password" : pw_hash,
#         }
#         query = "INSERT INTO paintings(first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
#         return connectToMySQL(cls.db).query_db(query, data)


#     @classmethod
#     def save_new_password(cls, data):
#         pw_hash = bcrypt.generate_password_hash(data['password'])
#         print("pw_hash", pw_hash)
#         data = {
#             "password" : pw_hash,
#         }
#         query = "INSERT INTO paintings(password, updated_at) VALUES(%(password)s, NOW());"
#         return connectToMySQL(cls.db).query_db(query, data)


#     @staticmethod
#     def validate_registration(data):
#         is_valid = True # we assume this is true
#         if len(data['first_name']) < 2 or len( data['last_name']) < 2:
#             flash("First and Last Name  must be at least 2 characters.")
#             is_valid = False

#         if not data['first_name'].isalpha() or not data['last_name'].isalpha():
#             flash("First and Last Name can not contain numbers")
#             is_valid = False

#         if len(data['password']) < 8 or len(data['confirm_password']) < 8:
#             flash("Password must be at least 8 characters")
#             is_valid = False

#         if data['password'] != data['confirm_password']:
#             flash("Passwords do not match")
#             is_valid = False

#         if not EMAIL_REGEX.match(data['email']):
#             flash("Invalid email address!")
#             is_valid = False

#         email = {'email' : data['email']}
#         painting = painting.get_one_by_email(email)
#         if len(painting) > 0:
#             flash("The email you entered is already associated with an account.")
#             is_valid = False
#         return is_valid


#     @classmethod
#     def get_one_by_email(cls, data):
# #        print('get_one_by_email  email:', data)
#         query = "SELECT * FROM paintings where email = %(email)s;"
# #        print(connectToMySQL(cls.db).query_db(query, data))
#         return (connectToMySQL(cls.db).query_db(query, data))


#     @staticmethod
#     def validate_login(data):
#         is_valid = True
#         email = {'email' : data['email']}
#         print(email)
#         painting = painting.get_one_by_email(email)
#         print('painting', painting)
#         if len(painting) == 0:
#             flash("No account exists with this email")
#             is_valid = False
#             return is_valid
#         if (data['first_name'] != painting[0]['first_name']) or (data['last_name'] != painting[0]['last_name']):
#             flash("Invalid login credentials")
#             is_valid = False
#         if len(painting) != 1:
#             flash("Invalid login credentials")
#             is_valid = False
#         elif is_valid and not bcrypt.check_password_hash(painting[0]['password'], data['password']):
#             flash("Invalid login credentials")
#             is_valid = False
#         return is_valid



#     @staticmethod
#     def painting_edit_validation(data):
#         is_valid = True # we assume this is true
#         if len(data['first_name']) < 2 or len( data['last_name']) < 2:
#             flash("First and Last Name  must be at least 2 characters.")
#             is_valid = False

#         if not data['first_name'].isalpha() or not data['last_name'].isalpha():
#             flash("First and Last Name can not contain numbers")
#             is_valid = False

#         if not EMAIL_REGEX.match(data['email']):
#             flash("Invalid email address!")
#             is_valid = False

#         email = { 'email' : data['email'] }
#         painting = painting.get_one_by_email(email)
#         if painting:
#             if (data['id'] != painting[0]['id']) and (data['email'] == painting[0]['email']):
#                 flash("The email you entered is already associated with another account.")
#                 is_valid = False

#         return is_valid


#     @staticmethod
#     def painting_edit_password_validation(data):
#         is_valid = True
#         painting_id = { 'id' :  data['id'] }
#         pw = data['password']
#         confirm_pw = data['confirm_password']
#         new_pw = data['new_password']
#         new_confirm_pw = data['confirm_new_pw']

#         painting = painting.get_one(painting_id)
#         if not bcrypt.check_password_hash(painting.password, data['password']):
#             flash("Invalid Password")
#             is_valid = False
#         if pw != confirm_pw:
#             flash("Confirm password must match password")
#             is_valid = False
#         if len(new_pw) < 8 or len(new_confirm_pw) < 8:
#             flash("Password must be at least 8 characters")
#             is_valid = False
#         if new_pw != new_confirm_pw:
#             flash("Confirm new password must match new password")
#             is_valid = False
#         return is_valid


#     @classmethod
#     def update_name_email(cls, data):
#         data = {
#             'id' : data['id'],
#             "first_name": data['first_name'],
#             "last_name" : data['last_name'],
#             "email" : data['email']
#         }
#         query = "UPDATE paintings SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE paintings.id = %(id)s;"
#         return connectToMySQL(cls.db).query_db(query, data)


#     @classmethod
#     def update_password(cls, data):
#         pw_hash = bcrypt.generate_password_hash(data['password'])
#         data = {
#             "id" : data['id'],
#             "password" : pw_hash
#         }
#         query = "UPDATE paintings SET password = %(password)s, updated_at = NOW() WHERE paintings.id = %(id)s;"
#         return connectToMySQL(cls.db).query_db(query, data)




#     @classmethod
#     def get_all_complete(cls):
#         # query = "SELECT * FROM recipes JOIN paintinges ON paintinges.id = recipes.painting_id WHERE paintinges.id = recipes.painting_id;"
#         query = "SELECT * FROM paintings JOIN paintinges ON paintinges.painting_id = paintings.id WHERE paintinges.painting_id = paintings.id;"
#         paintinges_from_db = connectToMySQL(cls.db).query_db(query)
#         all = []
#         print("JOIN QUERY", paintinges_from_db)
#         #painting_instance = cls(paintinges_from_db[0])
#         if not paintinges_from_db:
#             print("NO RESULTS FROM JOIN QUERY")
#             return False
#             # print("painting_INSTANCE:", painting_instance)
#             # print("paintingS_FROM_DB:", paintinges_from_db)
#             # return painting_instance
#         for painting in paintinges_from_db:

#             painting_data= {
#                 'id':painting['id'],
#                 'first_name':painting['first_name'],
#                 'last_name':painting['last_name'],
#                 'email':painting['email'],
#                 'password':painting['password'],
#                 'created_at':painting['created_at'],
#                 'updated_at':painting['updated_at']
#             }

#             painting_data = {
#                 'id' : painting['paintinges.id'],
#                 'location' : painting['location'],
#                 'what_happened' : painting['what_happened'],
#                 'date' : painting['date'],
#                 'number' : painting['number'],
#                 'painting_id' : painting['painting_id'],
#                 'created_at' : painting['paintinges.created_at'],
#                 'updated_at' : painting['paintinges.updated_at']
#             }

#             painting_inst = cls(painting_data)
#             painting_inst.paintinges = sas.painting(painting_data)
#             all.append(painting_inst)
#             print('ALL: ', all)
#         return all


#     # @classmethod
#     # def get_all_with_recipes(cls):
#     #     # query = "SELECT * FROM recipes JOIN paintings ON paintings.id = recipes.painting_id WHERE paintings.id = recipes.painting_id;"
#     #     query = "SELECT * FROM paintings JOIN recipes ON paintings.id = recipes.painting_id WHERE paintings.id = recipes.painting_id;"
#     #     paintings_from_db = connectToMySQL(cls.db).query_db(query)
#     #     all = []
#     #     print("JOIN QUERY", paintings_from_db)
#     #     #painting_instance = cls(paintings_from_db[0])
#     #     if not paintings_from_db:
#     #         print("NO RESULTS FROM JOIN QUERY")
#     #         return False
#     #         # print("painting_INSTANCE:", painting_instance)
#     #         # print("paintingS_FROM_DB:", paintings_from_db)
#     #         # return painting_instance
#     #     for usr in paintings_from_db:
#     #         recipe_data = {
#     #             'id':usr['recipes.id'],
#     #             'name':usr['name'],
#     #             'date':usr['date'],
#     #             'time':usr['time'],
#     #             'description':usr['description'],
#     #             'instructions':usr['instructions'],
#     #             'painting_id':usr['painting_id'],
#     #             'created_at':usr['recipes.created_at'],
#     #             'updated_at':usr['recipes.updated_at']
#     #         }

#     #         painting_data= {
#     #             'id':usr['id'],
#     #             'first_name':usr['first_name'],
#     #             'last_name':usr['last_name'],
#     #             'email':usr['email'],
#     #             'password':usr['password'],
#     #             'created_at':usr['created_at'],
#     #             'updated_at':usr['updated_at']
#     #         }
#     #         painting_inst = cls(painting_data)
#     #         painting_inst.recipes = recipe.Recipe(recipe_data)
#     #         all.append(painting_inst)
#     #     return all


#     # @classmethod
#     # def get_painting(cls, data):
#     #     query = "SELECT * FROM paintings WHERE id = %(id)s"
#     #     painting_from_db = connectToMySQL(cls.db).query_db(query,data)
#     #     return cls(painting_from_db[0])


#     # # @classmethod
#     # # def save(cls, data):
#     # #     query = "INSERT INTO paintings(first_name, last_name, email) VALUES(%(first_name)s, %(last_name)s,%(email)s);"
#     # #     return connectToMySQL(cls.db).query_db(query,data)



#     # @classmethod
#     # def edit_painting(cls, data):
#     #     query = "UPDATE paintings SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s;"
#     #     data = {
#     #         'first_name' : data['first_name'],
#     #         'last_name' : data['last_name'],
#     #         'email' : data['email']
#     #     }
#     #     return connectToMySQL(cls.db).query_db(query,data)





#     # @classmethod
#     # def delete_painting(cls, data):
#     #     query = "DELETE FROM paintings WHERE id = %()s"
#     #     return connectToMySQL(cls.db).query_db(query,data)


#     # @classmethod
#     # def delete_paintings(cls, data):
#     #     query = "TRUNCATE TABLE paintings"
#     #     return connectToMySQL(cls.db).query_db(query, data)