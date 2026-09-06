# Résumé du contrat

Enveloppe stable : `eventId`, `eventType`, `version`, `occurredAt`, `correlationId`, `causationId`, `producer`, `payload`. Le payload V1 contient identifiants session et formation, UTC, capacité positive, prix entier en unité mineure EUR et statut `SCHEDULED`. V2 ajoute `deliveryMode` (`ONSITE`, `REMOTE`, `HYBRID`) et `location.label`.

L'événement ne garantit ni ordre global, ni exactly-once, ni structure ORM, ni donnée personnelle. `eventId` est la clé d'idempotence.

