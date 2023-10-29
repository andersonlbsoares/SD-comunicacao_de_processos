import json
import socket
import threading
import time


data = json.load(open("dados.json"))
client_connections = []
votacao_iniciada = False
votacao_tempo_limite = 100 # Tempo limite para a votação (em segundos)

# Variável para manter a mensagem de aviso do administrador
admin_message = ""

# Função para salvar as alterações no JSON de volta ao arquivo (se necessário)
def salve_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)



def encerrar_votacao():
    global votacao_iniciada
    while True:
        if votacao_iniciada:
            time.sleep(votacao_tempo_limite)
            votacao_iniciada = False

            # Ordenar candidatos por quantidade de votos (maior para menor)
            dataEleitores = json.load(open("dados.json"))
            dataEleitores["candidatos"].sort(key=lambda x: x["votos"], reverse=True)

            print ("")
            print ("")
            print ("=======================RESULTADO=======================")
            print ("|     Votação encerrada!                              |")
            print ("|     Resultado final:                                |")
            print ("|     1º lugar: "+dataEleitores["candidatos"][0]["nome"]+" com "+str(dataEleitores["candidatos"][0]["votos"])+" votos")
            print ("|     2º lugar: "+dataEleitores["candidatos"][1]["nome"]+" com "+str(dataEleitores["candidatos"][1]["votos"])+" votos")
            print ("|     3º lugar: "+dataEleitores["candidatos"][2]["nome"]+" com "+str(dataEleitores["candidatos"][2]["votos"])+" votos")
            print ("========================================================")
            print ("")
            print ("")

            print ("Encerrando conexões com os hosts conectados...")
            mensagem_encerramento = "Votação encerrada.\n"

            for client_connection in client_connections:
                client_connection.send(mensagem_encerramento.encode())
                client_connection.close()

            print ("Conexões encerradas com sucesso!")
            break
            





def handle_client(client_socket):
    dataEleitores = json.load(open("dados.json"))
    verificado = False
    votou = False
    usuario = ""
    senha = ""

    while True:
        data = client_socket.recv(1024).decode()

        print (data)
        dataSeparada = data.split(" ")
        if dataSeparada[0] == "usuario":
            usuario = dataSeparada[1]
            client_socket.send("Agora digite sua senha".encode())
        elif dataSeparada[0] == "senha":
            senha = dataSeparada[1]
            for eleitor in dataEleitores["eleitores"]:
                if eleitor["usuario"] == usuario and eleitor["senha"] == senha:
                    if eleitor["votou"] == "True":
                        client_socket.send("Você já votou, encerrando conexão".encode())
                        break
                    verificado = True
            if verificado:
                client_socket.send(str(dataEleitores["candidatos"]).encode())
            else:
                client_socket.send("Usuário ou senha incorretos, encerrando conexão".encode())
                break
        elif dataSeparada[0] == "numero":
            numero = int(dataSeparada[1])
            for candidato in dataEleitores["candidatos"]:
                if candidato["numero"] == numero:
                    candidato["votos"] += 1
                    salve_json(dataEleitores, "dados.json")
                    votou = True
                    break
            if votou:
                client_socket.send("Voto computado com sucesso!".encode())
                for eleitor in dataEleitores["eleitores"]:
                    if eleitor["usuario"] == usuario and eleitor["senha"] == senha:
                        eleitor["votou"] = "True"
                        salve_json(dataEleitores, "dados.json")
                        break
                break
            else:
                client_socket.send("Número de candidato inválido, encerrando conexão".encode())
                break


    client_socket.close()

def admin_send_message():
    global admin_message
    while True:
        if votacao_iniciada:
            admin_input = input("Quando quiser mandar um aviso para todos os hosts conectados, é só digitar:")
            if admin_input:
                admin_message = f"aviso {admin_input}"
                for client_connection in client_connections:
                    try:
                        client_connection.send(admin_message.encode())
                    except:
                        pass



# Inicie a thread para que o administrador envie mensagens de aviso
admin_message_thread = threading.Thread(target=admin_send_message)
admin_message_thread.daemon = True
admin_message_thread.start()

votacao_encerrada_thread = threading.Thread(target=encerrar_votacao)
votacao_encerrada_thread.daemon = True
votacao_encerrada_thread.start()


while True:
    print("")
    print("")
    print("==================================")
    print("1 - Ver candidatos cadastrados")
    print("2 - Ver eleitores cadastrados")
    print("3 - Cadastrar candidato")
    print("4 - Cadastrar eleitor")
    print("5 - Iniciar votação")
    print("==================================")
    print("")

    opcao = int(input("Digite a opção desejada: "))

    if opcao == 1:
        for candidato in data["candidatos"]:
            print("")
            print("Numero: "+str(candidato["numero"]))
            print("Nome: "+ candidato["nome"])
            print("Quantidade de Votos: "+ str(candidato["votos"]))
            print("")

    elif opcao == 2:
        for eleitor in data["eleitores"]:
            print("")
            print("Nome: "+eleitor["nome"])
            print("Usuario: "+eleitor["usuario"])
            print("Senha: "+eleitor["senha"])
            print("")

    elif opcao == 3:
        novo_candidato = {
            "numero": int(input("Digite o número do candidato: ")),
            "nome": input("Digite o nome do candidato: "),
            "votos": 0
        }
        data["candidatos"].append(novo_candidato)
        salve_json(data, "dados.json")
        print("")
        print("==================================")
        print("Candidato cadastrado com sucesso!")
        print("==================================")
        print("")

    elif opcao == 4:
        novo_eleitor = {
            "nome": input("Digite o nome do eleitor: "),
            "usuario": input("Digite o usuário do eleitor: "),
            "senha": input("Digite a senha do eleitor: "),
            "votou": "False"
        }
        data["eleitores"].append(novo_eleitor)
        salve_json(data, "dados.json")
        print("")
        print("==================================")
        print("Eleitor cadastrado com sucesso!")
        print("==================================")
        print("")

    elif opcao == 5:
        votacao_iniciada = True
        print("")
        print("==================================")
        print("Iniciando votação...")
        print("==================================")
        print("")

        host = 'localhost'
        porta = 5000

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, porta))
        server_socket.listen(5)

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Conexão estabelecida com {client_address}")

            # Adicione o socket do cliente à lista de conexões
            client_connections.append(client_socket)

            # Crie uma nova thread para lidar com o cliente
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()