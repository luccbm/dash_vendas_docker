import os
import random
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine, text

def popular_banco():
    db_user = os.environ.get("DB_USER", "usuario")
    db_pass = os.environ.get("DB_PASSWORD", "senha123")
    db_host = os.environ.get("DB_HOST", "db")
    db_name = os.environ.get("DB_NAME", "vendas_db")

    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:5432/{db_name}")

    # Cria a tabela de vendas
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS vendas (
                id SERIAL PRIMARY KEY,
                data TIMESTAMP NOT NULL,
                produto VARCHAR(50) NOT NULL,
                categoria VARCHAR(50) NOT NULL,
                valor FLOAT NOT NULL,
                quantidade INT NOT NULL
            );
        """))
        conn.commit()

        # Checa se já existem dados
        result = conn.execute(text("SELECT COUNT(*) FROM vendas;")).scalar()
        if result == 0:
            categorias_produtos = {
                "Eletrônicos": ["Notebook", "Smartphone", "Fone de Ouvido", "Monitor"],
                "Vestuário": ["Camiseta", "Calça Jeans", "Tênis", "Jaqueta"],
                "Higiene": ["Shampoo", "Sabonete", "Protetor Solar", "Creme Dental"]
            }

            dados = []
            data_inicial = datetime.now() - timedelta(days=30)

            for _ in range(100):
                categoria = random.choice(list(categorias_produtos.keys()))
                produto = random.choice(categorias_produtos[categoria])
                valor = round(random.uniform(20.0, 1500.0), 2)
                quantidade = random.randint(1, 5)
                data_venda = data_inicial + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))

                dados.append({
                    "data": data_venda,
                    "produto": produto,
                    "categoria": categoria,
                    "valor": valor,
                    "quantidade": quantidade
                })

            df = pd.DataFrame(dados)
            df.to_sql("vendas", engine, if_exists="append", index=False)
            print("Banco popular com 100 vendas fictícias com sucesso!")

if __name__ == "__main__":
    popular_banco()