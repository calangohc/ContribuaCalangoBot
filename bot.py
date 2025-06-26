import configparser
import datetime
import sqlite3
import telebot
import os

config = configparser.ConfigParser()
config.sections()

config.read('calango.conf')
TOKEN = config['BOT']['TOKEN']
APOIADORES = config['APOIADORES']['ID']
CALANGOHC = config['CALANGOHC']['ID']

bot = telebot.TeleBot(TOKEN)

force_reply = telebot.types.ForceReply(
    selective=False,
    input_field_placeholder='Digite o saldo'
)

botao_apoia_se = telebot.types.InlineKeyboardMarkup()
btn = telebot.types.InlineKeyboardButton(
    f'💳 Apoia-se',
    url='https://apoia.se/calangohc'
)
botao_apoia_se.row(btn)

def le_ultimos_dez_valores_da_tabela():
    conn = sqlite3.connect('Calango.db')
    cursor = conn.cursor()
    aux = ('SELECT * FROM saldo order by data desc LIMIT 10')
    cursor.execute(aux)
    data = cursor.fetchall()
    conn.close()
    return data

def le_ultimo_valor_da_tabela():
    conn = sqlite3.connect('Calango.db')
    cursor = conn.cursor()
    aux = ('SELECT * FROM saldo order by data desc LIMIT 1')
    cursor.execute(aux)
    data = cursor.fetchone()
    conn.close()
    return data

def insere_na_tabela(message):
    try:
        valor = float(message.text.replace(',','.'))
    except:
        bot.reply_to(message, 'Cancelado')
        return
    data = str(datetime.datetime.now())
    conn = sqlite3.connect('Calango.db')
    cursor = conn.cursor()
    aux = (
        'INSERT INTO saldo '+
        '(chatid, data, valor) '+
        f'VALUES ("{message.from_user.id}", "{data}", {valor})'
    )
    cursor.execute(aux)
    conn.commit()
    conn.close()
    bot.reply_to(message, '💾 Salvo')

def espera_saldo(message):
    insere_na_tabela(message)

@bot.message_handler(commands=['atualiza_saldo'])
def cmd_atualiza_saldo(message):
    if bot.get_chat_member(APOIADORES, message.from_user.id).status == 'left':
        print('Somente os portadores da chave do CalangoHC podem atualizar o saldo.')
        return
    msg = bot.reply_to(message, 'Envie o saldo atual', reply_markup=force_reply)
    bot.register_next_step_handler(msg, espera_saldo)

@bot.message_handler(commands=['historico'])
def cmd_historico(message):
    dados = le_ultimos_dez_valores_da_tabela()
    historico = ''
    for linha in reversed(dados):
        if message.chat.id == APOIADORES:
            historico = f'{historico}\n{linha[1]:<10} {linha[2][:16]:<17} {linha[3]:<8}'
        else:
            historico = f'{historico}\n{linha[2][:16]:<17} R$ {linha[3]:<8}'
    mensagem = (
        '🗄 <b>Histórico</b>'+
        f'<blockquote expandable>{historico}</blockquote>'
    )

    bot.reply_to(message, mensagem, parse_mode='HTML') 

@bot.message_handler(commands=['avisa'])
def cmd_avisa_grupao(message):
    if bot.get_chat_member(APOIADORES, message.from_user.id).status == 'left':
        print('Somente os portadores da chave do CalangoHC podem enviar o aviso.')
        return
    cmd_saldo(None)
    bot.reply_to(message, 'Mensagem enviada')

@bot.message_handler(commands=['saldo'])
def cmd_saldo(message):
    dados = le_ultimo_valor_da_tabela()
    data = dados[2]
    saldo = dados[3]

    mensagem = (
        '🏦 <b>Finanças do Calango</b>\n\n'
        'O @CalangoHC precisa de R$ 2.000,00 para virar o mês.\n\n'+
        f'No momento, nosso saldo é de R$ {saldo}, '+
        f'<b>que cobre o custo de {float(saldo)/60:.2f} dias</b>. ⚠️\n\n'+
        '💶 <b>Contribua!</b>\n'+
        ' 🔸 <a href="https://apoia.se/calangohc">Doação recorrente no Apoia-se</a>\n'+
        ' 🔸 Chave PIX: <code>pix@calango.club</code>\n\n'+
        'ℹ️ <b>Mais informações e outros meios de pagamento:</b>\n'+
        'https://calango.club/contribua'
    )
    try:
        msg = bot.send_message(message.chat.id, mensagem, parse_mode='HTML', reply_markup=botao_apoia_se)
    except AttributeError:
        msg = bot.send_message(CALANGOHC, mensagem, parse_mode='HTML', reply_markup=botao_apoia_se)
        bot.pin_chat_message(CALANGOHC, msg.id, disable_notification=True)

@bot.message_handler(content_types=telebot.util.content_type_service)
def deleta_mensagens_de_servico(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
  
if __name__ == "__main__":
    bot.set_my_commands([
        telebot.types.BotCommand("/saldo", "Consultar saldo"),
        telebot.types.BotCommand("/atualiza_saldo", "Atualizar valor"),
        telebot.types.BotCommand("/avisa", "Envia mensagem no grupo"),
        telebot.types.BotCommand("/historico", "Ver histórico"),
        ], scope=telebot.types.BotCommandScopeChat(APOIADORES)
    )

    bot.set_my_commands([
        telebot.types.BotCommand("/saldo", "Consultar saldo"),
        telebot.types.BotCommand("/historico", "Ver histórico"),
        ], scope=telebot.types.BotCommandScopeAllGroupChats()
    )

    bot.set_my_commands([
        telebot.types.BotCommand("/saldo", "Consulta saldo"),
        telebot.types.BotCommand("/historico", "Ver extrato"),
        ], scope=telebot.types.BotCommandScopeAllPrivateChats()
    )

    bot.infinity_polling()
