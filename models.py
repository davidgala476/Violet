import sqlite3
from database import create_connection

class DollModel:

    @staticmethod
    def create(nombre, edad, estado):
        if not nombre or not estado:
            raise ValueError("Nombre y estado deben ser añadidos si o si")

        if estado not in ['activo', 'inactivo']:
            raise ValueError("Solo se permite 'activo' o 'inactivo'.")

        conn = create_connection()
        if conn is not None:
            try:
                sql = '''INSERT INTO dolls(nombre, edad, estado)
                         VALUES(?,?,?)'''
                cursor = conn.cursor()
                cursor.execute(sql, (nombre, edad, estado))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                print(f"No se creo Doll: {e}")
            finally:
                conn.close()
        return None

    @staticmethod
    def read_all():
        conn = create_connection()
        if conn is not None:
            try:
                sql = "SELECT * FROM dolls"
                cursor = conn.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"No se encontro la Doll: {e}")
            finally:
                conn.close()
        return []

    @staticmethod
    def read_by_id(doll_id):
        conn = create_connection()
        if conn is not None:
            try:
                sql = "SELECT * FROM dolls WHERE id = ?"
                cursor = conn.cursor()
                cursor.execute(sql, (doll_id,))
                return cursor.fetchone()
            except sqlite3.Error as e:
                print(f"No se encontro la Doll: {e}")
            finally:
                conn.close()
        return None

    @staticmethod
    def update(doll_id, **kwargs):
        if not kwargs:
            return False

        valid_fields = ['nombre', 'edad', 'estado', 'cartas_escritas', 'cartas_en_proceso']
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys() if key in valid_fields])
        values = list(kwargs.values())
        values.append(doll_id)

        conn = create_connection()
        if conn is not None:
            try:
                sql = f"UPDATE dolls SET {set_clause} WHERE id = ?"
                cursor = conn.cursor()
                cursor.execute(sql, values)
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                print(f"No se actualizo: {e}")
            finally:
                conn.close()
        return False

    @staticmethod
    def delete(doll_id):
        conn = create_connection()
        if conn is not None:
            try:
                sql = "DELETE FROM dolls WHERE id = ?"
                cursor = conn.cursor()
                cursor.execute(sql, (doll_id,))
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                print(f"No se pudo borrar la Doll: {e}")
            finally:
                conn.close()
        return False

    @staticmethod
    def get_available():
        conn = create_connection()
        if conn is not None:
            try:
                sql = """SELECT * FROM dolls
                         WHERE estado = 'activo' AND cartas_en_proceso < 5
                         ORDER BY cartas_en_proceso ASC"""
                cursor = conn.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"No se encontro Dolls disponibles: {e}")
            finally:
                conn.close()
        return []

    @staticmethod
    def get_cartas_count(doll_id):
        conn = create_connection()
        if conn is not None:
            try:
                sql = "SELECT cartas_en_proceso FROM dolls WHERE id = ?"
                cursor = conn.cursor()
                cursor.execute(sql, (doll_id,))
                result = cursor.fetchone()
                return result[0] if result else 0
            except sqlite3.Error as e:
                print(f"Conteo de cartas errado: {e}")
            finally:
                conn.close()
        return 0

    @staticmethod
    def get_cartas_escritas_count(doll_id):
        conn = create_connection()
        if conn is not None:
            try:
                sql = "SELECT cartas_escritas FROM dolls WHERE id = ?"
                cursor = conn.cursor()
                cursor.execute(sql, (doll_id,))
                result = cursor.fetchone()
                return result[0] if result else 0
            except sqlite3.Error as e:
                print(f"Conteo de cartas escritas errado: {e}")
            finally:
                conn.close()
        return 0


