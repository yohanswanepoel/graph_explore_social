# Exploring NEO4J

## Purpose
This repository is for me to learn more about graph databases and the power of exploring relationships between data elements using graph.

## Project structure
* Sample data in ./sample_data
* Cypher queries in util.py (using neomodel is probably simpler but there are some downsides in how labels are applied)
* Imports done line by line using Cypber ... not what you would on production *apoc.load.csv* would be faster

## Setup using Podman

### Pre-req
* Latest version of Podman running. Tested on 4.5.1

Create podman instance with mounted home - starting fresh
``bash
podman machine stop podman-machine-default
podman machine rm podman-machine-default
podman machine init --cpus=4 --disk-size=60 --memory=6096 -v $HOME:$HOME
podman machine start

```

Create Container for Neo4J
```bash
podman run \
    --restart always \
    --publish=7474:7474 --publish=7687:7687 \
    --env NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
    --env NEO4J_AUTH=neo4j/Pick_4_Good_Password \
    --volume=temp/ndata:/data \
    --volume=temp/nlogs:/logs \
    neo4j:5.9.0-enterprise \ 
    2>&1 & 

```

Crate container for Neodash
```bash
podman run --arch=x86_64 -it --rm -p 5005:5005 neo4jlabs/neodash  2>&1 & 
```

* Log on to localhost:7474

## Data Set - Assumptions
* Real data can have overlapping Passport Numbers per country - this model assumes numbers are unique
* Travelled model can be better, but that is heavily query and use case depended
* Transactions can almost be a date, year or month split out

## Use Cases
* Who might know how work and student overlap

#### Who knows who - from work? 
* No one
```cypher
MATCH (p:Employee)-[:WORKED_AS]->(r:Role)-[:AT_COMPANY]->(c:Employer) return p,c

# If you need to do it in the NeoDash - it does not automatically fill in the relationships
MATCH (p:Employee)-[x:WORKED_AS]->(r:Role)-[z:AT_COMPANY]->(c:Employer) return p,c,r,z,x

```
#### General Card Spend (this may not be the best type of use for graph)
```cypher
MATCH (p:Person)-[:HAS_CARD]->(n:CreditCard)-[tx:USED_AT]->(m:Merchant) return p.name,n.nr,sum(tx.amount)
```

#### Who knows who - from education
* Ah we have three people that attended the same school: 
```cypher
MATCH (p:Student)-[x:ENROLLED_IN]->(r:Course)-[y:AT_SCHOOL]->(c:School) return p,r,c,x,y
```
* A more precise way to run that query - now we are look for courses with exact dates *probably would look for overlaps as well*
```cypher
MATCH (p1:Student)-[x1:ENROLLED_IN]->(r1:Course)-[y1:AT_SCHOOL]->(c1:School)
MATCH (p2:Student)-[x2:ENROLLED_IN]->(r2:Course)-[y2:AT_SCHOOL]->(c2:School)
WHERE p1 <> p2
  AND c1.name = c2.name
  AND r1.name = r2.name
  AND x1.from = x2.from
  AND x1.to = x2.to
RETURN p1,p2,r1,c1, x1, y1
```

```cyper that same query for tabular view
MATCH (p1:Student)-[x1:ENROLLED_IN]->(r1:Course)-[y1:AT_SCHOOL]->(c1:School)
MATCH (p2:Student)-[x2:ENROLLED_IN]->(r2:Course)-[y2:AT_SCHOOL]->(c2:School)
WHERE p1 <> p2
  AND c1.name = c2.name
  AND r1.name = r2.name
  AND x1.from = x2.from
  AND x1.to = x2.to
RETURN DISTINCT p1.name,r1.name,c1.name, x1.from, x1.to
```

* Overlapping trips
* Transactions in a country while outside a country
* Where does a person spend their money
* Where does a person travel



## Running Python App

Setup venv and activate
```bash
python3 -m venv venv
source venv/bin/activate
```

Install requirements
```bash
pip install -r requirements.txt
```

