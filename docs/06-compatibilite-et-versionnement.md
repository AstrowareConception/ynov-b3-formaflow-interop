# Compatibilité et versionnement

## Vocabulaire

Toute conclusion nomme la version produite ou le schéma writer, la version consommée ou le schéma reader, le sens testé, le résultat et la preuve. Les termes backward, forward et full compatibility ne sont pas employés sans ce contexte.

## Ressources livrées

- `contracts/compatibility/matrix.yml` contient les couples writer/reader V1 et V2 ;
- `contracts/compatibility/format-evolution.md` décrit ajouts, défauts, renommages, suppressions, changements de type et champs Protobuf réservés ;
- `docs/versioning.md` définit la stratégie d'API, la dépréciation, la migration et le rollback ;
- `tests/compatibility/` vérifie les cas compatibles et volontairement incompatibles.

Chaque résultat précise la perte d'information éventuelle et la limite sémantique.

## API HTTP

La stratégie canonique utilise des chemins `/api/v1` et `/api/v2`. Le versionnement par en-tête reste comparé dans `docs/versioning.md`, sans seconde implémentation complète. Version d'API, version de message et version d'application restent indépendantes.

La route V1 expose les en-têtes `Deprecation`, `Sunset` et `Link`. La route V2 downcaste explicitement vers V1 pour préserver l'ancien consommateur.

## Dépréciation

La politique décrit coexistence, adaptateur, avertissement, observation d'usage, échéance, critères d'arrêt et rollback. Les en-têtes HTTP complètent cette communication mais ne la remplacent pas.
