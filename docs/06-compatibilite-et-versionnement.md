# Compatibilité et versionnement

## Vocabulaire obligatoire

Toute conclusion de compatibilité nomme explicitement :

- la version produite ou le schéma d'écriture ;
- la version consommée ou le schéma de lecture ;
- le sens testé ;
- le résultat et sa preuve.

Les termes backward, forward et full compatibility ne sont jamais employés sans ce contexte.

## Matrice minimale

`compatibility/serialization-matrix.md` confrontera readers et writers v1/v2 pour JSON Schema, Protobuf et Avro. `compatibility/api-versioning.md` confrontera client v1, client v2, API v1, API v2 et adaptateur.

Chaque cellule contient : compatible, conditionnel ou cassant ; test associé ; éventuelle perte d'information ; limite sémantique.

## API HTTP

Le dossier v1-v2 permet de comparer :

- version dans l'URL ;
- version dans un en-tête ;
- négociation par media type.

La décision prend en compte lisibilité, cache, routage, documentation, observabilité et coût de migration. Version d'API, version de message et version d'application restent indépendantes.

## Dépréciation

La politique attendue précise coexistence, adaptateur, avertissement, métriques d'usage, échéance, critères d'arrêt et rollback. Les en-têtes `Deprecation` et `Sunset` peuvent être employés lorsqu'ils sont applicables, mais ne remplacent pas une communication et une stratégie de repli.
