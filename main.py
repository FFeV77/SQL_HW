import psycopg2

def create_db(conn):
    '''Создание БД clients'''
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(30) NOT NULL,
                last_name VARCHAR(30) NOT NULL,
                email VARCHAR(400) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS phone(
                number VARCHAR(16) NOT NULL,
                client_id INT NOT NULL REFERENCES client(id) ON DELETE CASCADE,
                CONSTRAINT pk_phone PRIMARY KEY(number, client_id)
            );
            ''')

def add_client(conn, first_name:str, last_name:str, email:str, phones:list=None):
    '''Добавление нового клиента в БД, список телефонов опционально'''
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO client(first_name, last_name, email)
            VALUES
            (%s, %s, %s) RETURNING id;
            ''', (first_name, last_name, email))
        client_id = cur.fetchone()
        if phones != None:
            for phone in phones:
                add_phone(conn, client_id, phone)
    return client_id

def add_phone(conn, client_id:int, phone:str):
    '''Добавление телефона к существующему в БД клиенту'''
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO phone(client_id, number)
            VALUES(%s, %s);
            ''', (client_id, phone))
    return

def change_client(conn, client_id:int, first_name:str=None, last_name:str=None, email:str=None, phones:list=None):
    '''Изменение данных существующего в БД клиента'''
    execute=[]
    if first_name != None:
        execute += [f"first_name = '{first_name}'"]
    if last_name != None:
        execute += [f"last_name = '{last_name}'"]
    if email != None:
        execute += [f"email = '{email}'"]
    set = ', '.join(execute)
    with conn.cursor() as cur:
        cur.execute('''
            UPDATE client SET ''' + set + ''' 
            WHERE id=%s;''', (client_id, ))
    if phones != None:
        for phone in phones:
            add_phone(conn, client_id, phone)
    return

def delete_phone(conn, client_id:int, phone:str):
    '''Удаление телефона у существующего клиента'''
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM phone 
            WHERE client_id=%s AND number=%s;
            ''', (client_id, phone))

def delete_client(conn, client_id:int):
    '''Удаление клиента и связанных записей'''
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM client
            WHERE id=%s;
            ''', (client_id,))

def find_client(conn, first_name:str=None, last_name:str=None, email:str=None, phone:str=None):
    '''Поиск по БД клиента, возвращает список данных клиента'''
    execute=[]
    if first_name != None:
        execute += [f"first_name = '{first_name}'"]
    if last_name != None:
        execute += [f"last_name = '{last_name}'"]
    if email != None:
        execute += [f"email = '{email}'"]
    if phone != None:
        execute += [f"number = '{phone}'"]
    where = ' AND '.join(execute)
    with conn.cursor() as cur:
        cur.execute('''
            SELECT DISTINCT c.id, c.first_name, c.last_name, c.email FROM client c
            LEFT JOIN phone p ON c.id=p.client_id
            WHERE ''' + where)
        client = cur.fetchone()
    return client


with psycopg2.connect(database="client", user="postgres", password="postgres") as conn:
    #create_db(conn) #Создаем БД
    #print(add_client(conn, '3', '1', 'test.ru', ('000000000', '03', 'test-555-test'))) #Добавляем клиента
    #add_phone(conn, 2, '911') #Добавляем телефон клиенту
    #delete_phone(conn, 2, '911') #Удаляем телефон клиента
    #print(find_client(conn, email = 'test.ru')) #Находим клиента
    #change_client(conn, '2', '3', '3', email = 'test@kjhj.ru', phones = ['3456', '00098765']) #Меняем данные клиента
    #delete_client(conn, 2)