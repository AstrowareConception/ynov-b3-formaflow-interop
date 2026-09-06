# Contrats et représentations

## Sémantique commune

JSON, Protobuf et Avro préservent l'identité de l'événement, sa version, sa date d'occurrence, la corrélation et les données minimales de session. Le mapping documente les types, unités, identifiants, valeurs absentes ou nulles, règles métier et données volontairement non exposées.

## JSON Schema

Les schémas V1 et V2 utilisent JSON Schema 2020-12 avec `$schema`, `$id`, `type`, `properties`, `required` et `additionalProperties: false`. Ils sont volontairement explicites et plats : ils n'emploient actuellement ni `$defs` ni `$ref`.

La V1 impose notamment l'enveloppe stable, les identifiants canoniques, les dates UTC, une capacité positive, un prix en unité mineure et le statut `SCHEDULED`. La V2 reprend ces champs et exige `deliveryMode` et `location`. L'invariant `endsAt > startsAt` reste complété par la validation applicative.

Une racine JSON non objet produit une erreur contrôlée au chemin `$`, de règle `type`. Les exemples valides et invalides sont synchronisés avec les tests de contrats.

## Protobuf

Les numéros de champs sont stables, les numéros supprimés sont réservés et ne sont jamais réutilisés. Les champs inconnus sont préservés par un lecteur compatible, mais une absence ou une valeur par défaut Protobuf ne remplace pas automatiquement une règle métier.

Le code Python versionné est généré par `scripts/generate_contracts.py`. Le mode `--check` refuse un module généré obsolète.

## Avro

La compatibilité dépend du couple schéma writer/reader. Les ajouts V2 disposent de valeurs par défaut explicites lorsque la lecture V1/V2 le nécessite. Renommage, suppression et changement de type sont documentés dans `contracts/compatibility/format-evolution.md`.

## Équivalence

Les tests de round-trip reconstruisent une représentation sémantique commune. L'équivalence ne signifie pas que les octets, les mécanismes de valeurs par défaut ou les règles d'évolution sont identiques entre formats.
