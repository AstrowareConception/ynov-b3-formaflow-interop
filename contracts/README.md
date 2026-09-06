# Contrat canonique V1

`TrainingSessionCreated.v1` est un événement d'intégration dérivé de la création métier d'une session, jamais une sérialisation d'agrégat ou d'ORM.

- Propriétaire : gouvernance de contrat AstroBridge avec `training-management` producteur.
- Source métier : création d'une session planifiée FormaFlow.
- Consommateurs : préparation administrative et notification synthétique.
- Garanties : enveloppe stable, identifiants opaques, UTC, capacité positive, prix en unité mineure, EUR, statut initial.
- Non-garanties : ordre global, livraison exactement une fois, contenu personnel, structure interne ou envoi d'e-mail.
- Évolution : ajout compatible seulement après analyse des lecteurs ; rupture de sens, unité, type ou champ requis implique une nouvelle version et une migration testée.

Le JSON Schema contrôle la structure. `astrobridge.contracts.validation` ajoute l'invariant inter-champs `endsAt > startsAt` et retourne des chemins d'erreur lisibles.

