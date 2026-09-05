# Architecture du repository

## Composants exécutables

| Zone | Responsabilité |
|---|---|
| `src/api/` | API FastAPI v1/v2, webhook local et adaptateurs de compatibilité |
| `src/messaging/` | publication, routage, consommateurs, retry, DLQ et idempotence |
| `contracts/` | sources contractuelles JSON Schema, Protobuf et Avro |
| `tests/contracts/` | validation, golden samples et compatibilité de schémas |
| `tests/integration/` | broker, redelivery, doublons, poison messages et webhook |
| `benchmarks/` | corpus, protocole, scripts et résultats |
| `compatibility/` | matrices de versions, politique d'API et dépréciation |

## Flux de référence

1. un adapter simulé construit `TrainingSessionCreated.v1` ;
2. le message est validé avant publication ;
3. le producer ajoute `event_id`, `occurred_at` et `correlation_id` ;
4. un exchange topic route vers deux queues indépendantes ;
5. chaque consumer revalide, traite de façon idempotente puis acquitte ;
6. les échecs temporaires suivent un retry borné ; les messages poison terminent en DLQ.

## Frontières

Les modèles Python générés ou internes ne sont pas le contrat public. Les contrats sources et leurs règles de compatibilité font autorité. Les consumers ne lisent pas la base du producer et ne dépendent pas du projet DDD.

## Configuration

`.env.example` documentera uniquement des valeurs locales et factices : URL RabbitMQ, ports, noms d'exchange/queues, secret de webhook de démonstration et niveau de log. Aucun secret réel n'est versionné.
