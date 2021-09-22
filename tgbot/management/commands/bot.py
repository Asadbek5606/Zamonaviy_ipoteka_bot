from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram.utils.request import Request
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import (
    InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction
)
import requests

from .database import Database
from . import globals
from . import methods
import os

ADMIN_ID = settings.TGADMINID

base_path = settings.BASE_DIR
# base_path1 = base_path.replace(os.sep, '/')
db = Database()


def check(update, context):
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)
    contact_valid = context.user_data.get("contact_valid", 0)

    if not db_user:
        db.create_user(user.id)
        buttons = [
            [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU)]
        ]
        update.message.reply_text(text=globals.WELCOME_TEXT)
        update.message.reply_text(
            text=globals.CHOOSE_LANG,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["lang_id"]:
        buttons = [
            [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU)]
        ]
        update.message.reply_text(
            text=globals.CHOOSE_LANG,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["phone_number"]:
        buttons = [
            [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]
        ]
        if contact_valid == 0:
            update.message.reply_text(
                text=globals.TEXT_ENTER_CONTACT[db_user['lang_id']],
                parse_mode='HTML',
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=buttons,
                    resize_keyboard=True
                )
            )
        else:
            if db_user["lang_id"] == 1:
                update.message.reply_text(
                    text=f'Telefon nomer xato kiritildi, qayta yuboring yoki  "<b>{globals.BTN_SEND_CONTACT[db_user["lang_id"]]}</b>" tugmasini bosing.',
                    parse_mode='HTML'
                )
            else:
                update.message.reply_text(
                    text=f'Номер телефона введен неправильно, отправьте его повторно или нажмите "<b>{globals.BTN_SEND_CONTACT[db_user["lang_id"]]}</b>."',
                    parse_mode='HTML'
                )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["verify"]:
        if db_user['verify_counter'] == 0:
            update.message.reply_text(
                text=globals.VERIFY[db_user['lang_id']],
                reply_markup=ReplyKeyboardRemove()
            )

        elif db_user['verify_counter'] == 3:
            buttons = [
                [KeyboardButton(text=globals.BTN_RESEND_VERIFY_CODE[db_user['lang_id']])]
            ]
            update.message.reply_text(
                text=globals.TEXT_ERROR_VERIFY_CODE[db_user['lang_id']],
                parse_mode='HTML',
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=buttons,
                    resize_keyboard=True
                )
            )
            context.user_data["state"] = globals.STATES["reg"]

        else:
            update.message.reply_text(
                text=globals.TEXT_VERIFY_WARNING[db_user['lang_id']],
                reply_markup=ReplyKeyboardRemove()
            )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["first_name"]:
        update.message.reply_text(
            text=globals.TEXT_ENTER_FIRST_NAME[db_user['lang_id']],
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["last_name"]:
        update.message.reply_text(
            text=globals.TEXT_ENTER_LAST_NAME[db_user['lang_id']],
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data["state"] = globals.STATES["reg"]

    else:
        methods.send_main_menu(context, user.id, db_user['lang_id'])
        context.user_data["state"] = globals.STATES["menu"]


def check_data_decorator(func):
    def inner(update, context):
        user = update.message.from_user
        db_user = db.get_user_by_chat_id(user.id)
        state = context.user_data.get("state", 0)
        step_verify = context.user_data.get("step_verify", 0)
        contact_valid = context.user_data.get("contact_valid", 0)

        if state != globals.STATES['reg']:
            if not db_user:
                db.create_user(user.id)
                buttons = [
                    [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU)]
                ]
                update.message.reply_text(text=globals.WELCOME_TEXT)
                update.message.reply_text(
                    text=globals.CHOOSE_LANG,
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=buttons,
                        resize_keyboard=True
                    )
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["lang_id"]:
                buttons = [
                    [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU)]
                ]
                update.message.reply_text(
                    text=globals.CHOOSE_LANG,
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=buttons,
                        resize_keyboard=True
                    )
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["phone_number"]:
                buttons = [
                    [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]
                ]
                if contact_valid == 0:
                    update.message.reply_text(
                        text=globals.TEXT_ENTER_CONTACT[db_user['lang_id']],
                        parse_mode='HTML',
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=buttons,
                            resize_keyboard=True
                        )
                    )
                else:
                    if db_user["lang_id"] == 1:
                        update.message.reply_text(
                            text=f'Telefon nomer xato kiritildi, qayta yuboring yoki  "<b>{globals.BTN_SEND_CONTACT[db_user["lang_id"]]}</b>" tugmasini bosing.',
                            parse_mode='HTML'
                        )
                    else:
                        update.message.reply_text(
                            text=f'Номер телефона введен неправильно, отправьте его повторно или нажмите "<b>{globals.BTN_SEND_CONTACT[db_user["lang_id"]]}</b>."',
                            parse_mode='HTML'
                        )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["verify"]:
                if db_user['verify_counter'] == 0:
                    update.message.reply_text(
                        text=globals.VERIFY[db_user['lang_id']],
                        reply_markup=ReplyKeyboardRemove()
                    )

                elif db_user['verify_counter'] == 3:
                    buttons = [
                        [KeyboardButton(text=globals.BTN_RESEND_VERIFY_CODE[db_user['lang_id']])]
                    ]
                    update.message.reply_text(
                        text=globals.TEXT_ERROR_VERIFY_CODE[db_user['lang_id']],
                        parse_mode='HTML',
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=buttons,
                            resize_keyboard=True
                        )
                    )
                    context.user_data["state"] = globals.STATES["reg"]

                else:
                    update.message.reply_text(
                        text=globals.TEXT_VERIFY_WARNING[db_user['lang_id']],
                        reply_markup=ReplyKeyboardRemove()
                    )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["first_name"]:
                update.message.reply_text(
                    text=globals.TEXT_ENTER_FIRST_NAME[db_user['lang_id']],
                    reply_markup=ReplyKeyboardRemove()
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["last_name"]:
                update.message.reply_text(
                    text=globals.TEXT_ENTER_LAST_NAME[db_user['lang_id']],
                    reply_markup=ReplyKeyboardRemove()
                )
                context.user_data["state"] = globals.STATES["reg"]

            else:
                return func(update, context)

            return False

        else:
            return func(update, context)

    return inner


def start_handler(update, context):
    check(update, context)


def get_currency(update):
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)
    lang_name = f"CcyNm_{globals.LANGUAGE_CODE[db_user['lang_id']].upper()}"
    url = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/"
    result = requests.get(url).json()
    codes = ['840', '978', '643']
    flags = ["🇺🇸", "🇪🇺", "🇷🇺"]
    answer = ''
    c = 0
    h = ""
    for i in result:
        if i["Code"] in codes:
            answer += f"{flags[c]} {i[lang_name]} = <strong>{i['Rate']}</strong>\t ({h}{i['Diff']})\n\n"
            c += 1
    print(f"{globals.CURRENCY.get(db_user['lang_id'], 0)}  {i['Date']}\n\n{answer}")
    update.message.reply_text(
        text=f"{globals.CURRENCY.get(db_user['lang_id'], 0)}  {i['Date']}\n\n{answer}",
        parse_mode="HTML"
    )


