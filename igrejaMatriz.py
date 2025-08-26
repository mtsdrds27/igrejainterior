import asyncio
import os
import random
from threading import Thread
from flask import Flask
from telegram import Bot
from telegram.error import TelegramError

# --- Configuração ---
# Na Render, configure estas variáveis no ambiente da plataforma
TOKEN = os.environ.get('TOKEN')
CHAT_ID = int(os.environ.get('CHAT_ID', 0)) # Usamos int() para converter a string

# --- Lógica do Bot ---
bot = Bot(token=TOKEN)

async def enviar_mensagem_aleatoria():
    """Função principal do bot que envia mensagens em loop."""
    print("Bot com relógio iniciado...")
    while True:
        try:
            numero_de_badaladas = random.randint(1, 12)
            print(f"Enviando {numero_de_badaladas} badaladas...")
            
            for i in range(1, numero_de_badaladas + 1):
                texto_hora = f'SÃO {i} HORAS'
                if i == 1:
                    texto_hora = f'É {i} HORA'

                await bot.send_message(chat_id=CHAT_ID, text=texto_hora)
                await bot.send_message(chat_id=CHAT_ID, text="BONG")
                await asyncio.sleep(2)

            espera = random.randint(600, 10800)
            print(f"Envio concluído. Próxima badalada em {espera // 60} minutos.")
            await asyncio.sleep(espera)

        except (TelegramError, Exception) as e:
            print(f"Ocorreu um erro: {e}")
            await asyncio.sleep(300)

def run_bot_loop():
    """Cria e executa o loop de eventos asyncio para o bot."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(enviar_mensagem_aleatoria())

# --- Configuração do Servidor Web ---
app = Flask(__name__)

@app.route('/')
def home():
    # Esta página serve apenas para a Render saber que o serviço está saudável
    return "Bot está vivo e operando!"

# Inicia o bot em um processo de fundo assim que o servidor web começa
bot_thread = Thread(target=run_bot_loop)
bot_thread.daemon = True
bot_thread.start()