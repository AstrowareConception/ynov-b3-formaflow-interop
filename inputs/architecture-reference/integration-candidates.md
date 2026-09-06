# Contrats existants et candidats

## Canonique existant

`EnrollmentCreated.v1` vient de FormaFlow Reference 1.0.0. Producteur déclaré: `enrollment-management`. Consommateurs déclarés: notification, projection capacité, portail participant. Données minimales: identifiants opaques inscription/session/participant, état et date UTC selon son schéma canonique.

## Candidat non contractuel

`EnrollmentCancelled.v1` est un nom de travail, **pas un contrat canonique validé**. Producteur pressenti: Gestion des inscriptions. Consommateurs supposés: Notification, Projections, éventuellement Commande et facturation si une conversation de remboursement est validée.

Informations à discuter: identifiant d'inscription, session, instant d'annulation et résultat de politique; le montant est-il nécessaire ou relève-t-il du contexte financier? Aucun e-mail ni nom n'est requis.

Hypothèses: un downstream a besoin du fait d'annulation; la décision financière peut rester interne tant que son ownership n'est pas établi.

Questions ouvertes: qui possède la demande de remboursement? faut-il une outbox? quelles garanties de doublon/ordre? quelle rétention? quel schéma de confidentialité? quels consommateurs sont réels?
