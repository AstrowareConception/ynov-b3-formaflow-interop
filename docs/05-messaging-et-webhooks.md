# Messaging et webhooks

## Topologie RabbitMQ

- exchange topic : `formaflow.events` ;
- routing key : `training.session.created.v1` ;
- file administration : `astrobridge.administration.training-session-created.v1` ;
- file notification : `astrobridge.notification.training-session-created.v1` ;
- exchange retry : `astrobridge.retry` ;
- exchange dead-letter : `astrobridge.dead-letter` ;
- files retry et DLQ suffixées respectivement par `.retry` et `.dlq`.

Le producteur publie des messages persistants avec publisher confirms et `mandatory=True`. Les consommateurs utilisent un ack manuel et `prefetch_count=1`.

## Retry, DLQ et idempotence

Une erreur de décodage, de contrat ou une panne synthétique déclenche une republication bornée. Le canal active les publisher confirms pour les republications retry et DLQ. L'original est acquitté uniquement après confirmation ; un nack, un retour non routable ou une erreur AMQP provoque un nack avec requeue de l'original.

Les propriétés d'identification, de corrélation, de contenu et les en-têtes existants sont conservés. `x-retry-count` est incrémenté jusqu'à la DLQ. L'idempotence repose sur `eventId` et ne constitue pas une garantie `exactly-once` de bout en bout.

Les tests couvrent publication confirmée, deux consommateurs, doublon sans double effet, redelivery après fermeture sans ack, JSON invalide, JSON valide non objet, retry borné, DLQ et confirmation négative sans ack.

## Webhook local

L'émetteur et le récepteur utilisent un secret factice configurable, une signature HMAC, un horodatage et une clé d'idempotence. Le récepteur limite le rejeu. L'émetteur applique un timeout et au plus trois tentatives par défaut.

Les tests couvrent signature invalide, rejeu, corps signé non objet, première réponse HTTP 5xx suivie d'un succès et épuisement borné sur réponses 5xx. Le backoff est injectable afin que les tests n'attendent pas réellement.

## Comparaison Redis Pub/Sub

Redis Pub/Sub est comparé à RabbitMQ pour la diffusion temps réel : absence de persistance et d'acknowledgement natifs, pas de reprise automatique des messages manqués et routage plus limité. Aucun service Redis n'est déployé.
