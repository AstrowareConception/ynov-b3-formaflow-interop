# Versionnement V1/V2 et dépréciation

## Stratégie canonique

L'API choisit le versionnement d'URL (`/api/v1`, `/api/v2`) : il est visible dans les scripts de cours, simple à router et permet une dépréciation progressive. Le versionnement par media type ou header évite parfois de multiplier les URL, mais rend les essais, caches et diagnostics moins immédiats. Une seconde implémentation complète n'apporterait rien au module.

Les contrats d'événements gardent `eventType=TrainingSessionCreated` et portent un entier `version`. Le cycle de l'API et celui du message restent distincts.

## Évolution additive

V2 ajoute `deliveryMode` et `location`. L'upcast V1→V2 choisit `ONSITE` et `TO_BE_CONFIRMED` comme défauts visibles, jamais comme faits supposés silencieusement. Le downcast V2→V1 retire seulement ces deux champs ; il est identifié dans `astrobridge.contracts.adapters` et validé avant publication sur le routage V1.

## Différences de format

- JSON Schema refuse les propriétés supplémentaires : V2 doit être adapté avant un reader V1 strict.
- Protobuf ignore les champs inconnus sur lecture et les préserve lors d'une re-sérialisation ; les numéros et noms supprimés doivent être `reserved` et jamais réutilisés.
- Avro résout writer et reader ensemble : les champs nouveaux ont des défauts, les records renommés ont des alias des deux côtés utilisés, et chaque direction est testée.
- Renommer, supprimer, changer un type ou une unité constitue une rupture tant qu'une résolution explicite et testée n'est pas démontrée.

## Dépréciation, migration et rollback

V1 renvoie `Deprecation: true`, `Sunset` et un `Link` de documentation. La migration suit : inventorier les clients, publier V2, observer les appels V1, migrer un client pilote, généraliser, puis retirer V1 après la date annoncée. En rollback, conserver V1 et l'adaptateur, arrêter la production V2 sans réutiliser ses numéros Protobuf, puis rejouer uniquement les messages identifiés et idempotents.

