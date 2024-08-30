from jinja2 import Environment, FileSystemLoader
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, \
    filters, ContextTypes
import logging
import imgkit

(START, RETURN_MENU, SELECT_ACTION, SELECT_BANK, GET_STATUS, GET_TRANSACTION_TYPE, GET_SOURCE_ACCOUNT, GET_DEST_IBAN,
 GET_DEST_NAME, GET_DATETIME, GET_AMOUNT, GET_SENDER_NAME, GET_DEST_ACCOUNT, GET_DEST_BANK, GET_REASON, GET_DESCRIPTION,
 GET_TRACKING_CODE, GET_MARJA, GET_DATE, GET_TIME, GET_RECEIVER_FNAME, GET_RECEIVER_LNAME, GET_SOURCE_IBAN,
 GET_MANDE, GET_DESCRIPTION2, GET_REDUCE_SOURCE_ACCOUNT, GET_DESCRIPTION3) = range(27)

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
        [InlineKeyboardButton("بانک سامان تیره", callback_data='saman_paya_dark')],
        [InlineKeyboardButton("بانک سامان روشن", callback_data='saman_paya_light')],
        [InlineKeyboardButton("بانک سپه پایا", callback_data='sepah_paya')],
        [InlineKeyboardButton("بانک سپه ساتنا", callback_data='sepah_satna')],
        [InlineKeyboardButton("بانک تجارت", callback_data='tejarat')],
        [InlineKeyboardButton("بانک تجارت کارت به کارت", callback_data='tejarat_card')],
        [InlineKeyboardButton("بانک تجارت پایا", callback_data='tejarat_paya')],
        [InlineKeyboardButton("بانک آینده", callback_data='ayandeh')],
        [InlineKeyboardButton("بانک آینده پایا", callback_data='ayandeh_paya')],
        [InlineKeyboardButton("بانک اقتصاد", callback_data='eghtesad')],
        [InlineKeyboardButton("بانک کشاورزی", callback_data='keshavarzi')],
        [InlineKeyboardButton("بانک مهر", callback_data='mehr')],
        [InlineKeyboardButton("بانک مهر 2", callback_data='mehr_2')],
        [InlineKeyboardButton("بانک مهر 3", callback_data='mehr_3')],
        [InlineKeyboardButton("بانک مهر 4", callback_data='mehr_4')],
        [InlineKeyboardButton("بانک مهر تاریک", callback_data='mehr_dark')],
        [InlineKeyboardButton("بانک مهر تاریک 2", callback_data='mehr_dark_2')],
        [InlineKeyboardButton("بانک مهر روشن", callback_data='mehr_light')],
        [InlineKeyboardButton("بانک ملت", callback_data='mellat')],
        [InlineKeyboardButton("بانک پارسیان", callback_data='parsian')],
        [InlineKeyboardButton("بانک پاسارگاد پایا", callback_data='pasargad_paya')],
        [InlineKeyboardButton("بانک پاسارگاد پایا 2", callback_data='pasargad_paya_2')],
        [InlineKeyboardButton("بانک پاسارگاد ساتنا", callback_data='pasargad_satna')],
        [InlineKeyboardButton("بانک پست بانک پایا", callback_data='post_bank_paya')],
        [InlineKeyboardButton("بانک پست بانک پایا 2", callback_data='post_bank_paya_2')],
        [InlineKeyboardButton("بانک رفاه", callback_data='refah')],
        [InlineKeyboardButton("بانک رفاه 2", callback_data='refah_2')],
        [InlineKeyboardButton("بانک رفاه پایا", callback_data='refah_paya')],
        [InlineKeyboardButton("بانک رفاه ساتنا", callback_data='refah_satna')],
        [InlineKeyboardButton("بانک رسالت پایا", callback_data='resalat_paya')],
        [InlineKeyboardButton("بازگشت", callback_data='return_to_menu')],
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
            or context.user_data['bank_type'] == 'post_bank_paya_2'\
            or context.user_data['bank_type'] == 'refah_2'\
            or context.user_data['bank_type'] == 'refah_paya'\
            or context.user_data['bank_type'] == 'refah_satna'\
            or context.user_data['bank_type'] == 'mellat':
        await query.edit_message_text('تاریخ را به صورت ۱۴۰۳/۰۵/۲۴ وارد کنید')
        return GET_DATE

    await query.edit_message_text('تاریخ و ساعت را به صورت ۱۴۰۳/۰۵/۲۴ ۱۲:۴۵ وارد کنید')
    return GET_DATETIME


