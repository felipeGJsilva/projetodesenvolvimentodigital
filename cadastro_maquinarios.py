import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect("maquinario.db")
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS maquinarios (
        codigo TEXT PRIMARY KEY,
        codigo_identifica TEXT NOT NULL,
        placa TEXT,
        nome TEXT NOT NULL,
        marcas TEXT NOT NULL,
        modelos TEXT NOT NULL,
        ano TEXT NOT NULL,
        status TEXT
    )
''')

def cadastrar_maquinario():
    """
    Função para cadastrar um novo maquinário no banco de dados.
    """
    print("\n--- Cadastro de Maquinário ---")
    codigo = input("Digite o código do maquinário (ex: 1.21): ").strip()
    codigo_identifica = input("Digite o código de identificação do maquinário (ex: SCL-81): ").strip()
    placa = input("Digite a placa do veículo (opcional): ").strip()
    nome = input("Digite o nome do maquinário (ex: Trator): ").strip()
    marcas = input("Digite as marcas associadas ao maquinário (ex: John Deere): ").strip()
    modelos = input("Digite os modelos do maquinário (ex: 5055E): ").strip()
    ano = input("Digite o ano de fabricação (ex: 2023): ").strip()
    status = input("Digite o status do maquinário (ex: ativo, inativo): ").strip()

    # Validar entradas obrigatórias
    if not codigo or not codigo_identifica or not nome or not marcas or not modelos or not ano:
        print("Erro: Código, código de identificação, nome, marcas, modelos e ano são obrigatórios.")
        return

    # Verificar se o código já existe no banco
    cursor.execute("SELECT codigo FROM maquinarios WHERE codigo = ?", (codigo,))
    if cursor.fetchone():
        print("Erro: Código já cadastrado.")
        return

    # Inserir dados na tabela
    cursor.execute('''
        INSERT INTO maquinarios (codigo, codigo_identifica, placa, nome, marcas, modelos, ano, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (codigo, codigo_identifica, placa, nome, marcas, modelos, ano, status))
    conn.commit()
    print(f"Maquinário '{nome}' com código '{codigo}' cadastrado com sucesso!")

def exibir_maquinarios():
    """
    Função para exibir os maquinários cadastrados no banco de dados.
    """
    print("\n--- Maquinários Cadastrados ---")
    cursor.execute("SELECT codigo, codigo_identifica, nome, marcas, modelos, ano, status FROM maquinarios")
    maquinarios = cursor.fetchall()

    if not maquinarios:
        print("Nenhum maquinário cadastrado ainda.")
    else:
        for codigo, codigo_identifica, nome, marcas, modelos, ano, status in maquinarios:
            print(
                f"Código: {codigo} | Código de Identificação: {codigo_identifica} | "
                f"Nome: {nome} | Marcas: {marcas} | Modelos: {modelos} | "
                f"Ano: {ano} | Status: {status or 'N/A'}"
            )

def menu():
    """
    Menu principal do programa.
    """
    while True:
        print("\n--- Menu ---")
        print("1. Cadastrar Maquinário")
        print("2. Exibir Maquinários")
        print("3. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_maquinario()
        elif opcao == "2":
            exibir_maquinarios()
        elif opcao == "3":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Iniciar o programa
menu()

# Fechar a conexão com o banco de dados ao sair
conn.close()
