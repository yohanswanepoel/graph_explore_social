from neo4j import GraphDatabase
import pandas as pd
from util import Import_Education, Import_Work, Import_Trips, Import_Transactions, Clear_Graph
from neomodel import db

if __name__ == "__main__":
    # db.set_connection('bolt://neo4j:Pick_4_Good_Password@localhost:7687')
    clear_graph = Clear_Graph("bolt://localhost:7687", "neo4j", "Pick_4_Good_Password")
    clear_graph.clear()
    clear_graph.close()


    # import education
    imp_education = Import_Education("bolt://localhost:7687", "neo4j", "Pick_4_Good_Password")
    imp_education.import_data("sample_data/sng_education.csv")
    imp_education.close()

    # import work
    imp_work = Import_Work("bolt://localhost:7687", "neo4j", "Pick_4_Good_Password")
    imp_work.import_data("sample_data/sng_work.csv")
    imp_work.close()

    # import trips
    imp_trips = Import_Trips("bolt://localhost:7687", "neo4j", "Pick_4_Good_Password")
    imp_trips.import_data("sample_data/sng_trips.csv")
    imp_trips.close()

    # import transactions
    imp_tx = Import_Transactions("bolt://localhost:7687", "neo4j", "Pick_4_Good_Password")
    imp_tx.import_data("sample_data/sng_transaction.csv")
    imp_tx.close()

