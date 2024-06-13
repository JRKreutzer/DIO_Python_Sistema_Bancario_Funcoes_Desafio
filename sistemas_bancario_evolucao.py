import textwrap

# Função que imprime o menu principal
def menu():
    menu = '''\n
    {0:=^30}
    =={1:^26}==
    {0:=^30}

    Selecione uma opção:

    1. Depositar - Adicione fundos à sua conta.
    2. Sacar - Retire fundos da sua conta.
    3. Extrato - Verifique seu saldo atual.
    4. Criar Usuário - Adicione um novo cliente.
    5. Criar Conta - Adicone uma conta para um cliente.
    6. Listar Contas - Exibir uma lista de contas.
    0. Sair - Encerre o programa.

    Digite a opção escolhida: '''.format('', 'Menu Bancário')
    return input(textwrap.dedent(menu))

# Função que imprime o cabeçalho do extrato
def menu_extrato():
    menu_extrato = '''
    {0:=^30}
    =={1:^26}==
    {0:=^30}
    '''.format('', 'Extrato')
    return print(textwrap.dedent(menu_extrato))

# Função que faz as validações de depósito
def deposito(saldo, valor, extrato, /):
    if valor <= 0:
        print('Depósito não pode ser igual ou inferior a R$00,00, Tente novamente.')
    else:
        saldo += valor
        extrato += f'\nDepósito de R${valor:.2f} realizado com sucesso.\n'
        print(f'\nDepósito de R${valor:.2f} realizado com sucesso.\n')
        return saldo, extrato

# Função que faz as validações de saque
def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    
    # Verifica se o valor do saque é válido
    if valor <= 0:
        print('\nFalha ao realizar o saque, valores iguais ou menores que zero não são aceitos.\n')
    # Verifica se o valor do saque é maior que o valor em conta
    elif valor > saldo:
        print('\nFalha ao realizar o saque, verifique o seu saldo atual.\n')
    # Verifica se o valor do saque é maior que o limite da conta
    elif valor > limite:
        print('\nFalha ao realizar o saque, valor ultrapassou o limite.\n')
    # Verifica se o limite de saques não foi ultrapassado
    elif numero_saques == limite_saques:
        print('\nFalha ao realizar o saque, numeros de saques diários ultrapassado.\n')
    else:
        saldo -= valor
        numero_saques += 1
        extrato += f'\nSaque número {numero_saques} no valor de R${valor:.2f} realizado com sucesso.\n'
        print(f'\nSaque número {numero_saques} no valor de R${valor:.2f} realizado com sucesso.\n')
    return saldo, numero_saques, extrato

# Função que imprime o extrato
def tirar_extrato(saldo, /, *, extrato):
    menu_extrato()
    print('Não houve nenhum movimento na conta até o momento.\n') if not extrato else print(extrato + f'\nSaldo atual = R${saldo:.2f}\n')

# Função para verificar se existe algum usuário cadastrado com um cpf específico
def encontrar_usuario(cpf, usuarios):
    usuario_encontrado = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuario_encontrado if usuario_encontrado else None

# Função para criar um usuário e salva-lo numa lista de usuários
def criar_usuario(usuarios):
    cpf = input('\nDigite o CPF do cliente: ')
    usuario_ja_existe = encontrar_usuario(cpf, usuarios)
    if usuario_ja_existe:
        print('\nUsuário já cadastrado com esse CPF!\n')
        return
    nome = input('Digite o nome do cliente: ')
    data = input('Digite a data de nascimento do cliente: ')
    endereco = input('Digite o endereço do cliente: (Formato: logradouro, numero - Bairro - Cidade/Sigla Estado)')
    usuarios.append({'cpf': cpf, 'nome': nome, 'data': data, 'endereco': endereco})
    print(f'\nUsuário: {nome} cadastrado com sucesso!\n')

# Função para criar uma conta e salva-la numa lista de contas
def criar_conta(contas, usuarios, agencia, numero_conta):
    cpf = input('\nDigite o CPF do cliente: ')
    usuario_ja_existe = encontrar_usuario(cpf, usuarios)
    if not usuario_ja_existe:
        print('\nNenhum usuário cadastrado com esse CPF!\n')
    else:
        numero_conta += 1
        contas.append({'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario_ja_existe})
        print('\nConta criada com sucesso!\n')
    return numero_conta

# Função para imprimir uma lista de contas
def listar_contas(contas):
    if len(contas) == 0:
        print('Nenhuma conta cadastrada!')
        return
    for conta in contas:
        print(f'\nAgência: {conta['agencia']}, Número da conta: {conta['numero_conta']}, Usuário: {conta['usuario']}')

# Função principal que será chamada para iniciar o programa
def main():

    # Variável para armazenar o saldo da conta
    saldo = 0
    # Limite por saque é de R$ 500,00
    limite = 500
    # Variável para armazenar o extrato da conta
    extrato = ''
    # Contador para o número de saques realizados no dia
    numero_saques = 0
    # Lista para armazenar os usuários
    usuarios = []
    # Lista para armazenar contas
    contas = []
    # Contador de número de contas
    numero_conta = 0

    # Regra de negócio determina que o limite de saques diários seja de 3
    LIMITE_SAQUES = 3
    # Número da agência
    AGENCIA = '0001'

    # Loop principal do programa
    while True:

        # Solicita ao usuário que selecione uma opção do menu
        opcao = menu()

        # Opção 1: Depositar fundos na conta
        if opcao == '1':
            # Solicita ao usuário o valor a ser depositado
            valor = float(input('Digite o valor a ser depositado: '))

            saldo, extrato = deposito(saldo, valor, extrato)
            

        # Opção 2: Sacar fundos da conta
        elif opcao == '2':

            if saldo <= 0:
                print('\nOpção indisponível no momento, verifique seu saldo atual.\n')
            else:
                # Solicita ao usuário o valor a ser sacado
                valor = float(input('Digite o valor que deseja sacar: '))
            
                saldo, numero_saques, extrato = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)


        # Opção 3: Ver extrato e saldo atual
        elif opcao == '3':
            tirar_extrato(saldo, extrato=extrato)
        
        
        # Opção 4: Ver extrato e saldo atual
        elif opcao == '4':
            criar_usuario(usuarios)

        # Opção 5: Ver extrato e saldo atual
        elif opcao == '5':
            numero_conta = criar_conta(contas, usuarios, AGENCIA, numero_conta)

        # Opção 6: Ver extrato e saldo atual
        elif opcao == '6':
            listar_contas(contas)
            
        
        # Opção 0: Encerrar o programa
        elif opcao == '0':
            confirma = input('\nTem certeza que deseja sair? Digite [s] para sair ou qualquer outra tecla para voltar ao menu: ')
            # Confirmação de saída do programa
            if confirma == 's':
                break
            elif confirma == 'n':
                continue
        
        # Se a opção digitada pelo usuário for inválida, solicita que o usuário escolha novamente
        else:
            print('\nOperação inválida!')

main()
