# ADR 001 - Propriété du contrat d'intégration

Statut : accepté le 2026-09-06.

## Contexte

Le domaine source possède son modèle et son événement métier. Les consommateurs ont besoin d'un fait stable, minimal et sans dépendance à l'ORM.

## Décision

AstroBridge gouverne `TrainingSessionCreated.v1` avec le producteur `training-management` et les deux consommateurs déclarés. Le domaine source ne publie pas directement sa classe interne. Toute évolution est analysée selon les lecteurs identifiés.

## Alternatives et conséquences

Partager le modèle interne réduirait le mapping initial mais couplerait chaque consommateur. Laisser chaque consommateur interpréter un message sans propriétaire multiplierait les sens. Le contrat explicite ajoute une étape de gouvernance et rend les compatibilités testables.

