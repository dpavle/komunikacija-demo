# Demo REST API, Message Queue i RPC-a sa RabbitMQ

Ovaj repozitorijum sadrži primere za REST (HTTP), Message Queue i RPC komunikaciju. Svi primeri su realizovani u Python programskom jeziku. REST (HTTP) primer koristi Flask web framework, dok Message Queue i RPC primeri koriste RabbitMQ (putem `pika` python biblioteke). 

## Uslovi za pokretanje

- Python 3.x
- RabbitMQ instaliran i pokrenut na `localhost` (ili ažurirajte parametre povezivanja za RabbitMQ u `mq_client.py`, `mq_worker.py`, `rpc_client.py` i `rpc_server.py`).

## Početak

1. Kloniraj repo:
```sh
git clone https://github.com/dpavle/komunikacija-demo.git
cd komunikacija-demo       
```

2. Kreirajte virtuelno okruženje (opcionalno, ali preporučljivo):
```sh
python -m venv venv
source venv/bin/activate # Na Windows-u koristite "venv\Scripts\activate"
```
3. Instalirajte potrebne zavisnosti:

```sh
pip install -r requirements.txt
```

4. Pokreni RabbitMQ server:

Proverite da je RabbitMQ instaliran i pokrenut na `localhost`. Ako je potrebno, ažurirajte parametre povezivanja za RabbitMQ u `mq_client.py`, `mq_worker.py`, `rpc_client.py` i `rpc_server.py`.

## REST API

REST API vam omogućava:

- Dobavljanje svih zadataka: `GET /api/tasks`
- Označavanje zadatka kao završenog: `PUT /api/tasks/<task_id>`

### Primer zahteva i odgovora

#### Dobavljanje svih zadataka

- Zahtev: `GET /api/tasks`

- Odgovor:
```json
[
 {"id": 1, "title": "Zadatak 1", "description": "Opis za Zadatak 1", "done": false},
 {"id": 2, "title": "Zadatak 2", "description": "Opis za Zadatak 2", "done": true}
]
```
#### Označavanje zadatka kao završenog

- Zahtev: PUT /api/tasks/2

- Odgovor: HTTP 200 OK

    
```json
{"message": "Zadatak sa ID 2 je označen kao završen."}
```

## Message Queue sa RabbitMQ

Integracija sa RabbitMQ omogućava asinhronu obradu zadataka. mq_client.py šalje zahteve mq_worker.py-u, a mq_worker.py simulira obradu svakog zahteva asinhrono. Bitno je napomenuti da mq_client.py u ovom scenariju ne čeka odgovor na zahteve koje je poslao. 

Pokretanje Message Queue Servera (Worker)

Pokrenite mq_worker.py kako biste omogućili obradu asinhronih zahteva:
```sh
python mq_worker.py
```

Slanje zahteva Message Queue Serveru (Client)

Za slanje zahteva serveru možete koristiti mq_client.py:

```sh
python mq_client.py
```

## RPC sa RabbitMQ

Implementacija RPC-a koristi RabbitMQ za simuliranje RPC obrasca. rpc_client.py šalje zahteve rpc_server.py-u, a rpc_server.py asinhrono obrađuje svaki zahtev i odgovara klijentu sa statusom traženog zadatka.

Pokrenite rpc_server.py kako biste omogućili obradu RPC zahteva:
```sh
python rpc_server.py
```
Za slanje RPC zahteva serveru možete koristiti rpc_client.py:
```sh
python rpc_client.py
```