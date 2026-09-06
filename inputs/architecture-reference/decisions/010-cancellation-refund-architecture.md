# ADR-010 - Architecture de l'annulation et du remboursement

## Contexte
Le sujet pratique fournit un contrôleur fonctionnel mêlant HTTP, SQL, horloge, calcul et événement.
## Problème
Séparer les décisions sans imposer CQRS ou Event Sourcing à une mutation simple.
## Options
Conserver le contrôleur; service unique technique; domaine + cas d'usage + ports ciblés.
## Décision
`RefundPolicy` calcule depuis prix accepté et instants UTC. `Enrollment.cancel` protège transition/idempotence et collecte l'événement. `CancelEnrollment` orchestre via `CancellationTransaction`, `Clock` et `DomainEventPublisher`; les adapters HTTP/PostgreSQL traduisent.
## Conséquences positives et négatives
Bornes pures, événement unique et tests sans infrastructure; un port transactionnel supplémentaire est assumé.
## Preuves
Tests domaine aux bornes, tests applicatifs, intégration PostgreSQL idempotente et `cancel-sequence.mmd`.
## Limites
Aucun remboursement financier réel, outbox ou contrat d'intégration d'annulation.
## Condition de réexamen
Réexaminer si la décision financière appartient à un autre bounded context ou devient asynchrone.
