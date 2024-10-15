
# Generic Database Connector

Este projeto fornece uma classe genérica em Python para realizar ações em diferentes tipos de bancos de dados, como MySQL, MongoDB e Oracle. A classe permite a conexão, execução de queries e desconexão dos bancos de forma abstrata, facilitando o uso de múltiplos tipos de bancos de dados com a mesma interface.

## Funcionalidades

- Conectar a bancos de dados MySQL, MongoDB e Oracle.
- Executar queries SQL (MySQL, Oracle) e comandos MongoDB.
- Desconectar automaticamente após a execução das operações.

## Requisitos

Antes de começar, certifique-se de ter as seguintes dependências instaladas no seu sistema:

- Python 3.7+
- MySQL Server (para conexão com MySQL)
- MongoDB Server (para conexão com MongoDB)
- Oracle Database (para conexão com Oracle)

## Instalação

1. Clone o repositório para sua máquina local:

   ```bash
   git clone https://github.com/seuusuario/generic-database-connector.git
   cd generic-database-connector


2. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

## Configuração

Cada tipo de banco de dados requer uma configuração específica. Você deve passar os parâmetros de conexão apropriados dependendo do banco de dados que deseja usar.

### MySQL

Para usar o MySQL, a configuração deve conter os seguintes parâmetros:

```python
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'testdb'
}
```

### MongoDB

Para MongoDB, a configuração deve conter os seguintes parâmetros:

```python
mongodb_config = {
    'host': 'localhost',
    'port': 27017,
    'database': 'testdb'
}
```

### Oracle

Para Oracle, a configuração deve conter os seguintes parâmetros:

```python
oracle_config = {
    'host': 'localhost',
    'port': 1521,
    'sid': 'orcl',
    'user': 'admin',
    'password': 'password'
}
```

## Exemplo de Uso

Aqui está um exemplo básico de como usar a classe genérica para conectar e executar uma query em diferentes bancos de dados.

### Usando MySQL:

#### **Consultando registros (SELECT):**

```python
from database import GenericDatabase

# Configuração para MySQL
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'testdb'
}

# Conectar e executar uma query
db = GenericDatabase('mysql', mysql_config)
result = db.execute("SELECT * FROM users")
print(result)
db.close()
```

#### **Inserindo um registro (INSERT):**

```python
from database import GenericDatabase

# Configuração para MySQL
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'testdb'
}

# Conectar ao MySQL
db = GenericDatabase('mysql', mysql_config)

# Executar um INSERT
insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
params = ("John Doe", "john.doe@example.com")
db.execute(insert_query, params)
print("Registro inserido com sucesso!")
db.close()
```

#### **Deletando um registro (DELETE):**

```python
from database import GenericDatabase

# Configuração para MySQL
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'testdb'
}

# Conectar ao MySQL
db = GenericDatabase('mysql', mysql_config)

# Executar um DELETE
delete_query = "DELETE FROM users WHERE email = %s"
params = ("john.doe@example.com",)
db.execute(delete_query, params)
print("Registro deletado com sucesso!")
db.close()
```

### Usando MongoDB:

#### **Consultando registros (SELECT):**

```python
from database import GenericDatabase

# Configuração para MongoDB
mongodb_config = {
    'host': 'localhost',
    'port': 27017,
    'database': 'testdb'
}

# Conectar e executar uma consulta
db = GenericDatabase('mongodb', mongodb_config)
result = db.execute('users', {'name': 'John'})
for doc in result:
    print(doc)
db.close()
```
#### **Inserindo um registro (INSERT):**

Em MongoDB, o método para inserção é ligeiramente diferente, já que usamos `insert_one` ou `insert_many` para inserir documentos.

```python
from database import GenericDatabase

# Configuração para MongoDB
mongodb_config = {
    'host': 'localhost',
    'port': 27017,
    'database': 'testdb'
}

# Conectar ao MongoDB
db = GenericDatabase('mongodb', mongodb_config)

# Executar um INSERT
insert_query = 'users'  # Nome da coleção
params = {"name": "John Doe", "email": "john.doe@example.com"}
db.execute(insert_query).insert_one(params)
print("Documento inserido com sucesso!")
db.close()
```

#### **Deletando um registro (DELETE):**

```python
from database import GenericDatabase

# Configuração para MongoDB
mongodb_config = {
    'host': 'localhost',
    'port': 27017,
    'database': 'testdb'
}

# Conectar ao MongoDB
db = GenericDatabase('mongodb', mongodb_config)

# Executar um DELETE
delete_query = 'users'  # Nome da coleção
params = {"email": "john.doe@example.com"}
db.execute(delete_query).delete_one(params)
print("Documento deletado com sucesso!")
db.close()
```

### Usando Oracle:
#### **Consultando registros (SELECT):**
```python
from database import GenericDatabase

# Configuração para Oracle
oracle_config = {
    'host': 'localhost',
    'port': 1521,
    'sid': 'orcl',  # Service ID (SID) do Oracle
    'user': 'admin',
    'password': 'password'
}

# Conectar e executar uma query
db = GenericDatabase('oracle', oracle_config)
result = db.execute("SELECT * FROM employees")
print(result)
db.close()
```

#### **Inserindo um registro (INSERT):**

```python
from database import GenericDatabase

# Configuração para Oracle
oracle_config = {
    'host': 'localhost',
    'port': 1521,
    'sid': 'orcl',
    'user': 'admin',
    'password': 'password'
}

# Conectar ao Oracle
db = GenericDatabase('oracle', oracle_config)

# Executar um INSERT
insert_query = "INSERT INTO employees (name, email) VALUES (:1, :2)"
params = ("John Doe", "john.doe@example.com")
db.execute(insert_query, params)
print("Registro inserido no Oracle com sucesso!")
db.close()
```

#### **Deletando um registro (DELETE):**

```python
from database import GenericDatabase

# Configuração para Oracle
oracle_config = {
    'host': 'localhost',
    'port': 1521,
    'sid': 'orcl',
    'user': 'admin',
    'password': 'password'
}

# Conectar ao Oracle
db = GenericDatabase('oracle', oracle_config)

# Executar um DELETE
delete_query = "DELETE FROM employees WHERE email = :1"
params = ("john.doe@example.com",)
db.execute(delete_query, params)
print("Registro deletado no Oracle com sucesso!")
db.close()
```


## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues para bugs e melhorias.


### **Explicação do `README.md`:**
- **Introdução e Funcionalidades:** Explicação clara do propósito do projeto.
- **Requisitos e Instalação:** Orientações para configurar o ambiente de desenvolvimento e instalar as dependências necessárias.
- **Configuração e Exemplo de Uso:** Exemplos claros de como usar a classe para conectar a MySQL, MongoDB e Oracle.
- **Contribuição e Licença:** Informações sobre como contribuir e a licença do projeto.

