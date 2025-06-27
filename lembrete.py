import telebot
import os

TOKEN = os.environ.get('BOT_TOKEN')
APOIADORES = os.environ.get('APOIADORES')

bot = telebot.TeleBot(TOKEN)

if __name__ == "__main__":

    mensagem = (
        '🏦 <b>Finanças do Calango</b>\n\n'
        '🔄 Para atualizar o saldo, envie\n'+
        '<code>/atualiza_saldo@ContribuaCalangoBot</code>\n\n'+
        '📮 Para enviar o aviso no grupo @CalangoHC, envie\n'+
        '<code>/avisa@ContribuaCalangoBot</code>'
    )

    bot.send_message(
        APOIADORES,
        mensagem,
        parse_mode='HTML'
    )
