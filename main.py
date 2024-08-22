
from jinja2 import Environment, FileSystemLoader
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, \
    filters, ContextTypes
import logging
import imgkit



(START, RETURN_MENU, SELECT_ACTION, SELECT_BANK, GET_STATUS, GET_TRANSACTION_TYPE, GET_SOURCE_ACCOUNT, GET_DEST_IBAN,
 GET_DEST_NAME, GET_DATETIME, GET_AMOUNT, GET_SENDER_NAME, GET_DEST_ACCOUNT, GET_DEST_BANK, GET_REASON, GET_DESCRIPTION,
 GET_TRACKING_CODE, GET_MARJA) = range(18)

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

    await query.edit_message_text('تاریخ و ساعت را به صورت ۱۴۰۳/۰۵/۲۴ ۱۲:۴۵ وارد کنید')
    return GET_DATETIME


async def handle_get_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['datetime'] = update.message.text

    await update.message.reply_text('مبلغ را به ریال وارد کنید ')
    return GET_AMOUNT


async def handle_get_amount(update: Update, context):
    context.user_data['amount'] = update.message.text

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

    await update.message.reply_text('نام صاحب شبا را وارد کنید:')
    return GET_DEST_NAME


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

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_get_sender_name(update: Update, context):
    context.user_data['sender'] = update.message.text
    if context.user_data['bank_type'] == 'tejarat' \
            or context.user_data['bank_type'] == 'sepah_paya'\
            or context.user_data['bank_type'] == 'saman_paya_light'\
            or context.user_data['bank_type'] == 'saman_paya_dark':
        await update.message.reply_text('کد پیگیری را وارد کنید:')
        return GET_TRACKING_CODE

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_dest_account(update: Update, context):
    context.user_data['receiver_account'] = update.message.text
    if context.user_data['bank_type'] == 'sepah_satna' \
            or context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('نام بانک مقصد را وارد کنید:')
        return GET_DEST_BANK

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SENDER_NAME


async def handle_get_description(update: Update, context):
    context.user_data['description'] = update.message.text
    if context.user_data['bank_type'] == 'sepah_paya':
        await update.message.reply_text('نام ارسال کننده را وارد کنید:')
        return GET_SENDER_NAME
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

    await update.message.reply_text('شماره حساب مبدا را وارد کنید:')
    return GET_SOURCE_ACCOUNT


async def handle_tracking_code(update: Update, context):
    context.user_data['tracking_code'] = update.message.text
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
        html_content = {
            'bank_type': get_bank_type_in_farsi(context.user_data['bank_type']),
            'datetime': convert_numbers_to_farsi(context.user_data['datetime']),
            'amount': format_amount(convert_numbers_to_farsi(context.user_data['amount'])),
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
        },
        fallbacks=[CommandHandler('start', start)],
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()