class ClienteModel:
    @staticmethod
    def create(nombre, ciudad, motivo_carta, contacto):
        if not nombre:
            raise ValueError("Nombre es un campo obligatorio.")

        conn = create_connection()
        if conn is not None:
            try:
                sql = '''INSERT INTO clientes(nombre, ciudad, motivo_carta, contacto)
                         VALUES(?,?,?,?)'''
                cursor = conn.cursor()
                cursor.execute(sql, (nombre, ciudad, motivo_carta, contacto))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                print(f"No se creo el cliente: {e}")
            finally:
                conn.close()
        return None

    @staticmethod
    def read_all():
        conn = create_connection()
        if conn is not None:
            try:
                sql = "SELECT * FROM clientes"
                cursor = conn.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"No se encontro clientes: {e}")
            finally:
                conn.close()
        return []

    @staticmethod
    def read_by_id(cliente_id):
        conn = create_connection()
        if conn is not None:
            try:
                sql = "SELECT * FROM clientes WHERE id = ?"
                cursor = conn.cursor()
                cursor.execute(sql, (cliente_id,))
                return cursor.fetchone()
            except sqlite3.Error as e:
                print(f"No se leyo clientes: {e}")
            finally:
                conn.close()
        return None

    @staticmethod
    def update(cliente_id, **kwargs):
        if not kwargs:
            return False

        valid_fields = ['nombre', 'ciudad', 'motivo_carta', 'contacto']
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys() if key in valid_fields])
        values = list(kwargs.values())
        values.append(cliente_id)

        conn = create_connection()
        if conn is not None:
            try:
                sql = f"UPDATE clientes SET {set_clause} WHERE id = ?"
                cursor = conn.cursor()
                cursor.execute(sql, values)
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                print(f"No se pudo actualizar: {e}")
            finally:
                conn.close()
        return False

    @staticmethod
    def delete(cliente_id):
        conn = create_connection()
        if conn is not None:
            try:
                sql = "DELETE FROM clientes WHERE id = ?"
                cursor = conn.cursor()
                cursor.execute(sql, (cliente_id,))
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                print(f"No se pudo eliminar: {e}")
            finally:
                conn.close()
        return False

    @staticmethod
    def search_by_city(ciudad):
        conn = create_connection()
        if conn is not None:
            try:
                sql = "SELECT * FROM clientes WHERE ciudad LIKE ?"
                cursor = conn.cursor()
                cursor.execute(sql, (f'%{ciudad}%',))
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"No se encontro cliente por ciudad: {e}")
            finally:
                conn.close()
        return []