async def handle_get_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['datetime'] = update.message.text

    await update.message.reply_text('مبلغ را به ریال وارد کنید ')
    return GET_AMOUNT


async def handle_get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['date'] = update.message.text

    await update.message.reply_text('ساعت را به صورت ۱۲:۴۵ وارد کنید')
    return GET_TIME


async def handle_get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['time'] = update.message.text

    await update.message.reply_text('مبلغ را به ریال وارد کنید ')
    return GET_AMOUNT


async def handle_get_amount(update: Update, context):
    context.user_data['amount'] = update.message.text

    if context.user_data['bank_type'] == 'mehr':
        await update.message.reply_text('باقیمانده را وارد کنید:')
        return GET_MANDE

    if context.user_data['bank_type'] == 'mehr_3':
        await update.message.reply_text('باقیمانده را وارد کنید:')
        return GET_MANDE

    if context.user_data['bank_type'] == 'mehr_dark_2':
        await update.message.reply_text('باقیمانده را وارد کنید:')
        return GET_MANDE

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_get_mande(update: Update, context):
    context.user_data['mande'] = update.message.text

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_source_account(update: Update, context):
    context.user_data['source_account'] = update.message.text

    if context.user_data['bank_type'] == 'tejarat_paya':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'tejarat_card':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'tejarat':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'saman_paya_light':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'saman_paya_dark':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'ayandeh':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'ayandeh_paya':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'eghtesad':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'keshavarzi':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'maskan_satna':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr_2':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr_3':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr_dark':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr_dark_2':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mehr_light':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'mellat':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'parsian':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'post_bank_paya':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'post_bank_paya_2':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'refah':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'refah_paya':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'refah_satna':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('شماره شبا را وارد کنید:')
        return GET_DEST_IBAN

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_get_dest_iban(update: Update, context):
    context.user_data['iban'] = update.message.text
    if context.user_data['bank_type'] == 'tejarat':
        await update.message.reply_text('نام واریز کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'tejarat_card':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'tejarat_paya':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
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
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
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
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'mellat':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'parsian':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'post_bank_paya':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'post_bank_paya_2':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'refah':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'refah_paya':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'refah_satna':
        await update.message.reply_text('نام دریافت کننده را وارد کنید:')
        return GET_DEST_NAME
    if context.user_data['bank_type'] == 'resalat_paya':
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

    await update.message.reply_text('شماره شبا ارسال کننده را وارد کنید:')
    return GET_SOURCE_IBAN


async def handle_get_source_iban(update: Update, context):
    context.user_data['receiver_lname'] = update.message.text

    await update.message.reply_text('توضیحات را وارد کنید:')
    return GET_DESCRIPTION


async def handle_get_dest_name(update: Update, context):
    context.user_data['receiver'] = update.message.text
    if context.user_data['bank_type'] == 'tejarat_card':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE
    if context.user_data['bank_type'] == 'tejarat_paya':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE

    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('شماره حساب مقصد را وارد کنید:')
        return GET_DEST_ACCOUNT
    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('شماره حساب مقصد را وارد کنید:')
        return GET_DEST_ACCOUNT
    if context.user_data['bank_type'] == 'saman_paya_light':
        await update.message.reply_text('شماره حساب مقصد را وارد کنید:')
        return GET_DEST_ACCOUNT
    if context.user_data['bank_type'] == 'saman_paya_dark':
        await update.message.reply_text('شماره حساب مقصد را وارد کنید:')
        return GET_DEST_ACCOUNT

    if context.user_data['bank_type'] == 'ayandeh':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'eghtesad':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME

    if context.user_data['bank_type'] == 'ayandeh_paya':
        await update.message.reply_text('توضیحات را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'keshavarzi':
        await update.message.reply_text('توضیحات را وارد کنید:')
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
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE
    if context.user_data['bank_type'] == 'mehr_light':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE

    if context.user_data['bank_type'] == 'mehr_dark_2':
        await update.message.reply_text('توضیحات خط اول را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'mehr_4':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'mellat':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'parsian':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'post_bank_paya':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'post_bank_paya_2':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'refah_satna':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'refah':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME

    if context.user_data['bank_type'] == 'refah_paya':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_get_sender_name(update: Update, context):
    context.user_data['sender'] = update.message.text
    if context.user_data['bank_type'] == 'tejarat' \
            or context.user_data['bank_type'] == 'sepah_paya' \
            or context.user_data['bank_type'] == 'saman_paya_light' \
            or context.user_data['bank_type'] == 'saman_paya_dark' \
            or context.user_data['bank_type'] == 'ayandeh' \
            or context.user_data['bank_type'] == 'mehr_4' \
            or context.user_data['bank_type'] == 'post_bank_paya' \
            or context.user_data['bank_type'] == 'post_bank_paya_2' \
            or context.user_data['bank_type'] == 'eghtesad':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE

    if context.user_data['bank_type'] == 'mellat':
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

    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    if context.user_data['bank_type'] == 'parisan':
        await update.message.reply_text('توضیحات را وارد کنید:')
        return GET_DESCRIPTION

    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('شرح را وارد کنید:')
        return GET_DESCRIPTION

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
    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
    if context.user_data['bank_type'] == 'mehr_dark_2':
        await update.message.reply_text('توضیحات خط دوم را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('علت (بابت) انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('علت (بابت) انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('علت (بابت) انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('علت (بابت) انتقال را وارد کنید:')
        return GET_DESCRIPTION2

    await update.message.reply_text('کد پیگیری را وارد کنید:')
    return GET_TRACKING_CODE


async def handle_get_description2(update: Update, context):
    context.user_data['description2'] = update.message.text
    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('شرح را وارد کنید')
        return GET_DESCRIPTION3

    await update.message.reply_text('کد پیگیری را وارد کنید:')
    return GET_TRACKING_CODE


async def handle_get_description3(update: Update, context):
    context.user_data['description2'] = update.message.text
    await update.message.reply_text('کد پیگیری را وارد کنید:')
    return GET_TRACKING_CODE


async def handle_get_reason(update: Update, context):
    context.user_data['reason'] = update.message.text
    await update.message.reply_text('توضیحات را وارد کنید:')
    return GET_DESCRIPTION


async def handle_dest_bank(update: Update, context):
    context.user_data['receiver_bank'] = update.message.text
    if context.user_data['bank_type'] == 'sepah_satna':
        await update.message.reply_text('توضیحات را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('توضیحات را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'mellat':
        await update.message.reply_text('توضیحات را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'refah_paya':
        await update.message.reply_text('علت (بابت) را وارد کنید:')
        return GET_DESCRIPTION
    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('نام بانک کسر کارمزد را وارد کنید:')
        return GET_REDUCE_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'pasargad_paya':
        await update.message.reply_text('نام بانک کسر کارمزد را وارد کنید:')
        return GET_REDUCE_SOURCE_ACCOUNT
    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('نام بانک کسر کارمزد را وارد کنید:')
        return GET_REDUCE_SOURCE_ACCOUNT
    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('نام بانک کسر کارمزد را وارد کنید:')
        return GET_REDUCE_SOURCE_ACCOUNT
    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('نام بانک کسر کارمزد را وارد کنید:')
        return GET_REDUCE_SOURCE_ACCOUNT

    if context.user_data['bank_type'] == 'refah':
        await update.message.reply_text('علت (بابت) انتقال را وارد کنید:')
        return GET_DESCRIPTION2
    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE
    print(context.user_data['bank_type'], "=============")
    if context.user_data['bank_type'] == 'refah_satna':
        await update.message.reply_text('شناسه پرداخت را وارد کنید:')
        return GET_TRACKING_CODE

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
    if context.user_data['bank_type'] == 'mehr_dark':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'mehr_dark_2':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'mehr_light':
        await create_receipt_and_send_resid(update, context)
        return ConversationHandler.END
    if context.user_data['bank_type'] == 'mellat':
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

    if context.user_data['bank_type'] == 'pasargad_paya_2':
        await update.message.reply_text('شناسه واریز را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'pasargad_satna':
        await update.message.reply_text('شناسه واریز را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'post_bank_paya':
        await update.message.reply_text('شناسه واریز را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'refah_2':
        await update.message.reply_text('شماره درخواست را وارد کنید:')
        return GET_MARJA
    if context.user_data['bank_type'] == 'resalat_paya':
        await update.message.reply_text('شماره واریز/شماره قبض را وارد کنید:')
        return GET_MARJA
    await update.message.reply_text('کد مرجع را وارد کنید:')
    return GET_MARJA


async def handle_get_marja(update: Update, context):
    context.user_data['marja'] = update.message.text
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

    if bank_type == 'saman_paya_dark':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_account': convert_numbers_to_farsi(context.user_data['receiver_account']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
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
            'receiver_account': convert_numbers_to_farsi(context.user_data['receiver_account']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
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
            'reason': 'بدون علت',
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
        }

    if bank_type == 'sepah_satna':
        amount = context.user_data['amount']
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'amount_fa': format_amount(convert_numbers_to_farsi(convert_number_to_words(int(amount) / 10))),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_account': convert_numbers_to_farsi(context.user_data['receiver_account']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'reason': 'بدون علت',
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
        }

    if bank_type == 'tejarat':
        html_content = {
            'status': 'در حال انجام',
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
        }

    if bank_type == 'tejarat_card':
        html_content = {
            'status': 'در حال انجام',
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
        }

    if bank_type == 'tejarat_paya':
        html_content = {
            'status': 'در حال انجام',
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
        }

    if bank_type == 'ayandeh':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
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
        }

    if bank_type == 'keshavarzi':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'status': 'ارسال شده',
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
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
        }

    if bank_type == 'mehr_2':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'mande': format_amount(convert_numbers_to_farsi(context.user_data['mande'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
        }

    if bank_type == 'mehr_3':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
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
        }

    if bank_type == 'mehr_dark':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
        }

    if bank_type == 'mehr_dark_2':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'mande': format_amount(convert_numbers_to_farsi(context.user_data['mande'])),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
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
        }

    if bank_type == 'mellat':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
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
            'amount_fa': format_amount(convert_numbers_to_farsi(convert_number_to_words(int(amount) / 10))),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
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
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
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
        }

    if bank_type == 'refah_2':
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'source_account': convert_numbers_to_farsi(context.user_data['source_account']),
            'iban': convert_numbers_to_farsi(context.user_data['iban']),
            'sender': convert_numbers_to_farsi(context.user_data['sender']),
            'receiver': convert_numbers_to_farsi(context.user_data['receiver']),
            'receiver_bank': convert_numbers_to_farsi(context.user_data['receiver_bank']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
            'date': convert_numbers_to_farsi(context.user_data['date']),
            'time': convert_numbers_to_farsi(context.user_data['time']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
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
            'amount_fa': format_amount(convert_numbers_to_farsi(convert_number_to_words(int(amount) / 10))),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'tracking_code': convert_numbers_to_farsi(context.user_data['tracking_code']),
            'description': convert_numbers_to_farsi(context.user_data['description']),
            'description2': convert_numbers_to_farsi(context.user_data['description2']),
            'marja': convert_numbers_to_farsi(context.user_data['marja']),
        }

    await update.message.reply_text('در حال ساخت رسید... لطفا صبر کنید!:')
    rendered_html = template.render(html_content)
    png_path = f"./receipts/image/receipt_{context.user_data['tracking_code']}.png"
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
    elif context.user_data['bank_type'] == 'sepah_satna':
        options['height'] = '1280'
        options['width'] = '752'
    elif context.user_data['bank_type'] == 'sepah_paya':
        options['height'] = '1280'
        options['width'] = '685'
    elif context.user_data['bank_type'] == 'saman_paya_light':
        options['height'] = '1280'
        options['width'] = '752'
    elif context.user_data['bank_type'] == 'saman_paya_dark':
        options['height'] = '1280'
        options['width'] = '752'
    elif context.user_data['bank_type'] == 'saman_paya_dark':
        options['height'] = '1280'
        options['width'] = '752'
    elif context.user_data['bank_type'] == 'ayandeh':
        options['height'] = '1280'
        options['width'] = '654'
    elif context.user_data['bank_type'] == 'ayandeh_paya':
        options['height'] = '1280'
        options['width'] = '966'
    elif context.user_data['bank_type'] == 'eghtesad':
        options['height'] = '1280'
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
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'mehr_light':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'mellat':
        options['height'] = '1280'
        options['width'] = '744'
    elif context.user_data['bank_type'] == 'parsian':
        options['height'] = '1280'
        options['width'] = '687'
    elif context.user_data['bank_type'] == 'pasargad_paya':
        options['height'] = '1280'
        options['width'] = '615'
    elif context.user_data['bank_type'] == 'pasargad_paya_2':
        options['height'] = '1280'
        options['width'] = '615'
    elif context.user_data['bank_type'] == 'pasargad_satna':
        options['height'] = '1280'
        options['width'] = '623'
    elif context.user_data['bank_type'] == 'post_bank_paya':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'post_bank_paya_2':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'refah':
        options['height'] = '1289'
        options['width'] = '630'
    elif context.user_data['bank_type'] == 'refah_2':
        options['height'] = '1282'
        options['width'] = '656'
    elif context.user_data['bank_type'] == 'refah_paya':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'refah_satna':
        options['height'] = '1280'
        options['width'] = '591'
    elif context.user_data['bank_type'] == 'resalat_paya':
        options['height'] = '1280'
        options['width'] = '623'

    imgkit.from_string(rendered_html, png_path, options=options)

    await update.message.reply_photo(photo=open(png_path, 'rb'))

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
        'parsian': 'بانک پارسیان',
        'pasargad_paya': 'بانک پاسارگاد پایا',
        'pasargad_paya_2': 'بانک پاسارگاد پایا 2',
        'pasargad_satna': 'بانک پاسارگاد ساتنا',
        'post_bank_paya': 'بانک پست بانک پایا',
        'post_bank_paya_2': 'بانک پست بانک پایا 2',
        'refah': 'بانک رفاه',
        'refah_2': 'بانک رفاه 2',
        'refah_paya': 'بانک رفاه پایا',
        'refah_satna': 'بانک رفاه ساتنا',
        'resalat_paya': 'بانک رسالت پایا',
    }
    return bank_type_list[bank_type]


def format_amount(amount):
    reversed_amount = amount[::-1]
    grouped = [reversed_amount[i:i + 3] for i in range(0, len(reversed_amount), 3)]
    formatted_amount = ','.join(grouped)[::-1]
    return formatted_amount


def convert_numbers_to_farsi(text):
    english_to_farsi = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    return text.translate(english_to_farsi)


def convert_number_to_words(number):
    units = ["", "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه"]
    tens = ["", "ده", "بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود"]
    teens = ["ده", "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده", "نوزده"]
    hundreds = ["", "صد", "دویست", "سیصد", "چهارصد", "پانصد", "ششصد", "هفتصد", "هشتصد", "نهصد"]
    thousands = ["", "هزار", "میلیون", "میلیارد", "هزار میلیارد"]

    def convert_three_digits(n):
        if n == 0:
            return ""
        elif n < 10:
            return units[n]
        elif n < 20:
            return teens[n - 10]
        elif n < 100:
            return tens[n // 10] + (units[n % 10] if (n % 10) != 0 else "")
        else:
            return hundreds[n // 100] + " و " + convert_three_digits(n % 100)

    def convert_number_to_words_recursive(n, level=0):
        if n == 0:
            return ""
        else:
            return convert_number_to_words_recursive(n // 1000, level + 1) + (
                " و " if n % 1000 != 0 and level > 0 else "") + convert_three_digits(n % 1000) + (
                " " + thousands[level] if n % 1000 != 0 else "")

    result = convert_number_to_words_recursive(number).strip()
    return result if result else "صفر"


def main():
    application = Application.builder().token("7415076812:AAEqyQE_M13mYmDn8wbxE3U-d6-uoYHe_2o").build()


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
            GET_REDUCE_SOURCE_ACCOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_reduce_source_account)],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
