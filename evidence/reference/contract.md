# Preuve formative - contrat d'échange V1

## Faits observés

Le JSON Schema 2020-12 accepte l'exemple valide et rejette capacité nulle et fin antérieure au début avec chemins précis.

## Hypothèses

La devise pédagogique reste EUR ; d'autres devises nécessiteraient une règle métier supplémentaire.

## Décision et alternatives

Un contrat d'intégration distinct du domaine est retenu plutôt qu'une exposition ORM.

## Preuves

`python -m pytest tests/unit/test_mapping.py tests/unit/test_validation.py tests/contracts/test_json_contract.py`.

## Limites

Ces tests ne démontrent pas encore le transport broker ni la compatibilité V2.

## Transfert au projet CDAN

Réutiliser la démarche propriétaire-consommateurs-invariants sur un événement du projet personnel.

