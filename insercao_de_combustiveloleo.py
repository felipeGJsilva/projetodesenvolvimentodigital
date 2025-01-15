import sqlite3

# Conexão com os bancos de dados
# Conecta ao banco de dados dos maquinários e cria um novo para os horímetros.
conn_maquinarios = sqlite3.connect("maquinario.db")
conn_horimetros = sqlite3.connect("horimetros.db")
cursor_maquinarios = conn_maquinarios.cursor()
cursor_horimetros = conn_horimetros.cursor()

# Criar tabela no banco horimetros.db
# Cria a tabela 'horimetros' no banco horimetros.db, caso ainda não exista.
cursor_horimetros.execute('''
    CREATE TABLE IF NOT EXISTS horimetros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  # Identificador único para cada entrada
        codigo_identifica TEXT NOT NULL,      # Código do maquinário (chave estrangeira)
        mes TEXT NOT NULL,                    # Mês de referência
        inicio INTEGER NOT NULL,              # Marcação inicial do horímetro
        final INTEGER NOT NULL,               # Marcação final do horímetro
        kmhs INTEGER NOT NULL,                # Quilômetros rodados ou horas trabalhadas
        litros INTEGER NOT NULL,              # Combustível consumido
        media REAL NOT NULL,                  # Média de consumo (km/hs por litro)
        FOREIGN KEY (codigo_identifica) REFERENCES grupos (codigo_identifica)  # Relaciona com a tabela 'grupos'
    )
''')
conn_horimetros.commit()  # Confirma a criação da tabela

def adicionar_horimetro():
    """
    Função para adicionar dados mensais de um maquinário.
    """
    print("\n--- Adicionar Horímetro ---")
    codigo_identifica = input("Digite o código de identificação do maquinário: ").strip()

    # Verificar se o código existe no banco maquinario.db
    # Consulta no banco 'maquinario.db' para verificar se o código existe.
    cursor_maquinarios.execute("SELECT nome FROM grupos WHERE codigo_identifica = ?", (codigo_identifica,))
    maquinario = cursor_maquinarios.fetchone()

    if not maquinario:  # Se não encontrar o maquinário, exibe uma mensagem de erro.
        print("Erro: Código de identificação não encontrado.")
        return

    # Exibe o nome do maquinário encontrado.
    print(f"Maquinário encontrado: {maquinario[0]}")

    # Coleta os dados mensais do usuário.
    mes = input("Digite o mês de referência (ex: janeiro): ").strip().capitalize()
    inicio = int(input("Digite o valor inicial do horímetro: ").strip())
    final = int(input("Digite o valor final do horímetro: ").strip())
    kmhs = final - inicio  # Calcula os quilômetros rodados ou horas trabalhadas.
    litros = int(input("Digite a quantidade de litros consumidos: ").strip())
    media = kmhs / litros if litros > 0 else 0  # Calcula a média de consumo.

    # Insere os dados no banco horimetros.db
    cursor_horimetros.execute('''
        INSERT INTO horimetros (codigo_identifica, mes, inicio, final, kmhs, litros, media) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (codigo_identifica, mes, inicio, final, kmhs, litros, media))
    conn_horimetros.commit()  # Salva as alterações no banco.

    print(f"Dados de {mes} adicionados com sucesso para o maquinário '{maquinario[0]}'.")

def exibir_horimetros():
    """
    Função para exibir dados de horímetro de um maquinário.
    """
    print("\n--- Exibir Horímetros ---")
    codigo_identifica = input("Digite o código de identificação do maquinário: ").strip()

    # Verificar se o código existe no banco maquinario.db
    # Confere se o código de identificação está no banco 'maquinario.db'.
    cursor_maquinarios.execute("SELECT nome FROM grupos WHERE codigo_identifica = ?", (codigo_identifica,))
    maquinario = cursor_maquinarios.fetchone()

    if not maquinario:  # Caso o maquinário não exista, exibe uma mensagem.
        print("Erro: Código de identificação não encontrado.")
        return

    # Exibe o nome do maquinário encontrado.
    print(f"Horímetros registrados para o maquinário '{maquinario[0]}':")

    # Busca os dados de horímetro no banco horimetros.db
    cursor_horimetros.execute('''
        SELECT mes, inicio, final, kmhs, litros, media 
        FROM horimetros WHERE codigo_identifica = ?
    ''', (codigo_identifica,))
    registros = cursor_horimetros.fetchall()

    if not registros:  # Se não houver registros, informa o usuário.
        print("Nenhum registro encontrado.")
    else:  # Exibe cada registro encontrado.
        for mes, inicio, final, kmhs, litros, media in registros:
            print(
                f"Mês: {mes} | Início: {inicio} | Final: {final} | KM/HS: {kmhs} | "
                f"Litros: {litros} | Média: {media:.2f}"
            )

def menu():
    """
    Menu principal do programa.
    """
    while True:  # Loop para manter o menu ativo até o usuário decidir sair.
        print("\n--- Menu ---")
        print("1. Adicionar Horímetro")  # Opção para adicionar um novo registro de horímetro.
        print("2. Exibir Horímetros")    # Opção para visualizar os registros existentes.
        print("3. Sair")                 # Opção para sair do programa.

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_horimetro()  # Chama a função para adicionar horímetro.
        elif opcao == "2":
            exibir_horimetros()  # Chama a função para exibir horímetros.
        elif opcao == "3":
            print("Saindo do programa...")
            break  # Sai do loop e termina o programa.
        else:
            print("Opção inválida! Tente novamente.")  # Mensagem para opção inválida.

# Iniciar o programa
menu()

# Fechar conexões ao sair
conn_maquinarios.close()  # Fecha a conexão com o banco de maquinários.
conn_horimetros.close()   # Fecha a conexão com o banco de horímetros.
