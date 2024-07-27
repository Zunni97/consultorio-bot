#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

# async def clear_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     chat_id = update.message.chat_id
#     message_id = update.message.message_id
#     print(f"chat_id = {chat_id} - message_id = {message_id}")
#     cant = 0
#     for msg_id in range(message_id,0,-1):
#         try:
#             await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
#             print(f"Deleting --> {msg_id}")
#         except Exception as e:
#             cant = cant + 1
#             if cant == 5:
#                 break
#             logger.info(f"Could not delete message {msg_id}: {e}")

async def clear_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Delete the message that triggered the button press or command."""
    # Determina si el mensaje proviene de un comando o de un botón
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    elif update.callback_query and update.callback_query.message:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
    elif update.callback_query and update.callback_query.message:
        chat_id = update.callback_query.message.photo.chat_id
        message_id = update.callback_query.message.photo.message_id
    else:
        logger.info("No se pudo obtener el chat_id o message_id.")
        return

    print(f"chat_id = {chat_id} - message_id = {message_id}")

    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        print(f"Deleted message {message_id}")
    except Exception as e:
        logger.info(f"Could not delete message {message_id}: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    print(f"Usuario: {user.id} ha iniciado la conversación.")
    user = update.effective_user

    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id
    
    keyboard = [[InlineKeyboardButton('Agendar Cita', callback_data='cita')],
                    [InlineKeyboardButton('Contacto', callback_data='contacto')],
                    [InlineKeyboardButton('Sobre Nosotros', callback_data = 'nosotros')],
                    [InlineKeyboardButton('Salir', callback_data='salir')]]
    menu_choices = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
    chat_id=chat_id, text="Bienvenido a SmileWorks, estamos aqui para ayudarte con cualquier pregunta o inquietud que tengas sobre tus dientes. Por favor selecciona una de nuestras opciones:", reply_markup=menu_choices)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    mensaje = update.message.text
    if update.message.text == 'hola':
        mensaje = "Hola como estas?"
        await update.message.reply_text(mensaje)
        await context.bot.send_message(
            chat_id=update.message.chat_id, text="", reply_markup=mensaje)
        
async def salir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /salir is issued."""

    # Determina si el chat_id viene de un mensaje o de una interacción de botón
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id

    keyboard = [[InlineKeyboardButton('Iniciar', callback_data = 'menu')]]
    menu_choices = InlineKeyboardMarkup(keyboard)
    # Send the message with menu
    await context.bot.send_message(
    chat_id=chat_id, text="Gracias por su preferencia, si desea volver a contactarnos solo debe presionar el boton de Iniciar.", reply_markup=menu_choices)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /menu is issued."""

    # Determina si el chat_id viene de un mensaje o de una interacción de botón
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id

    keyboard = [[InlineKeyboardButton('Agendar Cita', callback_data='cita')],
                    [InlineKeyboardButton('Contacto', callback_data='contacto')],
                    [InlineKeyboardButton('Sobre Nosotros', callback_data = 'nosotros')],
                    [InlineKeyboardButton('Salir', callback_data='salir')]]
    menu_choices = InlineKeyboardMarkup(keyboard)
# Send the message with menu
    await context.bot.send_message(
    chat_id=chat_id, text="Bienvenido a SmileWorks, estamos aqui para ayudarte con cualquier pregunta o inquietud que tengas sobre tus dientes. Por favor selecciona una de nuestras opciones:", reply_markup=menu_choices)

async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /contacto is issued."""

    # Determina si el chat_id viene de un mensaje o de una interacción de botón
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id

    keyboard = [[InlineKeyboardButton('Menu', callback_data='menu')]]
    menu_choices = InlineKeyboardMarkup(keyboard)

    # Enviar la imagen desde un archivo local
    photo_file_path = "smileworks.jpg"
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=open(photo_file_path, 'rb')
    )

    # Send the message with menu
    await context.bot.send_message(
    chat_id=chat_id, 
    text="Estamos ubicados en calle sexta #1447-7 (a un costado de la catedral). Telefono: (646)4877812 y (646)4877812. Buscanos en Facebook e Instagram como: Smileworks ens. Horario: Lunes - Viernes 9:00 a 19:00, Sabado - 9:00 a 15:00, Domingo: Previa Cita", 
    reply_markup=menu_choices)

