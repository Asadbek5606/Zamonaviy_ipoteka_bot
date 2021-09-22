# import sqlite3
from datetime import datetime

from django.db.models import Q

from ...models import User, New, Category, Product, Comment


class Database:
    def create_user(self, chat_id):

        try:
            user = User.objects.create(chat_id=chat_id)
        except Exception as e:
            print(e)


    def get_user_by_chat_id(self, chat_id):
        try:
            user = User.objects.get(chat_id=chat_id)
            return user
        except Exception as e:
            print(e)

    def update_user_data(self, chat_id, key, value):
        try:
            user = User.objects.get(chat_id=chat_id)
            user = User.objects.update(
                Q(key=key),
                Q(value=value)
            )
        except Exception as e:
            print(e)
        return user
    #     def update_user_data(self, chat_id, key, value):
    #         self.cur.execute(f"""update user set {key} = ? where chat_id = ?""", (value, chat_id))
    #         self.conn.commit()


    def get_all_users(self):
        try:
            user = User.objects.all()
        except Exception as e:
            print(e)
        return user

        # def get_all_users(self):
        #     self.cur.execute("""select * from user""")
        #     user = dict_fetchall(self.cur)
        #     return user

    def get_news(self):
        try:
            news = New.objects.all()
        except Exception as e:
            print(e)
        return news

#     def get_news(self):
#         self.cur.execute(
#             """select * from 'ugc_new'"""
#         )
#         news=dict_fetchall(self.cur)
#         return news


    def get_categories_by_parent_category_name(self, name):
        try:
            category = Category.objects.get(
                name_uz = name
            )
            categories = Category.objects.filter(parent=category.id)
        except Exception as e:
            print(e)
        return categories

    #     def get_categories_by_parent_category_name(self, name):
    #         self.cur.execute("""select * from category
    #         where parent_id = (select id from category where name_uz=?)""", (name,))
    #         categories = dict_fetchall(self.cur)
    #         return categories


    def get_category_id_by_name(self, name):
        try:
            category_id = Category.objects.get(id).filter(id__in__name_uz=name)
        except Exception as p:
            print(e)

        return category_id

    #     def get_category_id_by_name(self, name):
    #         self.cur.execute("""select id from category where name_uz=?""", (name,))
    #         category_id = dict_fetchone(self.cur)
    #         return category_id

    def get_products_by_category(self, category_id):
        try:
            products = Product.objects.filter(category_id=category_id)
        except Exception as e:
            print(e)
        return products


#     def get_products_by_category(self, category_id):
#         self.cur.execute("""select * from product where category_id = ?""", (category_id, ))
#         products = dict_fetchall(self.cur)
#         return products


    def create_comment(self, user_id, username, comment_text):
        try:
            comment = Comment.objects.create(user_id=user_id, username=username, comment_text=comment_text)
        except Exception as e:
            print(e)

        return comment

    #     def create_comment(self,user_id,username,comment):
    #         self.cur.execute("""insert into comment(user_id, comment_text, username) values (?, ?, ?)""",
    #                          (user_id,comment,username))
    #         self.conn.commit()

    def get_category_parent(self, category_id):
        try:
            category = Category.objects.get(parent_id__id=category_id)
        except Exception as e:
            print(e)
        return category

#     def get_category_parent(self, category_id):
#         self.cur.execute("""select parent_id from category where id = ?""", (category_id, ))
#         category = dict_fetchone(self.cur)
#         return category


    def get_categories_by_parent(self, name_uz=None, parent_id=None):
        if parent_id:
            categories = Category.objects.filter(parent_id=parent_id)
        elif name_uz:
            categories = Category.objects.filter(name_uz=name_uz)
        else:
            categories = Category.objects.filter(parent_id=None)

        return categories


