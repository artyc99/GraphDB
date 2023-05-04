import os
import sys

from pyspark.sql import SparkSession

from libs.data_tsp_load import load

from graphframes import GraphFrame

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

spark = SparkSession\
    .builder\
    .master("local[*]")\
    .getOrCreate()


def main():

    vertices, edges = load('./data/data.tsp')

    v = spark.createDataFrame(vertices, ["id", "x", "y"])

    e = spark.createDataFrame(edges, ["src", "dst", "relationship"])
    v.printSchema()
    e.printSchema()

    g = GraphFrame(v, e)

    g.vertices.show()

    g.bfs('id = 20', 'id = 1', maxPathLength=10).show(truncate=False)


if __name__ == '__main__':
    main()
