import sqlite3

# Conexão com o banco de dados de maquinários
conn_maquinarios = sqlite3.connect("maquinario.db")
cursor_maquinarios = conn_maquinarios.cursor()

# Criar tabela de maquinários se não existir
cursor_maquinarios.execute('''
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

# Conexão com o banco de dados de horímetros
conn_horimetros = sqlite3.connect("horimetros.db")
cursor_horimetros = conn_horimetros.cursor()

# Criar tabela de horímetros se não existir
cursor_horimetros.execute('''
    CREATE TABLE IF NOT EXISTS horimetros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_identifica TEXT NOT NULL,
        mes TEXT NOT NULL,
        inicio_horimetro REAL NOT NULL,
        final_horimetro REAL NOT NULL,
        kmhs REAL NOT NULL,
        litros REAL NOT NULL,
        media REAL NOT NULL,
        FOREIGN KEY (codigo_identifica) REFERENCES maquinarios (codigo_identifica)
    )
''')

# Função para cadastrar maquinário
def cadastrar_maquinario():
    print("\n--- Cadastro de Maquinário ---")
    codigo = input("Digite o código do maquinário (ex: 1.21): ").strip()
    codigo_identifica = input("Digite o código de identificação (ex: SCL-81): ").strip()
    placa = input("Digite a placa do veículo (opcional): ").strip()
    nome = input("Digite o nome do maquinário (ex: Trator): ").strip()
    marcas = input("Digite as marcas associadas (ex: John Deere): ").strip()
    modelos = input("Digite os modelos associados (ex: 5055E): ").strip()
    ano = input("Digite o ano de fabricação (ex: 2023): ").strip()
    status = input("Digite o status (ex: ativo, inativo): ").strip()

    if not codigo or not codigo_identifica or not nome or not marcas or not modelos or not ano:
        print("Erro: Campos obrigatórios não podem estar vazios.")
        return

    cursor_maquinarios.execute("SELECT codigo FROM maquinarios WHERE codigo = ?", (codigo,))
    if cursor_maquinarios.fetchone():
        print("Erro: Código já cadastrado.")
        return

    cursor_maquinarios.execute('''
        INSERT INTO maquinarios (codigo, codigo_identifica, placa, nome, marcas, modelos, ano, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (codigo, codigo_identifica, placa, nome, marcas, modelos, ano, status))
    conn_maquinarios.commit()
    print(f"Maquinário '{nome}' cadastrado com sucesso!")

# Função para registrar horímetro
def registrar_horimetro():
    print("\n--- Registro de Horímetro ---")
    codigo_identifica = input("Digite o código de identificação do maquinário: ").strip()

    cursor_maquinarios.execute("SELECT nome FROM maquinarios WHERE codigo_identifica = ?", (codigo_identifica,))
    maquinario = cursor_maquinarios.fetchone()

    if not maquinario:
        print("Erro: Código de identificação não encontrado.")
        return

    mes = input("Digite o mês de referência (ex: Janeiro): ").strip()
    try:
        inicio = float(input("Digite a marcação inicial do horímetro: "))
        final = float(input("Digite a marcação final do horímetro: "))
        kmhs = float(input("Digite a quantidade de km/h rodados: "))
        litros = float(input("Digite a quantidade de combustível em litros: "))

        if final < inicio:
            print("Erro: A marcação final não pode ser menor que a inicial.")
            return

        media = kmhs / litros
        cursor_horimetros.execute('''
            INSERT INTO horimetros (codigo_identifica, mes, inicio_horimetro, final_horimetro, kmhs, litros, media)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (codigo_identifica, mes, inicio, final, kmhs, litros, media))
        conn_horimetros.commit()
        print(f"Registro de horímetro para '{maquinario[0]}' adicionado com sucesso!")

    except ValueError:
        print("Erro: Valores inválidos. Use números para as marcações e consumos.")

# Função para exibir registros de horímetros
def exibir_horimetros():
    print("\n--- Registros de Horímetros ---")
    cursor_horimetros.execute('''
        SELECT h.codigo_identifica, m.nome, h.mes, h.inicio_horimetro, h.final_horimetro, 
               h.kmhs, h.litros, h.media
        FROM horimetros h
        JOIN maquinarios m ON h.codigo_identifica = m.codigo_identifica
    ''')
    registros = cursor_horimetros.fetchall()

    if not registros:
        print("Nenhum registro de horímetro encontrado.")
    else:
        for reg in registros:
            print(f"Código: {reg[0]} | Nome: {reg[1]} | Mês: {reg[2]} | Início: {reg[3]} | Final: {reg[4]} | "
                  f"Km/h: {reg[5]} | Litros: {reg[6]} | Média: {reg[7]:.2f}")

# Menu principal
def menu():
    while True:
        print("\n--- Menu Principal ---")
        print("1. Cadastrar Maquinário")
        print("2. Registrar Horímetro")
        print("3. Exibir Registros de Horímetros")
        print("4. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_maquinario()
        elif opcao == "2":
            registrar_horimetro()
        elif opcao == "3":
            exibir_horimetros()
        elif opcao == "4":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Executar o programa
menu()

# Fechar conexões com os bancos de dados
conn_maquinarios.close()
conn_horimetros.close()
