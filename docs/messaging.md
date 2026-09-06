# RabbitMQ, retry, DLQ et comparaison Redis

AstroBridge déclare l'exchange topic durable `formaflow.events`, routing key `training.session.created.v1`, et deux files durables indépendantes : `astrobridge.administration.training-session-created.v1` et `astrobridge.notification.training-session-created.v1`. Les messages sont persistants, la publication attend un confirm, les consommateurs utilisent ack manuel et `prefetch=1`.

Chaque file possède une file `.retry` à TTL court reliée à `astrobridge.retry`. `x-retry-count` est borné à 3 ; au-delà, le message va vers `.dlq` via `astrobridge.dead-letter`. L'original n'est acquitté qu'après effet local ou republication durable. `eventId` pilote l'idempotence et `correlationId` est conservé dans les traces.

| Critère | RabbitMQ utilisé ici | Redis Pub/Sub, comparaison uniquement |
|---|---|---|
| Persistance | messages/files durables | aucune pour Pub/Sub |
| Acknowledgement | manuel | absent |
| Redelivery | configurable | absent si abonné déconnecté |
| Routage | topic/direct, bindings | canaux/patterns plus simples |
| Usage adapté | intégration fiable, reprise, DLQ | signal éphémère temps réel |
| Limite | exploitation et topologie à gouverner | perte possible, pas de retry natif |

Redis n'est ni déployé ni requis. Le consommateur Notification écrit une trace synthétique et n'envoie jamais d'e-mail.

