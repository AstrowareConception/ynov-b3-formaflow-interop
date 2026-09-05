# Contrats et représentations

## Sémantique commune

Les trois représentations décrivent le même événement et doivent préserver : identité de l'événement, version, date d'occurrence, corrélation, identifiant de session, formation, période, capacité et informations strictement nécessaires aux consommateurs.

Le mapping doit expliciter :

- types et unités ;
- format des dates et identifiants ;
- absent, `null`, vide et valeur par défaut ;
- champs requis ou optionnels ;
- propriétaire et définition métier ;
- règle structurelle ou invariant métier ;
- donnée volontairement non exposée.

## JSON Schema

Le contrat utilise le dialecte 2020-12 avec `$schema`, `$id`, `type`, `properties`, `required`, `additionalProperties`, `$defs` et `$ref`. Il fournit plusieurs exemples valides et invalides ainsi que des erreurs contenant un chemin exploitable.

Un `format` JSON Schema ne remplace pas nécessairement une validation applicative. Les règles métier qui nécessitent un état externe restent hors du schéma.

## Protocol Buffers

Le `.proto` doit appliquer ces règles :

- les numéros de champs sont stables ;
- un numéro supprimé n'est jamais réutilisé ;
- les numéros et noms retirés sont déclarés `reserved` ;
- l'ajout de champ tient compte des valeurs par défaut ;
- les champs inconnus et les déploiements désynchronisés sont testés ;
- le code généré est reproductible par `make contracts` et n'est pas édité manuellement.

## Avro

Le `.avsc` documente le record, les unions et les valeurs par défaut. Les tests distinguent schéma d'écriture et schéma de lecture et vérifient résolution, alias et promotions de types autorisées. Le schéma d'écriture doit rester disponible au lecteur des données binaires.

## Évolution

Chaque modification — ajout, suppression logique, renommage, changement de type ou contrainte — est classée selon le format et le couple précis de versions. Une compatibilité technique ne garantit pas une compatibilité sémantique.
