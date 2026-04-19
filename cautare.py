import os
import oracledb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

#Incarca modelul AI si datele de conectare din fișierul .env (user, parola, dsn)
load_dotenv()
utilizator = os.getenv("user_db")
parola = os.getenv("parola_db")
adresa_db = os.getenv("dsn_db")
model_ai = SentenceTransformer('all-MiniLM-L6-v2')

#Conectare la db
conexiune = oracledb.connect(user=utilizator, password=parola, dsn=adresa_db)
cursor = conexiune.cursor()


intrebare = input("Pune o intrebare: ")

#Transformăm intrebarea utilizatorului in vector
vector_intrebare = str(model_ai.encode(intrebare).tolist())

#Interogarea vector search
#Oracle calculează care articole sunt cele mai apropiate ca ințeles de intrebare
sql = """
select titlu, vector_distance(abstract_vector, :v, COSINE) as distanta
from articole_stiintifice
order by distanta
fetch first 3 rows only
"""

print("\nCele mai relevante rezultate")
for rand in cursor.execute(sql, v=vector_intrebare):
    #Cu cat distanta e mai mica, cu atat articolul e mai relevant
    print(f"-> Titlu: {rand[0]} (Scor relevanta: {rand[1]:.4f})")

#Inchidere conexiunea
cursor.close()
conexiune.close()