# Décisions acquises

- Contrat d'intégration distinct du modèle de domaine et de l'ORM.
- Version d'API canonique dans l'URL ; version de message dans l'enveloppe.
- RabbitMQ pour ack, reprise, routage et DLQ ; Redis Pub/Sub reste une comparaison.
- Downcast explicite V2 vers V1 durant la migration.
- Effets et notifications exclusivement synthétiques.

Les méthodes agiles, priorités et découpage du travail ne sont pas décidés ici.