#     def get_categories_by_parent(self, name_uz=None, parent_id=None):
#         if parent_id:
#             self.cur.execute("""select * from category where parent_id = ?""", (parent_id,))
#         elif name_uz:
#             self.cur.execute("""select * from category where name_uz = ?""", (name_uz,))
#         else:
#             self.cur.execute("""select * from category where parent_id is NULL""")
#
#         categories = dict_fetchall(self.cur)
#         return categories


    def get_product_by_id(self, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
        except Exception as e:
            print(e)

        return product


    # def get_product_by_id(self, product_id):
#         self.cur.execute("""select * from product where id = ?""", (product_id, ))
#         product = dict_fetchone(self.cur)
#         return product




# class Database:
#     def __init__(self, db_name):
#         self.conn = sqlite3.connect(db_name, check_same_thread=False)
#         self.cur = self.conn.cursor()
#
#     def create_user(self, chat_id):
#
#         self.cur.execute("""insert into user(chat_id) values (?)""", (chat_id,))
#         self.conn.commit()
#
#     def update_user_data(self, chat_id, key, value):
#         self.cur.execute(f"""update user set {key} = ? where chat_id = ?""", (value, chat_id))
#         self.conn.commit()
#

#     def get_user_by_chat_id(self, chat_id):
#         user = User.objects.get(chat_id=chat_id)
#         # self.cur.execute("""select * from user where chat_id = ?""", (chat_id, ))
#         # user = dict_fetchone(self.cur)
#         return user
# ###########GET ALL USERS#########
#     def get_all_users(self):
#         self.cur.execute("""select * from user""")
#         user = dict_fetchall(self.cur)
#         return user
# #################
#

#
#     def get_categories_by_parent_category_name(self, name):
#         self.cur.execute("""select * from category
#         where parent_id = (select id from category where name_uz=?)""", (name,))
#         categories = dict_fetchall(self.cur)
#         return categories
#

#

#
#
#
#     def get_about_us(self):
#         self.cur.execute("""select * from about_us""")
#         about_us = dict_fetchall(self.cur)
#         return about_us
#
#     def get_product_for_cart(self, product_id):
#         self.cur.execute(
#             """select product.*, category.name_uz as cat_name_uz, category.name_ru as cat_name_ru
#             from product inner join category on product.category_id = category.id where product.id = ?""",
#             (product_id, )
#         )
#         product = dict_fetchone(self.cur)
#         return product
#
#     def create_order(self, user_id, products, payment_type, location):
#         self.cur.execute(
#             """insert into "order"(user_id, status, payment_type, longitude, latitude, created_at) values (?, ?, ?, ?, ?, ?)""",
#             (user_id, 1, payment_type, location.longitude, location.latitude, datetime.now())
#         )
#         self.conn.commit()
#         self.cur.execute(
#             """select max(id) as last_order from "order" where user_id = ?""", (user_id, )
#         )
#         last_order = dict_fetchone(self.cur)['last_order']
#         for key, val in products.items():
#             self.cur.execute(
#                 """insert into "order_product"(product_id, order_id, amount, created_at) values (?, ?, ?, ?)""",
#                 (int(key), last_order,  int(val), datetime.now())
#             )
#         self.conn.commit()
#
#     def get_user_orders(self, user_id):
#         self.cur.execute(
#             """select * from "order" where user_id = ? and status = 1""", (user_id, )
#         )
#         orders = dict_fetchall(self.cur)
#         return orders
#
#     def get_order_products(self, order_id):
#         self.cur.execute(
#             """select order_product.*, product.name_uz as product_name_uz, product.name_ru as product_name_ru,
#             product.price as product_price from order_product inner join product on order_product.product_id = product.id
#             where order_id = ?""", (order_id, ))
#         products = dict_fetchall(self.cur)
#         return products
#



# def dict_fetchall(cursor):
#     columns = [col[0] for col in cursor.description]
#     return [
#         dict(zip(columns, row))
#         for row in cursor.fetchall()
#     ]
#
#
# def dict_fetchone(cursor):
#     row = cursor.fetchone()
#     if row is None:
#         return False
#     columns = [col[0] for col in cursor.description]
#     return dict(zip(columns, row))
