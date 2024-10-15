from abc import ABC, abstractmethod
import mysql.connector
from pymongo import MongoClient
import oracledb  # Atualizado de cx_Oracle para oracledb

# Interface de banco de dados
class DatabaseInterface(ABC):
    
    @abstractmethod
    def connect(self, config):
        pass
    
    @abstractmethod
    def execute_query(self, query, params=None):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass

# Implementação MySQL
class MySQLDatabase(DatabaseInterface):
    
    def __init__(self):
        self.connection = None
    
    def connect(self, config):
        self.connection = mysql.connector.connect(**config)
        # verificar se a conexão foi bem-sucedida
        if self.connection.is_connected():
            print("Conexão bem-sucedida ao MySQL")
        else:
            print("Erro na conexão ao MySQL")
            exit(1)
     
    
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)

        # Verifica se a query é um SELECT ou outra query que retorna resultados
        if cursor.with_rows:
            result = cursor.fetchall()  # Consome todos os resultados
        else:
            result = None  # ou outra ação apropriada

        self.connection.commit()  # Apenas após consumir os resultados

        cursor.close()  # Fechar o cursor após o uso
        return result
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Desconectado do MySQL")

# Implementação MongoDB
class MongoDBDatabase(DatabaseInterface):
    
    def __init__(self):
        self.connection = None
        self.db = None
    
    def connect(self, config):
        self.connection = MongoClient(config['host'], config['port'])
        self.db = self.connection[config['database']]
        print("Conectado ao MongoDB")
    
    def execute_query(self, query, params=None):
        # Para MongoDB, query pode ser uma string representando a coleção e params um filtro
         # Verifica se a query é um SELECT ou outra query que retorna resultados
        if query.startswith('SELECT') or query.startswith('SHOW'):
            result = self.db[query].find(params)
            # Consome todos os resultados
            result = list(result)
        else:
            # Para outras operações, como INSERT, UPDATE, DELETE, etc.
            result = self.db[query].update_one(params, {"$set": params})
            # Consome todos os resultados
            result = list(result)


        collection = self.db[query]
        return collection.find(params)
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Desconectado do MongoDB")

# Implementação Oracle com oracledb
class OracleDatabase(DatabaseInterface):
    
    def __init__(self):
        self.connection = None
    
    def connect(self, config):
        # Usando a nova biblioteca oracledb para criar a conexão
        self.connection = oracledb.connect(
            user=config['user'], 
            password=config['password'], 
            dsn=f"{config['host']}:{config['port']}/{config['sid']}"
        )
        print("Conectado ao Oracle")
    
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)

        # Verifica se a query é um SELECT ou outra query que retorna resultados
        if cursor.with_rows:
            result = cursor.fetchall()  # Consome todos os resultados
        else:
            result = None  # ou outra ação apropriada
            

        self.connection.commit()
        return cursor.fetchall()
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Desconectado do Oracle")

# Classe Genérica que escolhe o banco de dados
class GenericDatabase:
    
    def __init__(self, db_type, config):
        self.db = None
        if db_type == 'mysql':
            self.db = MySQLDatabase()
        elif db_type == 'mongodb':
            self.db = MongoDBDatabase()
        elif db_type == 'oracle':
            self.db = OracleDatabase()
        else:
            raise ValueError(f"Tipo de banco de dados {db_type} não suportado.")
        
        self.db.connect(config)
    
    def execute(self, query, params=None):
        return self.db.execute_query(query, params)
    
    def close(self):
        self.db.disconnect()

