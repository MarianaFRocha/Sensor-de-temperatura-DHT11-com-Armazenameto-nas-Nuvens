# Carrega as bibliotecas
import pyodbc
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import MySQLdb as mariadb

mariadb_connection = mariadb.connect(user='root', passwd='*****', db='bancoTeste')
cursor = mariadb_connection.cursor()

server = 'nome_do_servidor'
database = 'nome_do_banco'
username = 'nome_usuario'
password = '****'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';51333;DATABASE='+database+';UID='+username+';PWD='+ password)
cursorserver = cnxn.cursor()


# Define o tipo de sensor
sensor = Adafruit_DHT.DHT11
 
GPIO.setmode(GPIO.BOARD)
 
# Define a GPIO conectada ao pino de dados do sensor
pino_sensor = 4
 

# Informações iniciais
print ("*** Lendo os valores de temperatura e umidade");

while(1):
   # Efetua a leitura do sensor
   umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor);
   # Caso leitura esteja ok, mostra os valores na tela
   if umid is not None and temp is not None:
     print ("Temperatura = {0:0.1f}  Umidade = {1:0.1f}n").format(temp, umid);
     print ("Aguarda 1 segundos para efetuar nova leitura...n");
     
     try:
        cursor.execute("INSERT into tabelaTeste(temp, umi) values(" + str(temp) + "," + str(umid) +")")
        mariadb_connection.commit()
    	  cursorserver.execute("INSERT INTO dbo.dados (temp, umid) values ("+str(temp)+","+str(umid)+")")
    	  cursorserver.commit()
     except mariadb.Error as e:
        print(e)
     time.sleep(1)
   else:
     # Mensagem de erro de comunicação com o sensor
     print("Falha ao ler dados do DHT11 !!!")
cursor.close()