async def nosotros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /nosotros is issued."""

    # Determina si el chat_id viene de un mensaje o de una interacción de botón
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id

    keyboard = [[InlineKeyboardButton('Menu', callback_data='menu')]]
    menu_choices = InlineKeyboardMarkup(keyboard)

    # Enviar la imagen desde un archivo local
    photo_file_path = "maiky.jpg"
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=open(photo_file_path, 'rb')
    )

    # Send the message with menu
    await context.bot.send_message(
    chat_id=chat_id, 
    text="Nuestra mision es brindar atencion dental personalizada y de alta calidad a nuestros pacientes, con el fin de mejorar su salud bucal. Nos esforzamos por crear un ambiente seguro, confiable y amigable, donde nuestros pacientes se sientan comodos y valorados.", 
    reply_markup=menu_choices)

async def cita(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /cita is issued."""

    # Determina si el chat_id viene de un mensaje o de una interacción de botón
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id

    keyboard = [[InlineKeyboardButton('Eliminacion de Caries', callback_data='mes')],
                [InlineKeyboardButton('Extracciones', callback_data='mes')],
                [InlineKeyboardButton('Limpieza', callback_data='mes')],
                [InlineKeyboardButton('Valoracion', callback_data='mes')],
                [InlineKeyboardButton('Regresar', callback_data='menu')],
                [InlineKeyboardButton('Salir', callback_data='salir')]]
    menu_choices = InlineKeyboardMarkup(keyboard)
# Send the message with menu
    await context.bot.send_message(
    chat_id=chat_id, text="¿Que tipo de Cita necesitas?", reply_markup=menu_choices)

async def mes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /mes is issued."""
    
    # Determina si el chat_id viene de un mensaje o de una interacción de botón
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id  
    
    keyboard = [[InlineKeyboardButton('Julio', callback_data='dia'),
                InlineKeyboardButton('Agosto', callback_data='dia'),
                InlineKeyboardButton('Septiembre', callback_data='dia')],
                [InlineKeyboardButton('Octubre', callback_data='dia'),
                InlineKeyboardButton('Noviembre', callback_data='dia'),
                InlineKeyboardButton('Diciembre', callback_data='dia')],
                [InlineKeyboardButton('Regresar', callback_data='cita'),
                InlineKeyboardButton('Salir', callback_data='salir')]]
    menu_choices = InlineKeyboardMarkup(keyboard)
# Send the message with menu
    await context.bot.send_message(
    chat_id=chat_id, text="Seleccione el mes para agendar su cita", reply_markup=menu_choices)

async def dia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /dia is issued."""
    
    # Determina si el chat_id viene de un mensaje o de una interacción de botón
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id 
    
    keyboard = [
    [InlineKeyboardButton('1', callback_data='horario'),
     InlineKeyboardButton('2', callback_data='horario'),
     InlineKeyboardButton('3', callback_data='horario'),
     InlineKeyboardButton('4', callback_data='horario'),
     InlineKeyboardButton('5', callback_data='horario'),
     InlineKeyboardButton('6', callback_data='horario'),
     InlineKeyboardButton('7', callback_data='horario')],
         [InlineKeyboardButton('8', callback_data='horario'),
     InlineKeyboardButton('9', callback_data='horario'),
     InlineKeyboardButton('10', callback_data='horario'),
     InlineKeyboardButton('11', callback_data='horario'),
     InlineKeyboardButton('12', callback_data='horario'),
     InlineKeyboardButton('13', callback_data='horario'),
     InlineKeyboardButton('14', callback_data='horario')],
         [InlineKeyboardButton('15', callback_data='horario'),
     InlineKeyboardButton('16', callback_data='horario'),
     InlineKeyboardButton('17', callback_data='horario'),
     InlineKeyboardButton('18', callback_data='horario'),
     InlineKeyboardButton('19', callback_data='horario'),
     InlineKeyboardButton('20', callback_data='horario'),
     InlineKeyboardButton('21', callback_data='horario')],
         [InlineKeyboardButton('22', callback_data='horario'),
     InlineKeyboardButton('23', callback_data='horario'),
     InlineKeyboardButton('24', callback_data='horario'),
     InlineKeyboardButton('25', callback_data='horario'),
     InlineKeyboardButton('26', callback_data='horario'),
     InlineKeyboardButton('27', callback_data='horario'),
     InlineKeyboardButton('28', callback_data='horario')],    
        [InlineKeyboardButton('29', callback_data='horario'),
     InlineKeyboardButton('30', callback_data='horario'),
     InlineKeyboardButton('31', callback_data='horario')],
     [InlineKeyboardButton('Regresar', callback_data='mes'),
     InlineKeyboardButton('Salir', callback_data='salir')]
 ]
    menu_choices = InlineKeyboardMarkup(keyboard)
