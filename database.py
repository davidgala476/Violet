import sqlite3

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('postal_ch.db')
        return conn
    except sqlite3.Error as e:
        print(f"No se pudo conectar: {e}")
    return conn

def create_tables(conn):

    sql_create_dolls_table = """
    CREATE TABLE IF NOT EXISTS dolls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER,
        estado TEXT NOT NULL CHECK(estado IN ('activo', 'inactivo')),
        cartas_escritas INTEGER DEFAULT 0,
        cartas_en_proceso INTEGER DEFAULT 0
    );
    """

    sql_create_clientes_table = """
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        ciudad TEXT,
        motivo_carta TEXT,
        contacto TEXT
    );
    """

    sql_create_cartas_table = """
    CREATE TABLE IF NOT EXISTS cartas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        doll_id INTEGER NOT NULL,
        fecha_creacion TEXT DEFAULT CURRENT_DATE,
        estado TEXT NOT NULL CHECK(estado IN ('borrador', 'revisado', 'enviado')) DEFAULT 'borrador',
        contenido TEXT,
        resumen TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
        FOREIGN KEY (doll_id) REFERENCES dolls (id)
    );
    """

    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_dolls_table)
        cursor.execute(sql_create_clientes_table)
        cursor.execute(sql_create_cartas_table)
        conn.commit()
        print(" Base de datos creada")
        print("    Tabla 'dolls' correcto")
        print("    'clientes' correcto")
        print("    'cartas' correcto.")
    except sqlite3.Error as e:
        print(f" Error al crear las tablas: {e}")

def insert_test_data(conn):

    dolls_data = [
        ('Violet Evergarden', 14, 'activo', 42, 2),
        ('Cattleya Baudelaire', 24, 'activo', 128, 1),
        ('Iris Cannary', 15, 'activo', 15, 4)
    ]
    
    clientes_data = [
        ('Leon Stephanotis', 'Leidenschaftlich', 'Oferta de FOTOJAPON', 'Estudio de Fotografía'),
        ('Oscar Webster', 'Lux', 'Amor', 'Casa de la Familia Webster'),
        ('Ann Magnolia', 'Leylat', 'Querida Mami', 'Calle Principal #123')
    ]
    
    cartas_data = [
        (1, 1, 'enviado', 'Estimado Sr. Stephanotis, agradecemos su interés en nuestros servicios de fotografía FOTOJAPON pronto le haremos conocer nuestros servicios por medio de una nueva carta. Buen dia', 'Respuesta formal a consulta comercial'),
        (2, 2, 'revisado', 'Mi querida Eleanor, cada día que pasa pienso en el amor que una vez compartimos sin importar lo que fuera yo me enamore de ti desde esa vez que te vi cerca al aeropuerto', 'Carta de amor y reconciliación'),
        (3, 3, 'borrador', 'Querida mamá, espero que estes bien. He estado estudiando mucho en la universidad de Alemania pronto te mandare otra carta con un nuevo regalo. Te amo Mucho ma besos', 'Carta familiar de actualización')
    ]
    
    try:
        cursor = conn.cursor()
        
        cursor.executemany('''INSERT INTO dolls (nombre, edad, estado, cartas_escritas, cartas_en_proceso)
                           VALUES (?, ?, ?, ?, ?)''', dolls_data)
        
        cursor.executemany('''INSERT INTO clientes (nombre, ciudad, motivo_carta, contacto)
                           VALUES (?, ?, ?, ?)''', clientes_data)
        
        cursor.executemany('''INSERT INTO cartas (cliente_id, doll_id, estado, contenido, resumen)
                           VALUES (?, ?, ?, ?, ?)''', cartas_data)
        
        conn.commit()
        print(" Datos insertados de prueba")
        print("   - Hay 3 Auto Memory Dolls creadas")
        print("   - Hay 3 Clientes registrados")
        print("   - Hay 3 Cartas escritas")

        print("\n Resumen:")
        
        cursor.execute("SELECT * FROM dolls")
        dolls = cursor.fetchall()
        print("\nAuto Memory Dolls:")
        for doll in dolls:
            print(f"   ID: {doll[0]}, Nombre: {doll[1]}, Estado: {doll[3]}, Cartas: {doll[4]}")
        
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        print("\nClientes:")
        for cliente in clientes:
            print(f"   ID: {cliente[0]}, Nombre: {cliente[1]}, Ciudad: {cliente[2]}")
        
        cursor.execute("""SELECT c.id, cl.nombre, d.nombre, c.estado, c.resumen 
                       FROM cartas c 
                       JOIN clientes cl ON c.cliente_id = cl.id 
                       JOIN dolls d ON c.doll_id = d.id""")
        cartas = cursor.fetchall()
        print("\nCartas:")
        for carta in cartas:
            print(f"   ID: {carta[0]}, Cliente: {carta[1]}, Doll: {carta[2]}, Estado: {carta[3]}")
            
    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")

def main():

    print("Compañía Postal CH...")
    conn = create_connection()
    
    if conn is not None:
        create_tables(conn)
        
        print("\nInsertando datos de prueba de Violet Evergarden...")
        insert_test_data(conn)
        
        conn.close()
        print("\n Base de datos configurada correctamente. Archivo: 'postal_ch.db'")
        print("\n ")
        print("   - Violet Evergarden ")
        print("   - Cattleya Baudelaire ")
        print("   - Iris Cannary ")
        print("   - Leon Stephanotis ")
        print("   - Oscar Webster ")
        print("   - Ann Magnolia ")
    else:
        print("Error: No se pudo crear la conexión a la base de datos.")

if __name__ == '__main__':
    main()
