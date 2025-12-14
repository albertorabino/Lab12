from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.connessione import Connessione

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO

    def cerca_rifugi(anno):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []

        query = """ 
                    select r.id AS id_rifugio, r.nome
                    FROM mountain_paths.rifugio r
                    JOIN mountain_paths.connessione c
                    ON r.id = c.id_rifugio1 OR r.id = c.id_rifugio2
                    WHERE c.anno <= %s
        """

        cursor.execute(query, (anno,))
        for row in cursor:
            rifugio = Rifugio(row['id_rifugio'], row['nome'])
            result.append(rifugio)

        print("Errore nel database")

        cursor.close()
        cnx.close()
        return result


    def connessioni(anno):
        cnx = DBConnect.get_connection()
        result = []
        cursor = cnx.cursor(dictionary=True)
        query = """
                            SELECT id_rifugio1,id_rifugio2,difficolta,distanza
                            from mountain_paths.connessione c,mountain_paths.rifugio r 
                            where anno<=%s and r.id =c.id_rifugio1
                """
        try:
            cursor.execute(query,(anno,))
            for row in cursor:
                conn = Connessione(row['id_rifugio1'],row['id_rifugio2'],row['difficolta'],row['distanza'])
                result.append(conn)
        except:
            print("Errore nel database")
        finally:
            cursor.close()
            cnx.close()
            return result

