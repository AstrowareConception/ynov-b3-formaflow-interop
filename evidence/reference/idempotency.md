# Preuve formative - idempotence

## Faits observés

Deux publications du même `eventId` produisent un seul effet par consommateur et une trace `duplicate-ignored`.

## Hypothèses

Le stockage fichier convient à la démonstration locale, pas à plusieurs instances concurrentes en production.

## Décision et alternatives

L'idempotence est placée au consommateur ; une livraison exactement une fois n'est pas supposée.

## Preuves

`tests/unit/test_idempotency_retry.py` et `tests/integration/test_rabbitmq_flow.py`.

## Limites

Pas de verrou distribué ni de rétention longue.

## Transfert au projet CDAN

Identifier une clé stable et rendre visible le second traitement sans second effet.