class CartaModel:

    @staticmethod
    def create(cliente_id, doll_id, contenido, resumen):
        if not cliente_id or not doll_id or not contenido:
            raise ValueError("Cliente, Doll y Contenido deben ser llenados si o si")

        conn = create_connection()
        if conn is not None:
            try:
                sql = '''INSERT INTO cartas(cliente_id, doll_id, contenido, resumen)
                         VALUES(?,?,?,?)'''
                cursor = conn.cursor()
                cursor.execute(sql, (cliente_id, doll_id, contenido, resumen))
                conn.commit()

                current_count = DollModel.get_cartas_count(doll_id)
                DollModel.update(doll_id, cartas_en_proceso=current_count + 1)

                return cursor.lastrowid
            except sqlite3.Error as e:
                print(f"No se creo la carta: {e}")
            finally:
                conn.close()
        return None

    @staticmethod
    def read_all():
        conn = create_connection()
        if conn is not None:
            try:
                sql = """SELECT c.*, cl.nombre as cliente_nombre, d.nombre as doll_nombre
                         FROM cartas c
                         JOIN clientes cl ON c.cliente_id = cl.id
                         JOIN dolls d ON c.doll_id = d.id"""
                cursor = conn.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"No se leyo las cartas: {e}")
            finally:
                conn.close()
        return []

    @staticmethod
    def read_by_id(carta_id):
        conn = create_connection()
        if conn is not None:
            try:
                sql = """SELECT c.*, cl.nombre as cliente_nombre, d.nombre as doll_nombre
                         FROM cartas c
                         JOIN clientes cl ON c.cliente_id = cl.id
                         JOIN dolls d ON c.doll_id = d.id
                         WHERE c.id = ?"""
                cursor = conn.cursor()
                cursor.execute(sql, (carta_id,))
                return cursor.fetchone()
            except sqlite3.Error as e:
                print(f"No se pudo leer la carta del todo: {e}")
            finally:
                conn.close()
        return None

    @staticmethod
    def update(carta_id, **kwargs):
        if not kwargs:
            return False

        valid_fields = ['cliente_id', 'doll_id', 'contenido', 'resumen', 'estado']
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys() if key in valid_fields])
        values = list(kwargs.values())
        values.append(carta_id)

        conn = create_connection()
        if conn is not None:
            try:
                sql = f"UPDATE cartas SET {set_clause} WHERE id = ?"
                cursor = conn.cursor()
                cursor.execute(sql, values)
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                print(f"No se pudo actualizar la carta que pidio: {e}")
            finally:
                conn.close()
        return False

    @staticmethod
    def delete(carta_id):
        if not CartaModel.can_be_deleted(carta_id):
            return False

        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT doll_id FROM cartas WHERE id = ?", (carta_id,))
                result = cursor.fetchone()

                if result:
                    doll_id = result[0]
                    sql = "DELETE FROM cartas WHERE id = ?"
                    cursor.execute(sql, (carta_id,))
                    conn.commit()

                    current_count = DollModel.get_cartas_count(doll_id)
                    DollModel.update(doll_id, cartas_en_proceso=current_count - 1)

                    return cursor.rowcount > 0
                return False
            except sqlite3.Error as e:
                print(f"No se pudo eliminar la carta: {e}")
            finally:
                conn.close()
        return False

    @staticmethod
    def update_status(carta_id, nuevo_estado):
        if nuevo_estado not in ['borrador', 'revisado', 'enviado']:
            raise ValueError("El estado solo puede ser: borrado o revisado o enviado unicamente")

        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()

                cursor.execute("SELECT estado, doll_id FROM cartas WHERE id = ?", (carta_id,))
                result = cursor.fetchone()
                if not result:
                    return False

                estado_actual, doll_id = result

                if estado_actual == 'enviado' and nuevo_estado != 'enviado':
                    raise ValueError("Si ya fue enviada entonces no puede editarla")

                sql = "UPDATE cartas SET estado = ? WHERE id = ?"
                cursor.execute(sql, (nuevo_estado, carta_id))

                if nuevo_estado == 'enviado' and estado_actual != 'enviado':
                    current_process = DollModel.get_cartas_count(doll_id)
                    current_written = DollModel.get_cartas_escritas_count(doll_id)
                    DollModel.update(doll_id,
                                   cartas_en_proceso=current_process - 1,
                                   cartas_escritas=current_written + 1)

                conn.commit()
                return True

            except sqlite3.Error as e:
                print(f"No se pudo cambiar el estado de la carta: {e}")
            finally:
                conn.close()
        return False

    @staticmethod
    def can_be_deleted(carta_id):
        conn = create_connection()
        if conn is not None:
            try:
                sql = "SELECT estado FROM cartas WHERE id = ?"
                cursor = conn.cursor()
                cursor.execute(sql, (carta_id,))
                result = cursor.fetchone()
                return result and result[0] == 'borrador'
            except sqlite3.Error as e:
                print(f"Error al momento de verificar: {e}")
            finally:
                conn.close()
        return False
    @staticmethod
    def get_cartas_por_doll(doll_id):
        conn = create_connection()
        if conn is not None:
            try:
                sql = """SELECT c.*, cl.nombre as cliente_nombre
                         FROM cartas c
                         JOIN clientes cl ON c.cliente_id = cl.id
                         WHERE c.doll_id = ?"""
                cursor = conn.cursor()
                cursor.execute(sql, (doll_id,))
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"No se obtuvo cartas por Doll: {e}")
            finally:
                conn.close()
        return []


if __name__ == '__main__':
    print(" test de los modelos")

    print("\n1. Prueba DollModel:")
    doll_id = DollModel.create("Violet Evergarden", 14, "activo")
    print(f"   Doll creada con ID: {doll_id}")
    print(f"   Dolls disponibles: {len(DollModel.get_available())}")

    print("\n2. Prueba ClienteModel:")
    cliente_id = ClienteModel.create("Leon Stephanotis", "Leidenschaftlich", "Negocios", "Estudio Fotografía")
    print(f"   Cliente creado con ID: {cliente_id}")

    print("\n3. Prueba CartaModel:")
    carta_id = CartaModel.create(cliente_id, doll_id, "Contenido de prueba", "Resumen de prueba")
    print(f"   Carta creada con ID: {carta_id}")
    print(f"   ¿Puede eliminarse? {CartaModel.can_be_deleted(carta_id)}")

    print("\n Pruebas completadas")
