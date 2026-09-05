# Messaging et webhooks

## Topologie RabbitMQ

La référence comporte un exchange `topic`, une queue par responsabilité de consumer et des routing keys explicites. Les noms exacts seront fixés dans l'implémentation V0.2, avec une convention commune dans la documentation et les tests.

Le producteur active les publisher confirms et publie des messages persistants. Les consumers utilisent acknowledgements manuels, prefetch borné, validation à l'entrée et logs structurés.

## Sémantique de livraison

Le parcours illustre `at-most-once` et `at-least-once`. Il n'annonce pas de garantie `exactly-once` de bout en bout. Avec `at-least-once`, l'effet métier doit être idempotent à partir d'une clé stable, même si le même `event_id` est livré plusieurs fois.

## Échecs attendus

- consumer indisponible puis redémarré ;
- exception avant l'effet métier ;
- exception après l'effet métier mais avant l'ack ;
- doublon volontaire ;
- message non conforme ;
- message poison après le nombre maximal de tentatives.

Les tests doivent prouver retry borné, absence de boucle infinie, redelivery visible et arrivée déterministe en DLQ.

## Webhook local

Le dépôt inclura un émetteur et un receiver locaux. Le contrat précisera identifiant, horodatage, signature fondée sur un secret factice, timeout, retries et idempotence. Les tests couvriront signature invalide, réponse 5xx et notification rejouée.

## Comparaison Redis Pub/Sub

Redis Pub/Sub est comparé à RabbitMQ pour la diffusion temps réel : faible persistance, absence de reprise native des messages manqués et sémantique proche de `at-most-once`. Cette comparaison est documentée ; aucun service Redis n'est requis.
