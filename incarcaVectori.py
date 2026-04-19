import os
import pandas as pd
import oracledb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

#Incarca datele de conectare din fișierul .env (user, parola, dsn)
load_dotenv()
utilizator = os.getenv("user_db")
parola = os.getenv("parola_db")
adresa_db = os.getenv("dsn_db")
model_ai = SentenceTransformer('all-MiniLM-L6-v2')

#Deschide fisierul de date
date = pd.read_csv('data/articole.csv', sep=';')

#Conectare la db
conexiune = oracledb.connect(user=utilizator, password=parola, dsn=adresa_db)
cursor = conexiune.cursor()


#Transformarea datelor in vectori si incarcarea in db
for index, rand in date.iterrows():
    text_articol = str(rand['abstract'])
    vector_numere = model_ai.encode(text_articol).tolist()
    comanda_sql = "INSERT INTO articole_stiintifice (titlu, abstract, abstract_vector) VALUES (:1, :2, :3)"
    cursor.execute(comanda_sql, [rand['titlu'], text_articol, str(vector_numere)])

#Salvarea modificarilor si inchiderea conexiunii
conexiune.commit()
cursor.close()
conexiune.close()

print("Articole incarcate cu succes")