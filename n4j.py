from neo4j import GraphDatabase

from libs.data_tsp_load import load


class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def query(self, query, db=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


def main():
    vertices, edges = load('./data/data.tsp')

    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", password="password")
    for vertic in vertices:
        conn.query("create (:City {id : " + str(vertic[0]) + ",x:" + str(vertic[1]) + ",y:" + str(vertic[2]) + "})")

    for edg in edges:
        conn.query("MATCH (src:City {id: " + str(edg[0]) + "})"\
            "MATCH (dst:City {id: " + str(edg[1]) + "})"\
            "MERGE (src)-[:ROAD  {way: " + str(edg[2]) + "}]->(dst);")
        print(edg)
        # MERGE(src)-[: ROAD {way: 10}]->(dst);

    src_id = 20
    dst_id = 1

    print(conn.query("MATCH (src:City { id:" + str(src_id) + " }), (dst:City { id: " + str(dst_id) + "}) , path = (src)-[:ROAD]->(dst) \
                RETURN distinct nodes(path) AS shortestPath, \
                length(path),  \
                min(reduce(way = 0, r in relationships(path) | way+r.way)) AS totalDistance   \
                ORDER BY length(path), totalDistance\
               "))


if __name__ == '__main__':
    main()
