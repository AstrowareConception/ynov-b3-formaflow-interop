# Architecture du repository

## Composants exécutables

| Zone | Responsabilité |
|---|---|
| `src/astrobridge/api/` | API FastAPI V1/V2, réception du webhook et consultation des preuves |
| `src/astrobridge/application/` | mapping du modèle amont synthétique vers l'événement d'intégration |
| `src/astrobridge/contracts/` | validation, codecs et adaptateurs V1/V2 |
| `src/astrobridge/messaging/` | publication, topologie RabbitMQ, consommateurs, retry et DLQ |
| `src/astrobridge/observability/` | preuves locales et registre d'idempotence |
| `src/astrobridge/webhooks/` | signature, protection contre le rejeu et émission avec retry |
| `src/generated/` | modules Python générés depuis les contrats Protobuf |
| `contracts/` | JSON Schema, Protobuf, Avro, exemples et matrice de compatibilité |
| `tests/` | tests unitaires, contrats, compatibilité, intégration, smoke et packaging |
| `benchmarks/raw/` et `benchmarks/reports/` | mesures brutes et synthèse contextualisée |

## Flux de référence

1. le mapping applicatif construit `TrainingSessionCreated.v1` à partir d'une session synthétique ;
2. le contrat est validé avant publication ;
3. le producteur publie l'enveloppe existante avec un message persistant et un publisher confirm ;
4. l'exchange topic `formaflow.events` route vers deux files indépendantes ;
5. chaque consommateur revalide, traite de façon idempotente puis acquitte ;
6. un échec republie vers le retry ou la DLQ avec confirmation avant l'ack de l'original.

## Frontières

Les modèles Python générés ou internes ne sont pas le contrat public. Les contrats sources et leurs règles de compatibilité font autorité. Les consommateurs ne lisent pas la base du producteur et ne dépendent pas du modèle de persistance FormaFlow.

## Configuration

`.env.example` contient uniquement des valeurs locales et factices : hôte RabbitMQ, identifiants de démonstration, secret de webhook synthétique et répertoire de preuves. `compose.yml` limite les ports à `127.0.0.1`.
