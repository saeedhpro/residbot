import os
import random
from random import randint

from dotenv import load_dotenv
import re

from jinja2 import Environment, FileSystemLoader
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, \
    filters, ContextTypes
import logging
from html2image import Html2Image

(START, RETURN_MENU, SELECT_ACTION, SELECT_BANK, GET_STATUS, GET_TRANSACTION_TYPE, GET_SOURCE_ACCOUNT, GET_DEST_IBAN,
 GET_DEST_NAME, GET_DATETIME, GET_AMOUNT, GET_SENDER_NAME, GET_DEST_ACCOUNT, GET_DEST_BANK, GET_REASON, GET_DESCRIPTION,
 GET_TRACKING_CODE, GET_MARJA, GET_DATE, GET_TIME, GET_RECEIVER_FNAME, GET_RECEIVER_LNAME, GET_SOURCE_IBAN,
 GET_MANDE, GET_DESCRIPTION2, GET_REDUCE_SOURCE_ACCOUNT, GET_DESCRIPTION3, GET_SIGNER, GET_DAY_NAME) = range(29)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("ایجاد رسید", callback_data='create_receipt')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('لطفاً گزینه‌ ی ساخت رسید را انتخاب کنید:', reply_markup=reply_markup)
    return SELECT_ACTION


async def handle_select_action(update, context):
    query = update.callback_query
    await query.answer()
    return await select_bank_type(update, context)


async def select_bank_type(update, context):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("بانک تجارت ساتنا (اصغر راه روکجابادی)", callback_data='tejarat')],
        [InlineKeyboardButton("بانک تجارت پایا (رضا کلهر)", callback_data='tejarat_paya')],
        [InlineKeyboardButton("بانک تجارت کارت به کارت (امیرحسن صفری)", callback_data='tejarat_card')],
        [InlineKeyboardButton("بانک سینا پایا (محمد عبدی)", callback_data='sina_paya')],
        [InlineKeyboardButton("بانک شهر پایا عادی (محمدحسن غفاری)", callback_data='shahr')],
        [InlineKeyboardButton("بانک شهر ساتنا (امید سالم دوست)", callback_data='shahr_satna')],
        [InlineKeyboardButton("بانک شهر پایا (مهدی یوسفی)", callback_data='shahr_paya')],
        [InlineKeyboardButton("بانک شهر پایا 2 (ولی واقفی)", callback_data='shahr_paya_2')],
        [InlineKeyboardButton("بانک سپه ساتنا (محمد عبدی)", callback_data='sepah_satna')],
        [InlineKeyboardButton("بانک سپه پایا (محمدحسن غفاری)", callback_data='sepah_paya')],
        [InlineKeyboardButton("بانک سامان تیره (عرفان ارجمندی فرد)", callback_data='saman_paya_dark')],
        [InlineKeyboardButton("بانک سامان روشن (امیرحسین صفری)", callback_data='saman_paya_light')],
        [InlineKeyboardButton("بانک صادرات عادی (عاطفه جعفرزاده تفتی)", callback_data='saderat')],
        [InlineKeyboardButton("بانک صادرات پایا (ژیلا اسکندری)", callback_data='saderat_paya')],
        [InlineKeyboardButton("بانک صادرات پایا 2 (ولی واقفی)", callback_data='saderat_2')],
        [InlineKeyboardButton("بانک رسالت ساتنا (ولی واقفی)", callback_data='resalat_satna')],
        [InlineKeyboardButton("بانک دی (فرحان کاشانی اصل)", callback_data='day')],
        [InlineKeyboardButton("بانک دی ساتنا (مجید مرادی)", callback_data='day_satna')],
        [InlineKeyboardButton("بانک رفاه پایا 1 (رضا کلهر)", callback_data='refah')],
        [InlineKeyboardButton("بانک رفاه پایا 2 (شاکر... دادگر...)", callback_data='refah_2')],
        [InlineKeyboardButton("بانک رفاه پایا 3 (ولی واقفی)", callback_data='refah_paya')],
        [InlineKeyboardButton("بانک رفاه ساتنا (حمیدرضا گودرزی)", callback_data='refah_satna')],
        [InlineKeyboardButton("بانک اقتصاد (محمدصادقی بهرمی بسحاق)", callback_data='eghtesad')],
        [InlineKeyboardButton("بانک مهر (ولی واقفی)", callback_data='mehr')],
        [InlineKeyboardButton("بانک مهر 2 (امیرحسین صفری)", callback_data='mehr_2')],
        [InlineKeyboardButton("بانک مهر 3 (حامد نشاطی)", callback_data='mehr_3')],
        [InlineKeyboardButton("بانک مهر 4 (فاطمه قلی زاده)", callback_data='mehr_4')],
        [InlineKeyboardButton("بانک مهر تاریک (فرحان کاشانی اصل)", callback_data='mehr_dark')],
        [InlineKeyboardButton("بانک مهر تاریک 2 (غلامرضا کوتی)", callback_data='mehr_dark_2')],
        [InlineKeyboardButton("بانک مهر روشن (ولی واقفی)", callback_data='mehr_light')],
        [InlineKeyboardButton("بانک کشاورزی (سید احمد طبیب زاده)", callback_data='keshavarzi')],
        [InlineKeyboardButton("بانک پارسیان (حامد نشاطی)", callback_data='parsian')],
        [InlineKeyboardButton("بانک پاسارگاد پایا (حمیدرضا یوسفی)", callback_data='pasargad_paya')],
        [InlineKeyboardButton("بانک پاسارگاد پایا 2 (امجد المنیهلاوی)", callback_data='pasargad_paya_2')],
        [InlineKeyboardButton("بانک پاسارگاد ساتنا (رضا کلهر)", callback_data='pasargad_satna')],
        [InlineKeyboardButton("بانک پاسارگاد شبا (حمیدرضا حمید یوسفی معبودی نژاد)", callback_data='pasargad_shaba')],
        [InlineKeyboardButton("بانک پست بانک پایا (حسین کریم پور)", callback_data='post_bank_paya')],
        [InlineKeyboardButton("بانک پست بانک پایا 2 (نوید داداش زاده)", callback_data='post_bank_paya_2')],
        [InlineKeyboardButton("بانک آینده (سید جابر بخات پور)", callback_data='ayandeh')],
        [InlineKeyboardButton("بانک آینده پایا (مجید مرادی)", callback_data='ayandeh_paya')],
        [InlineKeyboardButton("بانک مسکن ساتنا (مجید مرادی)", callback_data='maskan_satna')],
        [InlineKeyboardButton("بانک رسالت پایا (مهدی ابراهیمی)", callback_data='resalat_paya')],
        [InlineKeyboardButton("بانک رسالت ساتنا 2 (ولی واقفی)", callback_data='resalat_satna_2')],
        # [InlineKeyboardButton("بازگشت", callback_data='return_to_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("لطفاً یک بانک را انتخاب کنید:", reply_markup=reply_markup)
    return SELECT_BANK


