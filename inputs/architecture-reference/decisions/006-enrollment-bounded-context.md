# ADR-006 - Frontière du bounded context Inscription

## Contexte
FormaFlow mêle catalogue, commerce, droit de participation et messages.
## Problème
Déduire les frontières des tables confond stockage et langage.
## Options
Contexte unique; contexte par table; contextes par responsabilités et cycles de vie.
## Décision
Gestion des inscriptions possède `Enrollment` et ses décisions. Catalogue fournit la session; Commande fournit prix accepté/confirmation; Notification et Projections consomment des faits traduits.
## Conséquences positives et négatives
Ownership et langage explicites; les contrats entre contextes restent à éprouver au module Interopérabilité.
## Preuves
Context map, composants et séquence `EnrollLearner`.
## Limites
Une application modulaire, pas des microservices.
## Condition de réexamen
Réexaminer après découverte de nouvelles conversations métier ou contraintes organisationnelles.
