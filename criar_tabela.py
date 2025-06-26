import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('Calango.db')
    cursor = conn.cursor()
    aux = (
        'CREATE TABLE saldo ('+
        'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'+
        'chatid TEXT NOT NULL,'+
        'data DATE NOT NULL,'+
        'valor TEXT);'
    )
    try:
        cursor.execute(aux)
        conn.commit()
        conn.close()
        print('Tabela criada')
    except sqlite3.OperationalError as erro:
        if 'already exists' in str(erro):
            print('Tabela já existe')