async def handle_select_bank(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'return_to_menu':
        return RETURN_MENU

    context.user_data['bank_type'] = query.data

    if context.user_data['bank_type'] == 'ayandeh_paya' \
            or context.user_data['bank_type'] == 'post_bank_paya_2' \
            or context.user_data['bank_type'] == 'refah_2' \
            or context.user_data['bank_type'] == 'refah_paya' \
            or context.user_data['bank_type'] == 'refah_satna' \
            or context.user_data['bank_type'] == 'saderat_paya' \
            or context.user_data['bank_type'] == 'shahr' \
            or context.user_data['bank_type'] == 'shahr_paya' \
            or context.user_data['bank_type'] == 'sina_paya' \
            or context.user_data['bank_type'] == 'saderat_2' \
            or context.user_data['bank_type'] == 'saderat' \
            or context.user_data['bank_type'] == 'mehr_2' \
            or context.user_data['bank_type'] == 'mehr_3' \
            or context.user_data['bank_type'] == 'mehr_dark_2' \
            or context.user_data['bank_type'] == 'pasargad_shaba' \
            or context.user_data['bank_type'] == 'tejarat':
        await query.edit_message_text('تاریخ را وارد کنید')
        return GET_DATE

    await query.edit_message_text('تاریخ و ساعت را وارد کنید')
    return GET_DATETIME


async def handle_get_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['datetime'] = update.message.text

    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('مبلغ انتقال را به ریال وارد کنید ')
        return GET_AMOUNT

    if context.user_data['bank_type'] == 'resalat_satna':
        await update.message.reply_text('مبلغ انتقال را به ریال وارد کنید ')
        return GET_AMOUNT

    if context.user_data['bank_type'] == 'resalat_satna_2':
        await update.message.reply_text('مبلغ انتقال را به ریال وارد کنید ')
        return GET_AMOUNT

    await update.message.reply_text('مبلغ را به ریال وارد کنید ')
    return GET_AMOUNT


async def handle_get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['date'] = update.message.text

    await update.message.reply_text('ساعت را وارد کنید')
    return GET_TIME


async def handle_get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['time'] = update.message.text
    if context.user_data['bank_type'] == 'mehr_2' or \
            context.user_data['bank_type'] == 'mehr_3':
        await update.message.reply_text('نام روز هفته (شنبه و یکشنبه و ...) را وارد کنید:')
        return GET_DAY_NAME
    if context.user_data['bank_type'] == 'pasargad_shaba':
        await update.message.reply_text('مبلغ تراکنش را به ریال وارد کنید ')
        return GET_AMOUNT
    await update.message.reply_text('مبلغ را به ریال وارد کنید ')
    return GET_AMOUNT


async def handle_get_day_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['day_name'] = update.message.text

    await update.message.reply_text('مبلغ را به ریال وارد کنید ')
    return GET_AMOUNT


async def handle_get_amount(update: Update, context):
    context.user_data['amount'] = update.message.text

    if context.user_data['bank_type'] == 'pasargad_shaba':
        await update.message.reply_text('شبای مقصد را بدون IR وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr':
        await update.message.reply_text('مانده را وارد کنید:')
        return GET_MANDE

    if context.user_data['bank_type'] == 'mehr_3':
        await update.message.reply_text('مانده را وارد کنید:')
        return GET_MANDE

    if context.user_data['bank_type'] == 'mehr_dark_2':
        await update.message.reply_text('مانده را وارد کنید:')
        return GET_MANDE

    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('سپرده مبدا را وارد کنید:')
        return GET_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('سپرده مبدا را وارد کنید:')
        return GET_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('شماره سپرده مبدا را وارد کنید:')
        return GET_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('شماره سپرده مبدا را وارد کنید:')
        return GET_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('سپرده مبدا را وارد کنید:')
        return GET_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'shahr':
        await update.message.reply_text('شماره سپرده را وارد کنید:')
        return GET_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'saman_paya_dark':
        await update.message.reply_text('سپرده مبدا را وارد کنید:')
        return GET_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'saman_paya_light':
        await update.message.reply_text('سپرده مبدا را وارد کنید:')
        return GET_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'resalat_satna_2':
        await update.message.reply_text('شماره سپرده مبدا را وارد کنید:')
        return GET_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'maskan_satna':
        await update.message.reply_text('شماره حساب را وارد کنید:')
        return GET_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'shahr_satna' \
            or context.user_data['bank_type'] == 'shahr_paya' \
            or context.user_data['bank_type'] == 'shahr_paya_2':
        await update.message.reply_text('سپرده مبدا را وارد کنید:')
        return GET_SOURCE_ACCOUNT

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_get_mande(update: Update, context):
    context.user_data['mande'] = update.message.text

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_source_account(update: Update, context):
    context.user_data['source_account'] = update.message.text

    if context.user_data['bank_type'] == 'tejarat_paya':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'tejarat_card':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'tejarat':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'saman_paya_light':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'saman_paya_dark':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'ayandeh':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'ayandeh_paya':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'eghtesad':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'keshavarzi':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'maskan_satna':
        await update.message.reply_text('شماره شبا مبدا را وارد کنید:')
        return GET_SOURCE_IBAN

    if context.user_data['bank_type'] == 'mehr':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr_2':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr_3':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr_4':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr_dark':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr_dark_2':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr_light':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'parsian':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'post_bank_paya':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'post_bank_paya_2':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'refah':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'refah_paya':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'refah_satna':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'resalat_satna':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'resalat_satna_2':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'saderat_paya':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'saderat':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'day':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'day_satna':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'saderat_2':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'shahr':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'shahr_paya':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'shahr_paya_2':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'shahr_satna':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'sina_paya':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_get_dest_iban(update: Update, context):
    iban = update.message.text
    iban = iban.upper()
    # pattern = r'^IR\d{24}$'
    # if not re.match(pattern, iban):
    #     await update.message.reply_text('شبای وارد شده صحیح نمی باشد. لطفا شماره شبای صحیح را وارد کنید:')
    #     return GET_DEST_IBAN

    context.user_data['iban'] = iban

    if context.user_data['bank_type'] == 'tejarat':
        await update.message.reply_text('نام صاحب شبا را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'tejarat_card':
        await update.message.reply_text('نام صاحب شبا را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'pasargad_shaba':
        await update.message.reply_text('به نام (نام دریافت کننده) را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'tejarat_paya':
        await update.message.reply_text('نام صاحب شبا را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('نام صاحب شبا را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('گیرنده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'saman_paya_light':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'saman_paya_dark':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'ayandeh':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'ayandeh_paya':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'eghtesad':
        await update.message.reply_text('نام صاحب سپرده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'keshavarzi':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'mehr':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'mehr_2':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'mehr_3':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'mehr_4':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'mehr_dark':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'mehr_dark_2':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'mehr_light':
        await update.message.reply_text('دارنده مقصد را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'parsian':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME

    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('نام گیرنده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('نام گیرنده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('نام صاحب شبا را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'post_bank_paya':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'post_bank_paya_2':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'refah':
        await update.message.reply_text('گیرنده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('مشتری مقصد را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'refah_paya':
        await update.message.reply_text('نام دارنده شبا را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'refah_satna':
        await update.message.reply_text('نام دارنده شماره شبا را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'resalat_satna':
        await update.message.reply_text('نام صاحب شبا را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'resalat_satna_2':
        await update.message.reply_text('گیرنده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'saderat':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'saderat_paya':
        await update.message.reply_text('نام صاحب حساب مقصد را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'day':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'day_satna':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'saderat_2':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'shahr':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'shahr_paya':
        await update.message.reply_text('نام گیرنده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'shahr_paya_2':
        await update.message.reply_text('نام گیرنده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'shahr_satna':
        await update.message.reply_text('نام دارنده شماره شبا را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'sina_paya':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME

    if context.user_data['bank_type'] == 'maskan_satna':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_RECEIVER_FNAME

    await update.message.reply_text('نام صاحب شبا را وارد کنید:')
    return GET_DEST_NAME


async def handle_get_receiver_fname(update: Update, context):
    context.user_data['receiver_fname'] = update.message.text

    await update.message.reply_text('نام خانوادگی دریافت کننده را وارد کنید:')
    return GET_RECEIVER_LNAME


async def handle_get_receiver_lname(update: Update, context):
    context.user_data['receiver_lname'] = update.message.text

    if context.user_data['bank_type'] == 'maskan_satna':
        await update.message.reply_text('بابت را وارد کنید:')
        return GET_DESCRIPTION

    await update.message.reply_text('شماره شبا مبدا را وارد کنید:')
    return GET_SOURCE_IBAN


async def handle_get_source_iban(update: Update, context):
    iban = update.message.text
    context.user_data['source_iban'] = iban.upper()

    if context.user_data['bank_type'] == 'shahr':
        await update.message.reply_text('نام واریز کننده را وارد کنید:')
        return GET_SENDER_NAME

    if context.user_data['bank_type'] == 'shahr_satna':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'maskan_satna':
        await update.message.reply_text('شماره شبا مقصد را وارد کنید:')
        return GET_DEST_IBAN

    await update.message.reply_text('توضیحات را وارد کنید:')
    return GET_DESCRIPTION


async def handle_get_dest_name(update: Update, context):
    context.user_data['receiver'] = update.message.text
    if context.user_data['bank_type'] == 'pasargad_shaba':
        await update.message.reply_text('نام بانک مقصد را وارد کنید(مانند: بانک صادرات):')
        return GET_DEST_BANK
    if context.user_data['bank_type'] == 'tejarat_card':
        await update.message.reply_text('شماره پیگیری را وارد کنید:')
        return GET_TRACKING_CODE
    if context.user_data['bank_type'] == 'tejarat_paya':
        await update.message.reply_text('شماره پیگیری را وارد کنید:')
        return GET_TRACKING_CODE

    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('کسر کارمزد از سپرده را وارد کنید:')
        return GET_DEST_ACCOUNT
    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('کسر کارمزد از سپرده را وارد کنید:')
        return GET_DEST_ACCOUNT
    if context.user_data['bank_type'] == 'saman_paya_light':
        await update.message.reply_text('نام انتقال دهنده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'saman_paya_dark':
        await update.message.reply_text('نام انتقال دهنده را وارد کنید:')
        return GET_SENDER_NAME

    if context.user_data['bank_type'] == 'ayandeh':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'eghtesad':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'day':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'day_satna':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME

    if context.user_data['bank_type'] == 'ayandeh_paya':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'keshavarzi':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'shahr_satna':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'mehr':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE
    if context.user_data['bank_type'] == 'mehr_2':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE
    if context.user_data['bank_type'] == 'mehr_3':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE
    if context.user_data['bank_type'] == 'mehr_dark':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'mehr_light':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE

    if context.user_data['bank_type'] == 'mehr_dark_2':
        await update.message.reply_text('توضیحات خط اول را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'mehr_4':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'parsian':
        await update.message.reply_text('توضیحات را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('نام فرستنده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('نام فرستنده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK
    if context.user_data['bank_type'] == 'post_bank_paya':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    # if context.user_data['bank_type'] == 'post_bank_paya_2':
    #     await update.message.reply_text('نام ارسال کننده را وارد کنید:')
    #     return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'post_bank_paya_2':
        await update.message.reply_text('بابت انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'refah_satna':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'refah':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'shahr':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'shahr_paya':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'shahr_paya_2':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('نام صاحب کارت/حساب را وارد کنید:')
        return GET_SENDER_NAME

    if context.user_data['bank_type'] == 'refah_paya':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'resalat_satna':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'resalat_satna_2':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'saderat':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'saderat_paya':
        await update.message.reply_text('بابت (علت) واریز را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'saderat_2':
        await update.message.reply_text('بابت (علت) واریز را وارد کنید:')
        return GET_DESCRIPTION2

    if context.user_data['bank_type'] == 'sina_paya':
        await update.message.reply_text('بابت (علت) واریز را وارد کنید:')
        return GET_DESCRIPTION2

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_get_sender_name(update: Update, context):
    context.user_data['sender'] = update.message.text
    if context.user_data['bank_type'] == 'tejarat' \
            or context.user_data['bank_type'] == 'mehr_4' \
            or context.user_data['bank_type'] == 'post_bank_paya' \
            or context.user_data['bank_type'] == 'day' \
            or context.user_data['bank_type'] == 'day_satna' \
            or context.user_data['bank_type'] == 'eghtesad':
        await update.message.reply_text('شماره پیگیری را وارد کنید:')
        return GET_TRACKING_CODE

    if context.user_data['bank_type'] == 'saman_paya_light' \
            or context.user_data['bank_type'] == 'saman_paya_dark':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'refah_satna':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'parisan':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME

    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'ayandeh':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'resalat_satna_2':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'parsian':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'shahr':
        await update.message.reply_text('بابت (علت) را وارد کنید:')
        return GET_DESCRIPTION2

    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('بابت (علت) را وارد کنید:')
        return GET_DESCRIPTION2

    if context.user_data['bank_type'] == 'post_bank_paya_2':
        await update.message.reply_text('علت انتقال وجه را وارد کنید:')
        return GET_DESCRIPTION2

    if context.user_data['bank_type'] == 'saderat':
        await update.message.reply_text('بابت (علت) را وارد کنید:')
        return GET_DESCRIPTION2

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_dest_account(update: Update, context):
    context.user_data['receiver_account'] = update.message.text
    if context.user_data['bank_type'] == 'sepah_satna' \
            or context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    await update.message.reply_text('نام انتقال دهنده را وارد کنید:')
    return GET_SENDER_NAME


async def handle_get_description(update: Update, context):
    context.user_data['description'] = update.message.text
    if context.user_data['bank_type'] == 'pasargad_shaba':
        await update.message.reply_text('شرح انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('فرستنده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('علت (بابت) انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'mehr_dark_2':
        await update.message.reply_text('توضیحات خط دوم را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('بابت انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('بابت انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('بابت انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('علت (بابت) انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'resalat_satna':
        await update.message.reply_text('علت (بابت) انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'resalat_satna_2':
        await update.message.reply_text('علت (بابت) انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'shahr_paya':
        await update.message.reply_text('علت (بابت) انتقال را وارد کنید:')
        return GET_DESCRIPTION2

    if context.user_data['bank_type'] == 'saderat_paya':
        await update.message.reply_text('نوع تراکنش را وارد کنید:')
        return GET_DESCRIPTION2

    if context.user_data['bank_type'] == 'saderat':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END

    if context.user_data['bank_type'] == 'ayandeh_paya':
        await update.message.reply_text('امضا کنندگان را وارد کنید:')
        return GET_SIGNER

    if context.user_data['bank_type'] == 'keshavarzi':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE

    if context.user_data['bank_type'] == 'maskan_satna':
        await update.message.reply_text('کد رهگیری را وارد کنید:')
        return GET_TRACKING_CODE

    await update.message.reply_text('شماره پیگیری را وارد کنید:')
    return GET_TRACKING_CODE


async def handle_get_description2(update: Update, context):
    context.user_data['description2'] = update.message.text
    if context.user_data['bank_type'] == 'pasargad_shaba':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('شرح را وارد کنید')
        return GET_DESCRIPTION3
    if context.user_data['bank_type'] == 'saderat_paya':
        await update.message.reply_text('نوع حساب مبدا را وارد کنید')
        return GET_DESCRIPTION3
    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('شناسه واریز/شماره قبض را وارد کنید')
        return GET_MARJA
    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('شرح مبدا را وارد کنید')
        return GET_DESCRIPTION3
    if context.user_data['bank_type'] == 'mehr_dark_2':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    await update.message.reply_text('شماره پیگیری را وارد کنید:')
    return GET_TRACKING_CODE


async def handle_get_description3(update: Update, context):
    context.user_data['description3'] = update.message.text
    if context.user_data['bank_type'] == 'saderat_paya':
        await update.message.reply_text('شماره پیگیری را وارد کنید')
        return GET_TRACKING_CODE
    await update.message.reply_text('کد پیگیری را وارد کنید:')
    return GET_TRACKING_CODE


async def handle_get_signer(update: Update, context):
    context.user_data['signer'] = update.message.text
    await update.message.reply_text('شماره پیگیری را وارد کنید:')
    return GET_TRACKING_CODE


async def handle_get_reason(update: Update, context):
    context.user_data['reason'] = update.message.text
    await update.message.reply_text('توضیحات را وارد کنید:')
    return GET_DESCRIPTION


async def handle_dest_bank(update: Update, context):
    context.user_data['receiver_bank'] = update.message.text

    if context.user_data['bank_type'] == 'pasargad_shaba':
        await update.message.reply_text('نوع تراکنش را وارد کنید(مانند: برداشت وجه):')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'shahr_paya':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'shahr_paya_2':
        await update.message.reply_text('علت (بابت) را وارد کنید:')
        return GET_DESCRIPTION2

    if context.user_data['bank_type'] == 'refah_paya':
        await update.message.reply_text('علت (بابت) را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('کسر کارمزد از سپرده را وارد کنید:')
        return GET_REDUCE_SOURCE_ACCOUNT
    if context.user_data['bank_type'] == 'resalat_satna':
        await update.message.reply_text('کسر کارمزد از سپرده را وارد کنید:')
        return GET_REDUCE_SOURCE_ACCOUNT
    if context.user_data['bank_type'] == 'resalat_satna_2':
        await update.message.reply_text('کسر کارمزد از سپرده را وارد کنید:')
        return GET_REDUCE_SOURCE_ACCOUNT
    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('کسر کارمز از سپرده را وارد کنید:')
        return GET_REDUCE_SOURCE_ACCOUNT
    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('کسر کارمزد از سپرده را وارد کنید:')
        return GET_REDUCE_SOURCE_ACCOUNT
    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('کسر کارمزد از سپرده را وارد کنید:')
        return GET_REDUCE_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'refah':
        await update.message.reply_text('علت (بابت) انتقال را وارد کنید:')
        return GET_DESCRIPTION2

    if context.user_data['bank_type'] == 'saderat':
        await update.message.reply_text('نام صاحب حساب مبدا را وارد کنید:')
        return GET_SENDER_NAME

    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE

    if context.user_data['bank_type'] == 'refah_2' \
            or context.user_data['bank_type'] == 'saman_paya_light' \
            or context.user_data['bank_type'] == 'saman_paya_dark':
        await update.message.reply_text('شماره پیگیری را وارد کنید:')
        return GET_TRACKING_CODE
    if context.user_data['bank_type'] == 'refah_satna':
        await update.message.reply_text('شناسه پرداخت را وارد کنید:')
        return GET_TRACKING_CODE
    if context.user_data['bank_type'] == 'shahr':
        await update.message.reply_text('شماره شبا مبدا را وارد کنید:')
        return GET_SOURCE_IBAN

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_get_reduce_source_account(update: Update, context):
    context.user_data['reduce_source_account'] = update.message.text
    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('نام فرستنده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'resalat_satna':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'resalat_satna_2':
        await update.message.reply_text('نام فرستنده را وارد کنید:')
        return GET_SENDER_NAME
    await update.message.reply_text('شرح مبدا را وارد کنید:')
    return GET_DESCRIPTION


async def handle_tracking_code(update: Update, context):
    context.user_data['tracking_code'] = update.message.text
    if context.user_data['bank_type'] == 'ayandeh':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'keshavarzi':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'mehr':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'mehr_2':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'mehr_3':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'mehr_4':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'mehr_light':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'parsian':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'post_bank_paya_2':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'refah':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'refah_paya':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'refah_satna':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'day':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'day_satna':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'saderat_2':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'shahr':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'shahr_paya':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'shahr_paya_2':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'shahr_satna':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'sina_paya':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'sepah_satna':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'saderat':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'pasargad_paya':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END

    if context.user_data['bank_type'] == 'ayandeh_paya':
        await update.message.reply_text('شماره دستور پرداخت را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('شناسه واریز را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('شناسه واریز/شماره قبض را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'post_bank_paya':
        await update.message.reply_text('شناسه واریز را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('شماره درخواست را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('شناسه واریز/شماره قبض را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'resalat_satna':
        await update.message.reply_text('شناسه واریز/شماره قبض را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'resalat_satna_2':
        await update.message.reply_text('شناسه واریز را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('شناسه واریز را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'saderat_paya':
        await update.message.reply_text('شناسه پرداخت را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'saman_paya_light':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'saman_paya_dark':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'eghtesad':
        await update.message.reply_text('شماره مرجع تراکنش را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'maskan_satna':
        await update.message.reply_text('شناسه مرجع را وارد کنید:')
        return GET_MARJA
    await update.message.reply_text('شماره مرجع را وارد کنید:')
    return GET_MARJA


async def handle_get_marja(update: Update, context):
    context.user_data['marja'] = update.message.text
    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('شماره پیگیری را وارد کنید:')
        return GET_TRACKING_CODE
    await create_receipt_and_send_resid(update, context)
    return ConversationHandler.END


async def create_receipt_and_send_resid(update, context):
    await create_and_send_receipt(update, context)


async def create_and_send_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    env = Environment(loader=FileSystemLoader('.'))
    template_name = 'templates/' + context.user_data['bank_type'] + '/index.html'
    template = env.get_template(template_name)
    bank_type = context.user_data['bank_type']

    html_content = {}

    current_directory = os.getcwd()

    if bank_type == 'pasargad_shaba':
        amount = context.user_data['amount']
        amount_toman = int(int(amount) / 10)
        html_content = {
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'amount': format_amount(convert_numbers_to_farsi(amount)),
            'amount_toman': format_amount(convert_numbers_to_farsi(str(amount_toman))),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'current_directory': current_directory,
            'tracking_code': convert_numbers_to_farsi(str(random.randint(10000000000000, 100000000000000000000))),
            'bank_icon': get_bank_icon(context.user_data['iban'], 'pasargad_shaba'),
        }

    if bank_type == 'tejarat':
        html_content = {
            'status': 'در حال انجام',
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'current_directory': current_directory,
        }

    if bank_type == 'tejarat_paya':
        html_content = {
            'status': 'در حال انجام',
            'bank_type_en': context.user_data['bank_type'],
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'current_directory': current_directory,
        }

    if bank_type == 'tejarat_card':
        html_content = {
            'status': 'در حال انجام',
            'bank_type_en': context.user_data['bank_type'],
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'current_directory': current_directory,
        }

    if bank_type == 'sina_paya':
        html_content = {
            'bank_type_en': context.user_data['bank_type'],
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'current_directory': current_directory,
        }

    if bank_type == 'shahr_satna':
        html_content = {
            'bank_type_en': context.user_data['bank_type'],
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'current_directory': current_directory,
        }

    if bank_type == 'shahr_paya':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'shahr_paya_2':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'shahr':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'source_iban': convert_numbers_to_farsi(context.user_data['source_iban']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
        }

    if bank_type == 'sepah_satna':
        amount = context.user_data['amount']
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'amount_fa': convert_numbers_to_farsi(convert_number_to_words(int(int(amount) / 10))),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_account': convert_numbers_to_farsi(context.user_data['receiver_account']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'ghabz': convert_numbers_to_farsi(context.user_data['marja']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'sepah_paya':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_account': convert_numbers_to_farsi(context.user_data['receiver_account']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'description3': convert_numbers_to_farsi(context.user_data['description3']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'current_directory': current_directory,
        }

    if bank_type == 'saman_paya_light':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
        }

    if bank_type == 'saman_paya_dark':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
        }

    if bank_type == 'saderat_paya':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': context.user_data['source_account'],
            'description3': context.user_data['description3'],
            'iban': context.user_data['iban'],
            'receiver': context.user_data['receiver'],
            'amount': format_amount(context.user_data['amount']),
            'description2': context.user_data['description2'],
            'marja': context.user_data['marja'],
            'description': context.user_data['description'],
            'tracking_code': context.user_data['tracking_code'],
            'date': context.user_data['date'],
            'time': context.user_data['time'],
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'saderat_2':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'current_directory': current_directory,
        }

    if bank_type == 'saderat':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'date': context.user_data['date'],
            'time': context.user_data['time'],
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban'], 'saderat'),
        }

    if bank_type == 'resalat_satna':
        amount = context.user_data['amount']
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'reduce_source_account': convert_numbers_to_farsi(context.user_data['reduce_source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'amount_fa': convert_numbers_to_farsi(convert_number_to_words(int(int(amount) / 10))),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'day':
        html_content = {
            'status': 'ثبت شد',
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'eghtesad':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'current_directory': current_directory,
        }

    if bank_type == 'refah_paya':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'refah':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
        }

    if bank_type == 'refah_2':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': context.user_data['source_account'],
            'iban': context.user_data['iban'],
            'sender': context.user_data['sender'],
            'receiver': context.user_data['receiver'],
            'receiver_bank': context.user_data['receiver_bank'],
            'amount': format_amount(context.user_data['amount']),
            'date': context.user_data['date'],
            'time': context.user_data['time'],
            'marja': context.user_data['marja'],
            'tracking_code': context.user_data['tracking_code'],
            'current_directory': current_directory,
        }

    if bank_type == 'refah_satna':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
        }

    if bank_type == 'mehr':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'mande': format_amount(convert_numbers_to_farsi(context.user_data['mande'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'mehr_2':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'day_name': convert_numbers_to_farsi(context.user_data['day_name']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'mehr_3':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'mande': format_amount(convert_numbers_to_farsi(context.user_data['mande'])),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'day_name': convert_numbers_to_farsi(context.user_data['day_name']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'mehr_4':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'mehr_dark':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'current_directory': current_directory,
        }

    if bank_type == 'mehr_dark_2':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'mande': format_amount(convert_numbers_to_farsi(context.user_data['mande'])),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'day_name': convert_numbers_to_farsi(context.user_data['day_name']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'mehr_light':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'day_satna':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'keshavarzi':
        html_content = {
            'bank_type_en': context.user_data['bank_type'],
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount']), '❜'),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'status': 'ارسال شده',
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
        }

    if bank_type == 'parsian':
        html_content = {
            'status': 'آماده انجام',
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'pasargad_paya':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'reduce_source_account': convert_numbers_to_farsi(context.user_data['reduce_source_account']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'current_directory': current_directory,
        }

    if bank_type == 'pasargad_paya_2':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'reduce_source_account': convert_numbers_to_farsi(context.user_data['reduce_source_account']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'description3': convert_numbers_to_farsi(context.user_data['description3']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'current_directory': current_directory,
        }

    if bank_type == 'pasargad_satna':
        amount = context.user_data['amount']
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'reduce_source_account': convert_numbers_to_farsi(context.user_data['reduce_source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'amount_fa': convert_numbers_to_farsi(convert_number_to_words(int(int(amount) / 10))),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'post_bank_paya':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'post_bank_paya_2':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            # 'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'ayandeh':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'ayandeh_paya':
        html_content = {
            'status': 'پایان یافته',
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'signer': convert_numbers_to_farsi(context.user_data['signer']),
            'signer_small': do_signer_small(context.user_data['signer']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'maskan_satna':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'source_iban': convert_numbers_to_farsi(context.user_data['source_iban']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'receiver_fname': convert_numbers_to_farsi(context.user_data['receiver_fname']),
            'receiver_lname': convert_numbers_to_farsi(context.user_data['receiver_lname']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'current_directory': current_directory,
        }

    if bank_type == 'resalat_paya':
        amount = context.user_data['amount']
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'reduce_source_account': convert_numbers_to_farsi(context.user_data['reduce_source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'amount_fa': convert_numbers_to_farsi(convert_number_to_words(int(int(amount) / 10))),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'current_directory': current_directory,
            'bank_icon': get_bank_icon(context.user_data['iban']),
        }

    if bank_type == 'resalat_satna_2':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'reduce_source_account': convert_numbers_to_farsi(context.user_data['reduce_source_account']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'current_directory': current_directory,
        }

    await update.message.reply_text('در حال ساخت رسید... لطفا صبر کنید!:')
    rendered_html = template.render(html_content)
    png_name = f"receipt_{context.user_data['tracking_code']}.png"
    png_path = f"./receipts/image/"
    options = {
        'format': 'png',
        'encoding': "UTF-8",
        'no-stop-slow-scripts': '',
        'enable-local-file-access': '',
    }
    if context.user_data['bank_type'] == 'tejarat':
        options['height'] = '1019'
        options['width'] = '677'
    elif context.user_data['bank_type'] == 'tejarat_card':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'tejarat_paya':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'sina_paya':
        options['height'] = '1280'
        options['width'] = '739'
    elif context.user_data['bank_type'] == 'shahr_satna':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'shahr_paya_2':
        options['height'] = '1336'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'sepah_satna':
        options['height'] = '1380'
        options['width'] = '752'
    elif context.user_data['bank_type'] == 'sepah_paya':
        options['height'] = '1588'
        options['width'] = '685'
    elif context.user_data['bank_type'] == 'saman_paya_light':
        options['height'] = '1380'
        options['width'] = '752'
    elif context.user_data['bank_type'] == 'saman_paya_dark':
        options['height'] = '1380'
        options['width'] = '752'
    elif context.user_data['bank_type'] == 'saderat_paya':
        options['height'] = '1380'
        options['width'] = '747'
    elif context.user_data['bank_type'] == 'saderat_2':
        options['height'] = '1380'
        options['width'] = '635'
    elif context.user_data['bank_type'] == 'saderat':
        options['height'] = '1380'
        options['width'] = '744'
    elif context.user_data['bank_type'] == 'ayandeh':
        options['height'] = '1380'
        options['width'] = '654'
    elif context.user_data['bank_type'] == 'ayandeh_paya':
        options['height'] = '1380'
        options['width'] = '966'
    elif context.user_data['bank_type'] == 'eghtesad':
        options['height'] = '1380'
        options['width'] = '637'
    elif context.user_data['bank_type'] == 'keshavarzi':
        options['height'] = '1280'
        options['width'] = '665'
    elif context.user_data['bank_type'] == 'maskan_satna':
        options['height'] = '1280'
        options['width'] = '668'
    elif context.user_data['bank_type'] == 'mehr':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'mehr_2':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'mehr_3':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'mehr_4':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'mehr_dark':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'mehr_dark_2':
        options['height'] = '1380'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'mehr_light':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'parsian':
        options['height'] = '1378'
        options['width'] = '687'
    elif context.user_data['bank_type'] == 'pasargad_paya':
        options['height'] = '1380'
        options['width'] = '615'
    elif context.user_data['bank_type'] == 'pasargad_paya_2':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'pasargad_satna':
        options['height'] = '1280'
        options['width'] = '623'
    elif context.user_data['bank_type'] == 'pasargad_shaba':
        options['height'] = '1380'
        options['width'] = '614'
    elif context.user_data['bank_type'] == 'post_bank_paya':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'post_bank_paya_2':
        options['height'] = '1380'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'refah':
        options['height'] = '1378'
        options['width'] = '630'
    elif context.user_data['bank_type'] == 'refah_2':
        options['height'] = '1382'
        options['width'] = '656'
    elif context.user_data['bank_type'] == 'refah_paya':
        options['height'] = '1380'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'refah_satna':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'resalat_paya':
        options['height'] = '1380'
        options['width'] = '623'
    elif context.user_data['bank_type'] == 'resalat_satna':
        options['height'] = '1280'
        options['width'] = '667'
    elif context.user_data['bank_type'] == 'resalat_satna_2':
        options['height'] = '1380'
        options['width'] = '612'
    elif context.user_data['bank_type'] == 'day':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'day_satna':
        options['height'] = '1280'
        options['width'] = '996'
    elif context.user_data['bank_type'] == 'shahr':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'shahr_paya':
        options['height'] = '1320'
        options['width'] = '623'
    hti = Html2Image(output_path=png_path)
    hti.screenshot(
        html_str=rendered_html,
        css_str='',
        save_as=png_name,
        size=(int(options['width']), int(options['height']))
    )

    with open("f.html", "+w") as f:
        f.writelines(rendered_html)
    f.close()

    # imgkit.from_string(rendered_html, png_path, options=options)
    photo = f"{png_path}{png_name}"
    await update.message.reply_photo(photo=open(photo, 'rb'))

    return RETURN_MENU


async def handle_return_menu(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("ایجاد رسید", callback_data='create_receipt')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('لطفاً یکی از گزینه‌های زیر را انتخاب کنید:', reply_markup=reply_markup)
    return SELECT_ACTION


def get_bank_type_in_farsi(bank_type='tejarat'):
    bank_type_list = {
        'saman_paya_dark': 'بانک سامان تیره',
        'saman_paya_light': 'بانک سامان روشن',
        'sepah_paya': 'بانک سپه پایا',
        'sepah_satna': 'بانک سپه ساتنا',
        'tejarat': 'بانک تجارت',
        'tejarat_card': 'بانک تجارت کارت به کارت',
        'tejarat_paya': 'بانک تجارت پایا',
        'ayandeh': 'آینده',
        'ayandeh_paya': 'بانک آینده پایا',
        'eghtesad': 'بانک اقتصاد',
        'keshavarzi': 'بانک کشاورزی',
        'mehr': 'بانک مهر',
        'mehr_2': 'بانک مهر 2',
        'mehr_3': 'بانک مهر 3',
        'mehr_4': 'بانک مهر 4',
        'mehr_dark': 'بانک مهر تاریک',
        'mehr_dark_2': 'بانک مهر تاریک 2',
        'mehr_light': 'بانک مهر روشن',
        'mellat': 'بانک ملت',
        'maskan_satna': 'بانک مسکن ساتنا',
        'parsian': 'بانک پارسیان',
        'pasargad_paya': 'بانک پاسارگاد پایا',
        'pasargad_paya_2': 'بانک پاسارگاد پایا 2',
        'pasargad_satna': 'بانک پاسارگاد ساتنا',
        'pasargad_shaba': 'بانک پاسارگاد شبا',
        'post_bank_paya': 'بانک پست بانک پایا',
        'post_bank_paya_2': 'بانک پست بانک پایا 2',
        'refah': 'بانک رفاه',
        'refah_2': 'بانک رفاه 2',
        'refah_paya': 'بانک رفاه پایا',
        'refah_satna': 'بانک رفاه ساتنا',
        'resalat_paya': 'بانک رسالت پایا',
        'resalat_satna': 'بانک رسالت ساتنا',
        'resalat_satna_2': 'بانک رسالت ساتنا 2',
        'saderat': 'بانک صادرات',
        'saderat_2': 'بانک صادرات 2',
        'saderat_paya': 'بانک صادرات پایا',
        'day': 'بانک دی',
        'day_satna': 'بانک دی ساتنا',
        'shahr': 'بانک شهر',
        'shahr_paya': 'بانک شهر پایا',
        'shahr_paya_2': 'بانک شهر پایا 2',
        'shahr_satna': 'بانک شهر ساتنا',
        'sina_paya': 'بانک سینا پایا',
    }
    return bank_type_list[bank_type]


def format_amount(amount, splitter=','):
    reversed_amount = amount[::-1]
    grouped = [reversed_amount[i:i + 3] for i in range(0, len(reversed_amount), 3)]
    formatted_amount = splitter.join(grouped)[::-1]
    return formatted_amount


def convert_numbers_to_farsi(text):
    english_to_farsi = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    return text.translate(english_to_farsi)


def do_signer_small(text: str):
    splits = text.split(' ')
    if len(splits) > 2:
        return splits[1][0] + ' ' + splits[0][0]
    return text[0]


def convert_number_to_words(number):
    number = str(number)
    result = ""
    if "-" in number:
        inputN = number.replace("-", "")
        result += "منفی "
    elif "+" in number:
        inputN = number.replace("+", "")

    inputN = number.zfill(61)
    intN = int(number)

    if intN > 10 ** 61:
        print("خطا: عدد مورد نظر شما خارج از محدوده مشخص شده برای این برنامه میباشد.")
        quit()

    yekan = ["", "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه"]
    dahha = ["ده", "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده", "نوزده"]
    tabist = yekan + dahha
    dahgan = ["", "ده", "بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود"]
    sadgan = ["", "یکصد", "دویست", "سیصد", "چهارصد", "پانصد", "ششصد", "هفتصد", "هشتصد", "نهصد"]
    adadbozorg = {3: "هزار", 6: "میلیون", 9: "میلیارد", 12: "تریلیون",
                  15: "کوآدریلیون", 18: "کوینتیلیون", 21: "سکستیلیون", 24: "سپتیلیون",
                  27: "اکتیلیون", 30: "نانیلیون", 33: "دسیلیون", 36: "آندسیلیون",
                  39: "دیودسیلیون", 42: "تریدسیلیون", 45: "کواتیوردسیلیون", 48: "کویندسیلیون",
                  51: "سکسدسیلیون", 54: "سپتدسیلیون", 57: "اکتودسیلیون", 60: "نومدسیلیون"}

    va = " و "
    space = " "
    empty = ""

    listN = []
    for i in inputN:
        listN.append(i)

    def tahezar(number):
        if number > 0 and number < 10:
            return yekan[number]
        elif number % 10 == 0 and number < 100:
            return dahgan[number // 10]
        elif number > 10 and number < 20:
            return dahha[number - 10]
        elif number > 20 and number < 100:
            dahganNumberTahezar, yekanNumberTahezar = divmod(number, 10)
            word = str(dahgan[dahganNumberTahezar]) + \
                   va + str(yekan[yekanNumberTahezar])
            return word
        elif number % 100 == 0 and number < 1000:
            return sadgan[number // 100]
        elif number > 100 and number < 120:
            word = sadgan[1] + va + tabist[number - 100]
            return word
        elif number >= 120 and number < 200 and (number - 100) % 10 == 0:
            word = sadgan[1] + va + dahgan[(number - 100) // 10]
            return word
        elif number > 200 and number < 220:
            word = sadgan[2] + va + tabist[number - 200]
            return word
        elif number >= 220 and number < 300 and (number - 200) % 10 == 0:
            word = sadgan[2] + va + dahgan[(number - 200) // 10]
            return word
        elif number > 300 and number < 320:
            word = sadgan[3] + va + tabist[number - 300]
            return word
        elif number >= 320 and number < 400 and (number - 300) % 10 == 0:
            word = sadgan[3] + va + dahgan[(number - 300) // 10]
            return word
        elif number > 400 and number < 420:
            word = sadgan[4] + va + tabist[number - 400]
            return word
        elif number >= 420 and number < 500 and (number - 400) % 10 == 0:
            word = sadgan[4] + va + dahgan[(number - 400) // 10]
            return word
        elif number > 500 and number < 520:
            word = sadgan[5] + va + tabist[number - 500]
            return word
        elif number >= 520 and number < 600 and (number - 500) % 10 == 0:
            word = sadgan[5] + va + dahgan[(number - 500) // 10]
            return word
        elif number > 600 and number < 620:
            word = sadgan[6] + va + tabist[number - 600]
            return word
        elif number >= 620 and number < 700 and (number - 600) % 10 == 0:
            word = sadgan[6] + va + dahgan[(number - 600) // 10]
            return word
        elif number > 700 and number < 720:
            word = sadgan[7] + va + tabist[number - 700]
            return word
        elif number >= 720 and number < 800 and (number - 700) % 10 == 0:
            word = sadgan[7] + va + dahgan[(number - 700) // 10]
            return word
        elif number > 800 and number < 820:
            word = sadgan[8] + va + tabist[number - 800]
            return word
        elif number >= 820 and number < 900 and (number - 800) % 10 == 0:
            word = sadgan[8] + va + dahgan[(number - 800) // 10]
            return word
        elif number > 900 and number < 920:
            word = sadgan[9] + va + tabist[number - 900]
            return word
        elif number >= 920 and number < 1000 and (number - 900) % 10 == 0:
            word = sadgan[9] + va + dahgan[(number - 900) // 10]
            return word
        else:
            sadganTahezar = number // 100
            dahganTahezar = (number - sadganTahezar * 100) // 10
            yekanTahezar = (number - sadganTahezar * 100 - dahganTahezar * 10)
            word = sadgan[sadganTahezar] + va + \
                   dahgan[dahganTahezar] + va + yekan[yekanTahezar]
            return word

    tahezarN = listN[58:]
    hezarN = listN[55:58]
    millionN = listN[52:55]
    milliardN = listN[49:52]
    trillionN = listN[46:49]
    quadrillionN = listN[43:46]
    quintillionN = listN[40:43]
    sextillionN = listN[37:40]
    septillionN = listN[34:37]
    octillionN = listN[31:34]
    nonillionN = listN[28:31]
    decillionN = listN[25:28]
    undecillionN = listN[22:25]
    duodecillionN = listN[19:22]
    tredecillion = listN[16:19]
    quattuordecillonN = listN[13:16]
    quindecillionN = listN[10:13]
    sexdecillionN = listN[7:10]
    septendecillionN = listN[4:7]
    octodecillionN = listN[1:4]
    novemdN = listN[0]

    tahezarNs, tahezarNi = tahezar(int(empty.join(tahezarN))), int(empty.join(tahezarN))
    hezarNs, hezarNi = tahezar(int(empty.join(hezarN))), int(empty.join(hezarN))
    millionNs, millionNi = tahezar(int(empty.join(millionN))), int(empty.join(millionN))
    milliardNs, milliardNi = tahezar(int(empty.join(milliardN))), int(empty.join(milliardN))
    trillionNs, trillionNi = tahezar(int(empty.join(trillionN))), int(empty.join(trillionN))
    quadrillionNs, quadrillionNi = tahezar(int(empty.join(quadrillionN))), int(empty.join(quadrillionN))
    quintillionNs, quintillionNi = tahezar(int(empty.join(quintillionN))), int(empty.join(quintillionN))
    sextillionNs, sextillionNi = tahezar(int(empty.join(sextillionN))), int(empty.join(sextillionN))
    septillionNs, septillionNi = tahezar(int(empty.join(septillionN))), int(empty.join(septillionN))
    octillionNs, octillionNi = tahezar(int(empty.join(octillionN))), int(empty.join(octillionN))
    nonillionNs, nonillionNi = tahezar(int(empty.join(nonillionN))), int(empty.join(nonillionN))
    decillionNs, decillionNi = tahezar(int(empty.join(decillionN))), int(empty.join(decillionN))
    undecillionNs, undecillionNi = tahezar(int(empty.join(undecillionN))), int(empty.join(undecillionN))
    duodecillionNs, duodecillionNi = tahezar(int(empty.join(duodecillionN))), int(empty.join(duodecillionN))
    tredecillionNs, tredecillionNi = tahezar(int(empty.join(tredecillion))), int(empty.join(tredecillion))
    quattuordecillionNs, quattuordecillionNi = tahezar(int(empty.join(quattuordecillonN))), int(
        empty.join(quattuordecillonN))
    quindecillionNs, quindecillionNi = tahezar(int(empty.join(quindecillionN))), int(empty.join(quindecillionN))
    sexdecillionNs, sexdecillionNi = tahezar(int(empty.join(sexdecillionN))), int(empty.join(sexdecillionN))
    septendecillonNs, septendecillonNi = tahezar(int(empty.join(septendecillionN))), int(empty.join(septendecillionN))
    octodecillionNs, octodecillionNi = tahezar(int(empty.join(octodecillionN))), int(empty.join(octodecillionN))
    novemdNs, novemdNi = yekan[int(empty.join(novemdN))], int(empty.join(novemdN))

    if intN == 0:
        result = "صفر"

    if novemdNi > 0:
        result += novemdNs + space + adadbozorg[60]
        if intN % (10 ** 60) != 0:
            result += va

    if octodecillionNi > 0:
        result += octodecillionNs + space + adadbozorg[57]
        if intN % (10 ** 57) != 0:
            result += va

    if septendecillonNi > 0:
        result += septendecillonNs + space + adadbozorg[54]
        if intN % (10 ** 54) != 0:
            result += va

    if sexdecillionNi > 0:
        result += sexdecillionNs + space + adadbozorg[51]
        if intN % (10 ** 51) != 0:
            result += va

    if quindecillionNi > 0:
        result += quindecillionNs + space + adadbozorg[48]
        if intN % (10 ** 48) != 0:
            result += va

    if quattuordecillionNi > 0:
        result += quattuordecillionNs + space + adadbozorg[45]
        if intN % (10 ** 45) != 0:
            result += va

    if tredecillionNi > 0:
        result += tredecillionNs + space + adadbozorg[42]
        if intN % (10 ** 42) != 0:
            result += va

    if duodecillionNi > 0:
        result += duodecillionNs + space + adadbozorg[39]
        if intN % (10 ** 39) != 0:
            result += va

    if undecillionNi > 0:
        result += undecillionNs + space + adadbozorg[36]
        if intN % (10 ** 36) != 0:
            result += va

    if decillionNi > 0:
        result += decillionNs + space + adadbozorg[33]
        if intN % (10 ** 33) != 0:
            result += va

    if nonillionNi > 0:
        result += nonillionNs + space + adadbozorg[30]
        if intN % (10 ** 30) != 0:
            result += va

    if octillionNi > 0:
        result += octillionNs + space + adadbozorg[27]
        if intN % (10 ** 27) != 0:
            result += va

    if septillionNi > 0:
        result += septillionNs + space + adadbozorg[24]
        if intN % (10 ** 24) != 0:
            result += va

    if sextillionNi > 0:
        result += sextillionNs + space + adadbozorg[21]
        if intN % (10 ** 21) != 0:
            result += va

    if quintillionNi > 0:
        result += quintillionNs + space + adadbozorg[18]
        if intN % (10 ** 18) != 0:
            result += va

    if quadrillionNi > 0:
        result += quadrillionNs + space + adadbozorg[15]
        if intN % (10 ** 15) != 0:
            result += va

    if trillionNi > 0:
        result += trillionNs + space + adadbozorg[12]
        if intN % (10 ** 12) != 0:
            result += va

    if milliardNi > 0:
        result += milliardNs + space + adadbozorg[9]
        if intN % (10 ** 9) != 0:
            result += va

    if millionNi > 0:
        result += millionNs + space + adadbozorg[6]
        if intN % (10 ** 6) != 0:
            result += va

    if hezarNi > 0:
        result += hezarNs + space + adadbozorg[3]
        if intN % (10 ** 3) != 0:
            result += va

    if tahezarNi > 0:
        result += tahezarNs

    return result


def mask_string(s):
    if len(s) <= 4:
        return s
    return s[0] + s[1] + '*' * (len(s) - 4) + s[-2] + s[-1]


def format_number_sina_pay(input_str):
    if len(input_str) < 5:
        return input_str
    return f"{input_str[:3]}-{input_str[3]}{'*' * (len(input_str) - 5)}-{input_str[-1]}"


def format_iban_shar_satna(input_str, splitter='-'):
    reversed_amount = input_str
    grouped = [reversed_amount[i:i + 4] for i in range(0, len(reversed_amount), 4)]
    formatted_amount = splitter.join(grouped)
    return formatted_amount
    # if len(input_str) < 26:
    #     return input_str
    # return f"{input_str[:4]}-{input_str[4:7]}-{input_str[8:12]}-{input_str[8:12]}"


def bank_from_codes(code=''):
    bank_codes = {
        '011': 'sanat.png',
        '012': 'mellat.png',
        '013': 'refah.png',
        '014': 'maskan.png',
        '015': 'sepah.png',
        '016': 'keshavarzi.png',
        '017': 'meli.png',
        '018': 'tejarat.png',
        '019': 'saderat.png',
        '020': 'tose_saderat.png',
        '021': 'post_bank.png',
        '022': 'tose_taavon.png',
        '030': 'qavamin.png',
        '051': 'tose.png',
        '053': 'kar_afarin.png',
        '054': 'parsian.png',
        '055': 'eghtesad.png',
        '056': 'saman.png',
        '057': 'pasargad.png',
        '058': 'sarmayeh.png',
        '059': 'sina.png',
        '060': 'mehr.png',
        '061': 'shahr.png',
        '062': 'ayandeh.png',
        '063': 'ansar.png',
        '064': 'gardeshgari.png',
        '065': 'hekmat.png',
        '066': 'day.png',
        '069': 'iran_zamin.png',
    }
    return bank_codes[code]


def get_bank_icon(iban, bank=''):
    ib = iban
    if bank == 'saderat' \
            or bank == 'pasargad_shaba':
        ib = 'IR' + ib
    elif len(ib) < 26:
        return ''
    ib = ib.replace(" ", "").replace("-", "")
    return bank_from_codes(ib[4:7])


def main():
    load_dotenv()
    token = os.environ.get('TOKEN')
    application = Application.builder().token(token=token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_ACTION: [CallbackQueryHandler(handle_select_action)],
            SELECT_BANK: [CallbackQueryHandler(handle_select_bank)],
            GET_DATETIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_datetime)],
            GET_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_amount)],
            GET_SOURCE_ACCOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_source_account)],
            GET_DEST_IBAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_dest_iban)],
            GET_DEST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_dest_name)],
            GET_SENDER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_sender_name)],
            GET_DEST_ACCOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_dest_account)],
            GET_DEST_BANK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_dest_bank)],
            GET_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_reason)],
            GET_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_description)],
            RETURN_MENU: [CallbackQueryHandler(handle_return_menu)],
            GET_TRACKING_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tracking_code)],
            GET_MARJA: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_marja)],
            GET_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_date)],
            GET_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_time)],
            GET_RECEIVER_FNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_receiver_fname)],
            GET_RECEIVER_LNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_receiver_lname)],
            GET_SOURCE_IBAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_source_iban)],
            GET_MANDE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_mande)],
            GET_DESCRIPTION2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_description2)],
            GET_DESCRIPTION3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_description3)],
            GET_SIGNER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_signer)],
            GET_DAY_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_day_name)],
            GET_REDUCE_SOURCE_ACCOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_reduce_source_account)],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