@check_data_decorator
def message_handler(update, context):
    global text
    message = update.message.text
    user = update.message.from_user
    state = context.user_data.get("state", 0)
    db_user = db.get_user_by_chat_id(user.id)
    lang_code = db_user['lang_id']
    verify_counter = db_user['verify_counter']

    if state == 0:
        check(update, context)

    elif state == 1:
        if not lang_code:
            if message == globals.BTN_LANG_UZ:
                db.update_user_data(user.id, "lang_id", 1)
                check(update, context)

            elif message == globals.BTN_LANG_RU:
                db.update_user_data(user.id, "lang_id", 2)
                check(update, context)

            else:
                update.message.reply_text(
                    text=globals.TEXT_LANG_WARNING
                )

        elif not db_user["phone_number"]:
            if update.message['entities']:
                if update.message['entities'][0]['type'] == 'phone_number':
                    db.update_user_data(user.id, "phone_number", message)
                    check(update, context)
            else:
                context.user_data["contact_valid"] = 1
                check(update, context)

        elif not db_user['verify']:
            if verify_counter == 3:
                if message == globals.BTN_RESEND_VERIFY_CODE[lang_code]:
                    db.update_user_data(user.id, 'verify_counter', 0)
                    check(update, context)
                else:
                    if lang_code == 1:
                        update.message.reply_text(
                            text=f'<b>"{globals.BTN_RESEND_VERIFY_CODE[lang_code]}"</b> tugmasini bosing',
                            parse_mode='HTML'
                        )
                    else:
                        update.message.reply_text(
                            text=f'Нажмите кнопку <b>"{globals.BTN_RESEND_VERIFY_CODE[lang_code]}"</b>',
                            parse_mode='HTML'
                        )

            elif verify_counter < 3:
                if message == '1111':
                    db.update_user_data(user.id, "verify", message)
                    update.message.reply_text(
                        text=globals.VERIFY_CONFIRMED[lang_code]
                    )
                    check(update, context)
                else:
                    verify_counter += 1
                    db.update_user_data(user.id, 'verify_counter', verify_counter)
                    check(update, context)

        elif not db_user["first_name"]:
            db.update_user_data(user.id, "first_name", message)
            check(update, context)

        elif not db_user["last_name"]:
            db.update_user_data(user.id, "last_name", message)
            buttons = [
                [KeyboardButton(text=globals.BTN_SEND_CONTACT[lang_code], request_contact=True)]
            ]
            check(update, context)

        else:
            check(update, context)

    elif state == 2:
        if message == globals.BTN_MENU[lang_code] or message == globals.BTN_MENU[lang_code].lower():
            methods.send_main_menu(context, user.id, lang_code)

        elif message == globals.BTN_SEND_NEWS[lang_code]:
            if user.id == ADMIN_ID:
                users = db.get_all_users()
                list1 = []
                for u in users:
                    list1.append(u['chat_id'])
                for ch in list1:
                    try:
                        news = db.get_news()
                        last_news = news[-1]
                        date = last_news["posted_at"].split(' ')[0]

                        if not last_news['image']:
                            context.bot.send_message(
                                chat_id=ch,
                                text=f"""<b>{last_news[f'heading_{globals.LANGUAGE_CODE[db_user["lang_id"]]}']}</b>\n{last_news[f'text_{globals.LANGUAGE_CODE[db_user["lang_id"]]}']}\n<i>{date}</i>""",
                                parse_mode="HTML"
                            )
                        else:
                            path1 = settings.MEDIA_ROOT
                            newPath = path1.replace(os.sep, '/')
                            context.bot.send_photo(
                                chat_id=ch,
                                photo=open(f'{newPath}/{last_news["image"]}', "rb"),
                                caption=f"""<b>{last_news[f'heading_{globals.LANGUAGE_CODE[db_user["lang_id"]]}']}</b>\n{last_news[f'text_{globals.LANGUAGE_CODE[db_user["lang_id"]]}']}\n<i>{date}</i>""",
                                parse_mode="HTML"
                            )
                    except Exception:
                        continue

        elif message == globals.BTN_SEND_NEWS[lang_code]:
            users = db.get_all_users()
            list1 = []
            for u in users:
                list1.append(u['chat_id'])
            for ch in list1:
                try:
                    news = db.get_news()
                    last_news = news[-1]
                    date = last_news["posted_at"].split(' ')[0]

                    if not last_news['image']:
                        context.bot.send_message(
                            chat_id=ch,
                            text=f"""<b>{last_news[f'heading_{globals.LANGUAGE_CODE[lang_code]}']}</b>\n{last_news[f'text_{globals.LANGUAGE_CODE[lang_code]}']}\n<i>{date}</i>""",
                            parse_mode="HTML"
                        )

                    else:
                        path1 = settings.MEDIA_ROOT
                        # newPath = path1.replace(os.sep, '/')
                        context.bot.send_photo(
                            chat_id=ch,
                            photo=open(f'{path1}/{last_news["image"]}', "rb"),
                            caption=f"""<b>{last_news[f'heading_{globals.LANGUAGE_CODE[lang_code]}']}</b>\n{last_news[f'text_{globals.LANGUAGE_CODE[lang_code]}']}\n<i>{date}</i>""",
                            parse_mode="HTML"
                        )

                except Exception:
                    continue

        elif message == globals.BTN_CREDITS[lang_code]:
            categories = db.get_categories_by_parent_category_name(name='credits')

            category_id = db.get_category_id_by_name(name='credits')
            products = db.get_products_by_category(category_id=category_id['id'])

            if categories:
                buttons = methods.send_category_buttons(categories=categories, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            elif products:
                buttons = methods.send_product_buttons(products=products, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            else:
                update.message.reply_text(
                    text='404 NOT FOUND'
                )

        elif message == globals.BTN_DEPOSITS[lang_code]:
            categories = db.get_categories_by_parent_category_name(name='deposits')

            category_id = db.get_category_id_by_name(name='deposits')
            products = db.get_products_by_category(category_id=category_id['id'])

            if categories:
                buttons = methods.send_category_buttons(categories=categories, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            elif products:
                buttons = methods.send_product_buttons(products=products, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            else:
                update.message.reply_text(
                    text='404 NOT FOUND'
                )

        elif message == globals.BTN_TRANSFERS[lang_code]:
            categories = db.get_categories_by_parent_category_name(name='transfers')

            category_id = db.get_category_id_by_name(name='transfers')
            products = db.get_products_by_category(category_id=category_id['id'])

            if categories:
                buttons = methods.send_category_buttons(categories=categories, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            elif products:
                buttons = methods.send_product_buttons(products=products, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            else:
                update.message.reply_text(
                    text='404 NOT FOUND'
                )

        elif message == globals.BTN_INFO[lang_code]:
            categories = db.get_categories_by_parent_category_name(name='info')

            category_id = db.get_category_id_by_name(name='info')
            products = db.get_products_by_category(category_id=category_id['id'])

            if categories:
                buttons = methods.send_category_buttons(categories=categories, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            elif products:
                buttons = methods.send_product_buttons(products=products, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            else:
                update.message.reply_text(
                    text='404 NOT FOUND'
                )

        elif message == globals.BTN_CURRENCY[lang_code]:
            print('enter currency')
            get_currency(update)

        elif message == globals.BTN_CARDS[lang_code]:
            categories = db.get_categories_by_parent_category_name(name='cards')

            category_id = db.get_category_id_by_name(name='cards')
            products = db.get_products_by_category(category_id=category_id['id'])

            if categories:
                buttons = methods.send_category_buttons(categories=categories, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            elif products:
                buttons = methods.send_product_buttons(products=products, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            else:
                text = '404 NOT FOUND'
                update.message.reply_text(
                    text=text,
                )

        elif message == globals.BTN_HELP[lang_code]:
            categories = db.get_categories_by_parent_category_name(name='help')

            category_id = db.get_category_id_by_name(name='help')
            products = db.get_products_by_category(category_id=category_id['id'])

            if categories:
                buttons = methods.send_category_buttons(categories=categories, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            elif products:
                buttons = methods.send_product_buttons(products=products, lang_id=lang_code)
                text = globals.TEXT_ORDER[lang_code]
                update.message.reply_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )
            else:
                text = '404 NOT FOUND'
                update.message.reply_text(
                    text=text,
                )

        elif message == globals.BTN_SETTINGS[lang_code]:
            buttons = [
                [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BACK[lang_code]), KeyboardButton(text=globals.BTN_LANG_RU)]
            ]
            update.message.reply_text(
                text=globals.CHOOSE_LANG,
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=buttons,
                    resize_keyboard=True
                )
            )
            context.user_data["state"] = globals.STATES["settings"]

    elif state == 3:
        if message == globals.BTN_LANG_UZ:
            db.update_user_data(db_user['chat_id'], "lang_id", 1)
            context.user_data["state"] = globals.STATES["reg"]
            check(update, context)

        elif message == globals.BTN_LANG_RU:
            db.update_user_data(db_user['chat_id'], "lang_id", 2)
            context.user_data["state"] = globals.STATES["reg"]
            check(update, context)
        elif message == globals.BACK[lang_code]:
            methods.send_main_menu(context, user.id, lang_code)
            context.user_data["state"] = globals.STATES["menu"]
        else:
            update.message.reply_text(
                text=globals.TEXT_LANG_WARNING
            )

    elif state == 4:
        update.message.reply_text(
            text=f"Fikr va takliflaringiz uchun rahmat!"
        )
        comment = update.message.text
        db.create_comment(user.id, user.username, comment)
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"<i>{user.username}:</i>\n{comment}",
            parse_mode='HTML'
        )
        context.user_data["state"] = globals.STATES["reg"]
        check(update, context)

    elif state[0] == "admin":
        msg = update.message.text
        user = update.message.from_user.username
        context.bot.send_message(
            chat_id=state[1],
            text=msg
        )
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Xabar {user}ga jo'natildi",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(callback_data=f'admin_{state[1]}', text="✉ Yangi xabar jo'natish"),
                 InlineKeyboardButton(callback_data='mainmenu', text="🏠 Asosiy menyu")],

            ])

        )


def inline_handler(update, context):
    query = update.callback_query
    data_sp = str(query.data).split("_")
    print(f"-----  (data_sp)  ----------{data_sp}  -----------------")
    db_user = db.get_user_by_chat_id(query.message.chat_id)
    lang_code = db_user['lang_id']

    if data_sp[0] == "category":
        if data_sp[1] == "product":
            if data_sp[2] == "back":
                query.message.delete()
                products = db.get_products_by_category(category_id=int(data_sp[3]))
                buttons = methods.send_product_buttons(products=products, lang_id=db_user["lang_id"])

                clicked_btn = db.get_category_parent(int(data_sp[3]))

                if clicked_btn and clicked_btn['parent_id']:
                    buttons.append([InlineKeyboardButton(
                        text=globals.BACK[db_user["lang_id"]], callback_data=f"category_back_{clicked_btn['parent_id']}"
                    )])
                # else:
                #     buttons.append([InlineKeyboardButton(
                #         text=globals.BACK[db_user["lang_id"]], callback_data=f"category_back"
                #     )])
                query.message.reply_text(
                    text=globals.TEXT_ORDER[db_user['lang_id']],
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=buttons,
                    )
                )

            else:
                if len(data_sp) == 4:
                    query.message.delete()
                    carts = context.user_data.get("carts", {})
                    carts[f"{data_sp[2]}"] = carts.get(f"{data_sp[2]}", 0) + int(data_sp[3])
                    context.user_data["carts"] = carts

                    categories = db.get_categories_by_parent()
                    buttons = methods.send_category_buttons(categories=categories, lang_id=db_user["lang_id"])

                    query.message.reply_text(
                        text="PAGE 404 NOT FOUND",
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=buttons,
                        )
                    )

                else:
                    product = db.get_product_by_id(int(data_sp[2]))
                    query.message.delete()

                    caption = product[f"description_{globals.LANGUAGE_CODE[lang_code]}"]

                    buttons = [
                        [
                            InlineKeyboardButton(
                                text=globals.BACK[lang_code],
                                callback_data=f"category_product_back_{product['category_id']}"
                            )
                        ]
                    ]

                    try:
                        ########## dynamic_path #########################################################
                        path1 = settings.MEDIA_ROOT
                        newPath = path1.replace(os.sep, '/')
                        query.message.reply_photo(
                            photo=open(f'{newPath}/{product["image"]}', "rb"),
                            caption=caption,
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
                        )

                    except:
                        query.message.reply_text(
                            text=caption,
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
                        )
        ###################################################################
        elif data_sp[1] == "back":
            if len(data_sp) == 3:
                parent_id = int(data_sp[2])
            else:
                parent_id = None

            categories = db.get_categories_by_parent(parent_id=parent_id)
            buttons = methods.send_category_buttons(categories=categories, lang_id=db_user["lang_id"])

            if parent_id:
                clicked_btn = db.get_category_parent(parent_id)

                if clicked_btn and clicked_btn['parent_id']:
                    buttons.append([InlineKeyboardButton(
                        text=globals.BACK[db_user["lang_id"]], callback_data=f"category_back_{clicked_btn['parent_id']}"
                    )])
                # else:
                #     buttons.append([InlineKeyboardButton(
                #         text=globals.BACK[db_user["lang_id"]], callback_data=f"category_back"
                #     )])

            query.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=buttons
                )
            )
        else:
            categories = db.get_categories_by_parent(parent_id=int(data_sp[1]))
            if categories:
                buttons = methods.send_category_buttons(categories=categories, lang_id=db_user["lang_id"])
            else:
                products = db.get_products_by_category(category_id=int(data_sp[1]))
                buttons = methods.send_product_buttons(products=products, lang_id=db_user["lang_id"])

            clicked_btn = db.get_category_parent(int(data_sp[1]))

            if clicked_btn and clicked_btn['parent_id']:
                buttons.append([InlineKeyboardButton(
                    text=globals.BACK[db_user["lang_id"]], callback_data=f"category_back_{clicked_btn['parent_id']}"
                )])
            # else:
            #     buttons.append([InlineKeyboardButton(
            #         text=globals.BACK[db_user["lang_id"]], callback_data=f"category_back"
            #     )])

            query.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=buttons
                )
            )

    elif data_sp[0] == "admin":
        query.message.reply_text(text="Xabar matnini kiriting:", reply_markup=ReplyKeyboardRemove())

        context.user_data["state"] = data_sp

    elif data_sp[0] == "mainmenu":

        methods.send_main_menu(context, query.message.chat.id, db_user['lang_id'])
        context.user_data["state"] = globals.STATES["menu"]


def contact_handler(update, context):
    db_user = db.get_user_by_chat_id(update.message.from_user.id)
    contact = update.message.contact.phone_number
    db.update_user_data(update.message.from_user.id, "phone_number", contact)
    check(update, context)


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        # 1 -- правильное подключение
        request = Request(
            connect_timeout=1.0,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TGTOKEN,
            base_url=getattr(settings, 'PROXY_URL', None),
        )
        print(bot.get_me())

        # 2 -- обработчики
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', start_handler))
        dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
        dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
        dispatcher.add_handler(CallbackQueryHandler(inline_handler))

        # 3 -- запустить бесконечную обработку входящих сообщений
        updater.start_polling()
        updater.idle()
