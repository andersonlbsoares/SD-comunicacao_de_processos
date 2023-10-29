import socket
import threading


def main():
    # Configuração do cliente
    host = 'localhost'
    porta = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, porta))

    resposta = ""
    
    while True:
       
        if resposta == "":
            print("Bem vindo ao sistema de votação! :)")
            print("")
            usuario = input("Digite o seu usuário: ")
            usuario = "usuario "+ usuario
            client_socket.send(usuario.encode())
        
        elif resposta == "Agora digite sua senha":
            senha = input("Digite sua senha: ")
            senha = "senha "+senha
            client_socket.send(senha.encode())

        elif resposta[0] == "[":
            lista_de_dados = eval(resposta)
            print("")
            print("Você está apto a votar! :)")
            print("")
            print("==================================")
            print("Candidatos:")
            for candidato in lista_de_dados:
                print (str(candidato['numero']) + " -> " + str(candidato['nome']))
            print("==================================")
            print("")

            numero = input("Digite o número do candidato: ")
            numero = "numero "+numero
            client_socket.send(numero.encode())

        elif resposta == "Você já votou, encerrando conexão":
            print("Você já votou, encerrando conexão")
            client_socket.close()
            break

        elif resposta == "Voto computado com sucesso!":
            print("Obrigado por votar! :)")
            client_socket.close()
            break

        elif resposta.startswith("aviso"):
            print ("")
            print ("")
            print ("=======================AVISO=======================")
            print("|     "+ resposta[6:]+"     |")
            print("===================================================")
            print ("")
            print ("")
            
            resposta = ""

        else:
            print("Erro de comunicação com o servidor")
            client_socket.close()
            break
        
        try:
            resposta = client_socket.recv(1024).decode()
            if resposta[0] != "[":
                print(resposta)
        except:
            print("Aguardando resposta do servidor...")
if __name__ == '__main__':
    main()