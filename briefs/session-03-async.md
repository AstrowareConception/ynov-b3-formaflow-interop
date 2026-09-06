# Séance 3 - Publication fiable et reprise

**Durée :** 4 h, dont 1 h 30 FFP et 2 h 30 TDP. **Contexte :** deux consommateurs indépendants reçoivent le même événement via RabbitMQ.

## Objectifs et apport FFP

Étudier topic exchange, routage, confirms, ack manuel, idempotence, retry borné, poison, DLQ et webhook signé.

## Travail pratique

Démarrer Compose, injecter doublon et panne, redémarrer un consommateur, observer les traces synthétiques et tester le rejeu webhook.

## Production formative et preuve CDAN

Produire une démonstration d'idempotence et une décision de broker. Auto-vérifier deux effets indépendants, correlation ID, absence de boucle et DLQ.

## Commandes, erreurs fréquentes et checkpoint

`python scripts/tasks.py start`, `test-integration`, `smoke`, puis `stop`. Ne pas ack avant effet, réessayer sans borne ou envoyer un vrai e-mail. Fin : `checkpoint-async`.

