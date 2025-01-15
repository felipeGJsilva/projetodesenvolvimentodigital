import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect("maquinario.db")
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS grupos (
        codigo TEXT PRIMARY KEY,
        codigo_identifica TEXT,
        placa TEXT,
        nome TEXT NOT NULL,
        marcas TEXT NOT NULL,
        modelos TEXT NOT NULL,
        ano TEXT NOT NULL,
        status TEXT
    )
''')

def cadastrar_grupo():
    """
    Função para cadastrar um novo grupo de maquinário no banco de dados.
    """
    print("\n--- Cadastro de Grupo ---")
    codigo = input("Digite o código do grupo (ex: 1.21): ").strip()
    codigo_identifica = input("Digite o código de identificação do maquinário (ex: SCL-81): ").strip()
    placa = input("Digite a placa do veículo (opcional): ").strip()
    nome = input("Digite o nome do grupo (ex: Trator): ").strip()
    marcas = input("Digite as marcas associadas ao grupo (ex: John Deere): ").strip()
    modelos = input("Digite os modelos associados ao grupo (ex: 5055E): ").strip()
    ano = input("Digite o ano de fabricação (ex: 2023): ").strip()
    status = input("Digite o status do grupo (ex: ativo, inativo): ").strip()

    # Validar entradas obrigatórias
    if not codigo or not nome or not marcas or not modelos or not ano:
        print("Erro: Código, nome, marcas, modelos e ano são obrigatórios.")
        return

    # Verificar se o código já existe no banco
    cursor.execute("SELECT codigo FROM grupos WHERE codigo = ?", (codigo,))
    if cursor.fetchone():
        print("Erro: Código já cadastrado.")
        return

    # Inserir dados na tabela
    cursor.execute('''
        INSERT INTO grupos (codigo, codigo_identifica, placa, nome, marcas, modelos, ano, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (codigo, codigo_identifica, placa, nome, marcas, modelos, ano, status))
    conn.commit()
    print(f"Grupo '{nome}' com código '{codigo}' cadastrado com sucesso!")

def exibir_grupos():
    """
    Função para exibir os grupos cadastrados no banco de dados.
    """
    print("\n--- Grupos Cadastrados ---")
    cursor.execute("SELECT codigo, codigo_identifica, nome, marcas, modelos, ano, status FROM grupos")
    grupos = cursor.fetchall()

    if not grupos:
        print("Nenhum grupo cadastrado ainda.")
    else:
        for codigo, codigo_identifica, nome, marcas, modelos, ano, status in grupos:
            print(
                f"Código: {codigo} | Código de Identificação: {codigo_identifica or 'N/A'} | "
                f"Nome: {nome} | Marcas: {marcas} | Modelos: {modelos} | "
                f"Ano: {ano} | Status: {status or 'N/A'}"
            )

def menu():
    """
    Menu principal do programa.
    """
    while True:
        print("\n--- Menu ---")
        print("1. Cadastrar Grupo")
        print("2. Exibir Grupos")
        print("3. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_grupo()
        elif opcao == "2":
            exibir_grupos()
        elif opcao == "3":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Iniciar o programa
menu()

# Fechar a conexão com o banco de dados ao sair
conn.close()
