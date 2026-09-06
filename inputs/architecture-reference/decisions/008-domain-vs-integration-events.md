# ADR-008 - Domain event et événement d'intégration

## Contexte
Le référentiel connaît `EnrollmentCreated.v1`; le modèle local parle de confirmation.
## Problème
Publier directement la classe domaine couplerait modèle interne et consommateurs.
## Options
Sérialisation directe; aucun événement; traduction explicite.
## Décision
Garder `EnrollmentConfirmed` local et traduire séparément vers `EnrollmentCreated.v1` lorsque l'intégration est requise. Message de broker et journal restent d'autres concepts.
## Conséquences positives et négatives
Évolution interne protégée; un mapping supplémentaire est nécessaire.
## Preuves
Événement collecté/purgé et tests zéro événement sur refus.
## Limites
Le checkpoint collecte en mémoire; aucune livraison durable n'est revendiquée.
## Condition de réexamen
Réexaminer le contrat et l'outbox dans le module Interopérabilité.