# Send the message with menu
    await context.bot.send_message(
    chat_id=chat_id, text="Selecciona el dia de tu cita", reply_markup=menu_choices)

async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /horario is issued."""
    # Determina si el chat_id viene de un mensaje o de una interacción de botón
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id     
    
    keyboard = [[InlineKeyboardButton('9:00', callback_data='confirmacion'),
                InlineKeyboardButton('10:00', callback_data='confirmacion'),
                InlineKeyboardButton('11:00', callback_data='confirmacion'),
                InlineKeyboardButton('12:00', callback_data='confirmacion')],
                [InlineKeyboardButton('13:00', callback_data='confirmacion'),
                InlineKeyboardButton('14:00', callback_data='confirmacion'),
                InlineKeyboardButton('15:00', callback_data='confirmacion'),
                InlineKeyboardButton('16:00', callback_data='confirmacion')],
                [InlineKeyboardButton('17:00', callback_data='confirmacion'),
                InlineKeyboardButton('16:00', callback_data='confirmacion')],
                [InlineKeyboardButton('Regresar', callback_data='dia'),
                InlineKeyboardButton('Salir', callback_data='salir')]]
    menu_choices = InlineKeyboardMarkup(keyboard)
# Send the message with menu
    await context.bot.send_message(
    chat_id=chat_id, text="Seleccione la hora de su cita:", reply_markup=menu_choices)

async def confirmacion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /confirmacion is issued."""

    # Determina si el chat_id viene de un mensaje o de una interacción de botón
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id

    keyboard = [[InlineKeyboardButton('Menu', callback_data = 'menu')],
                [InlineKeyboardButton('Salir', callback_data='salir')]]
    menu_choices = InlineKeyboardMarkup(keyboard)
# Send the message with menu
    await context.bot.send_message(
    chat_id=chat_id, text="Su cita ha sido confirmada, se recomienda llegar 10 minutos antes a su cita. Gracias por confiar en SmileWorks estamos para servirle.", reply_markup=menu_choices)

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks and dispatch to the corresponding command handler."""
    query = update.callback_query
    await query.answer()

    # Dependiendo del callback_data, llama a la función correspondiente
    await clear_chat(update, context)

    callback_data = query.data

    if callback_data == "menu":
        await menu(update, context)
    elif callback_data == "cita":
        await cita(update, context)
    elif callback_data == "contacto":
        await contacto(update, context)
    elif callback_data == "nosotros":
        await nosotros(update, context)
    elif callback_data == "mes":
        await mes(update, context)
    elif callback_data == "dia":
        await dia(update, context)
    elif callback_data == "horario":
        await horario(update, context)
    elif callback_data == "confirmacion":
        await confirmacion(update, context)
    elif callback_data == "salir":
        await salir(update, context)
    elif callback_data == "start":
        await salir(update, context)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7207648344:AAGgu0bHwdDoscJmdFVKSksEfkwmNEI_qPc").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("contacto", contacto))
    application.add_handler(CommandHandler("nosotros", nosotros))
    application.add_handler(CommandHandler("cita", cita))
    application.add_handler(CommandHandler("mes", mes))
    application.add_handler(CommandHandler("dia", dia))
    application.add_handler(CommandHandler("horario", horario))
    application.add_handler(CommandHandler("confirmacion", horario))
    application.add_handler(CommandHandler("salir", salir))

    # CallbackQueryHandler para manejar los botones
    application.add_handler(CallbackQueryHandler(buttons))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()