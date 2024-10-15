from abc import ABC, abstractmethod
import mysql.connector
from pymongo import MongoClient
import cx_Oracle

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
        print("Conectado ao MySQL")
    
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor.fetchall()
    
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
        collection = self.db[query]
        return collection.find(params)
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Desconectado do MongoDB")

# Implementação Oracle
class OracleDatabase(DatabaseInterface):
    
    def __init__(self):
        self.connection = None
    
    def connect(self, config):
        dsn = cx_Oracle.makedsn(config['host'], config['port'], sid=config['sid'])
        self.connection = cx_Oracle.connect(config['user'], config['password'], dsn)
        print("Conectado ao Oracle")
    
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
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


