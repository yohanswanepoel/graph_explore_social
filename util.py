from neo4j import GraphDatabase
import pandas as pd 
import datetime, dateutil.parser


class Clear_Graph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def clear(self):
        tx = self.driver.session()
        result = tx.run(
            "MATCH (n) DETACH DELETE (n)")
        tx.close()

class Import_Education:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def import_data(self, file_uri):
        df = pd.read_csv(file_uri)
        for i, j in df.iterrows():
            tx = self.driver.session()
            result = tx.run(
                """
                MERGE (a:Country {name: $country})
                MERGE (b:Person {name: $name})
                ON CREATE SET b.passport=$passport
                SET b:Student
                MERGE (c:Organisation:School {name: $nameofinstitution})
                MERGE (d:Course {name: $course})
                MERGE (c)-[:BASED_IN]->(a)
                MERGE (b)-[:ATTENDED]->(c)
                MERGE (d)-[:AT_SCHOOL]->(c)
                MERGE (b)-[e:ENROLLED_IN]->(d)
                ON CREATE SET e.from=$from_year, e.to=$to_year""", 
                country=j.country,
                name=j[1], 
                passport=j.passportnumber,
                nameofinstitution=j.nameofinstitution,
                course=j.course,
                from_year=j.startyear,
                to_year=j.endyear)
            tx.close()


class Import_Work:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def import_data(self, file_uri):
        df = pd.read_csv(file_uri)
        for i, j in df.iterrows():
            tx = self.driver.session()
            result = tx.run(
                """
                MERGE (a:Country {name: $country})
                MERGE (b:Person {name: $name})
                ON CREATE SET b.passport=$passport
                SET b:Employee
                MERGE (c:Organisation:Employer {name: $nameoforganization})
                MERGE (d:Role {name: $designation})
                MERGE (c)-[:BASED_IN]->(a)
                MERGE (b)-[:EMPLOYED_BY]->(c)
                MERGE (d)-[:AT_COMPANY]->(c)
                MERGE (b)-[e:WORKED_AS]->(d)
                ON CREATE SET e.from=$from_year, e.to=$to_year""", 
                country=j.country,
                name=j[1], 
                passport=j.passportnumber,
                nameoforganization=j.nameoforganization,
                designation=j.designation,
                from_year=j.startyear,
                to_year=j.endyear)
            tx.close()


class Import_Transactions:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def import_data(self, file_uri):
        df = pd.read_csv(file_uri)
        for i, j in df.iterrows():
            tx = self.driver.session()
            temp_tx_date = datetime.datetime.strptime(j.transactiondate, "%A, %d %B %Y")
            if "HOTEL" in j.merchant:
                print(j.merchant)
                print(j.cardnumber)
                print(temp_tx_date)
                print(temp_tx_date.strftime("%Y-%m-%d"))
            result = tx.run(
                """
                MERGE (a:Country {name: $country})
                MERGE (b:Person {name: $name})
                ON CREATE SET b.passport=$passport
                MERGE (c:CreditCard {nr: $cardNumber})
                MERGE (d:Organisation:Merchant {name: $merchant})
                MERGE (b)-[:HAS_CARD]->(c)
                MERGE (d)-[:BASED_IN]->(a)
                MERGE (c)-[tx:USED_AT]->(d)
                ON CREATE SET tx.transaction_date=date($txDate), tx.amount=toFloat($amount)
                """, 
                country=j.country,
                cardNumber=j.cardnumber,
                merchant=j.merchant,
                txDate=temp_tx_date.strftime("%Y-%m-%d"),
                amount=j.amount[1:],
                name=j[1], 
                passport=j.passportnumber)
            tx.close()

class Import_Trips:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def import_data(self, file_uri):
        df = pd.read_csv(file_uri)
        for i, j in df.iterrows():
            tx = self.driver.session()
            temp_departure = datetime.datetime.strptime(j.departuredate, "%A, %d %B %Y")
            temp_arrival = datetime.datetime.strptime(j.arrivaldate, "%A, %d %B %Y")
            result = tx.run(
                """
                MERGE (az:Country {name: $citizenship})
                MERGE (ad:Country {name: $departurecountry})
                MERGE (aa:Country {name: $arrivalcountry})
                MERGE (t:Trip {name: $tripkey })
                ON CREATE SET t.departureDate=date($departureDate), t.arrivalDate=date($arrivalDate)
                MERGE (b:Person {name: $name})
                ON CREATE SET b.passport=$passport
                SET b:Traveller
                MERGE (b)-[:CITIZEN_OF]-(az)
                MERGE (t)-[:TRAVELLED_TO]->(aa)
                MERGE (t)-[:TRAVELLED_FROM]->(ad)
                MERGE (b)-[e:TRAVELLED]->(t)""", 
                citizenship=j.citizenship,
                departurecountry=j.departurecountry,
                arrivalcountry=j.arrivalcountry,
                tripkey = hash("{}{}{}".format(j[1],j.departuredate,j.arrivaldate)),  
                departureDate=temp_departure.strftime("%Y-%m-%d"),
                arrivalDate=temp_arrival.strftime("%Y-%m-%d"),
                name=j[1], 
                passport=j.passportnumber)
            tx.close()