# Incident de référence - lieu absent après migration

## Faits observés

Un client administratif ancien reçoit directement un JSON V2 strict et le rejette à cause de `deliveryMode` et `location`. Aucun message n'est perdu dans RabbitMQ, mais la file administrative augmente tandis que Notification continue.

## Hypothèses

Le producteur a contourné l'adaptateur V2→V1 ou utilisé la mauvaise routing key. La capacité et les horaires restent corrects.

## Décision de réponse

Suspendre la publication V2 vers le routage V1, restaurer le downcast, conserver les messages en file, vérifier l'idempotence puis reprendre par lots. Ne ni purger la file ni modifier le schéma V1 en urgence.

## Exploitation pédagogique

Prioriser diagnostic, mitigation, critères de reprise, communication, dette de migration et observabilité. L'incident reste volontairement ouvert pour le cours Agilité ; aucun backlog entièrement résolu n'est fourni.

