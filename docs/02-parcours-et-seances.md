# Parcours et séances

## Séance 1 — Contrat JSON explicite (4 h)

Entrée : dossier d'architecture canonique et exemples ambigus de `TrainingSessionCreated`.

Productions :

- table de mapping modèle interne / événement d'intégration ;
- JSON Schema 2020-12 ;
- exemples valides et invalides ;
- validateur Python et tests positifs/négatifs ;
- registre d'hypothèses et rapport de contrat.

Sortie : `checkpoint-contract` après `make contracts` et `make test`.

## Séance 2 — Trois représentations et leur évolution (3 h)

Productions :

- définitions `.proto` et `.avsc` du même message ;
- génération Protobuf reproductible ;
- encodage/décodage d'un corpus commun ;
- preuve d'équivalence sémantique ;
- mesures brutes, synthèse et ADR de choix ;
- matrice d'évolution compatible/cassante.

Sortie : `checkpoint-serialization` après `make contracts`, `make benchmark` et `make test`.

## Séance 3 — Intégration asynchrone fiable (4 h)

Productions :

- exchange topic, deux queues et routing keys documentés ;
- producteur avec validation et publisher confirms ;
- consommateurs avec ack manuel, prefetch et logs structurés ;
- idempotence, retry borné et dead-letter queue ;
- tests d'intégration et rapport d'injection de pannes.

Sortie : `checkpoint-async` après `make start`, `make smoke` et `make test`.

## Séance 4 — Migration v1-v2 et validation individuelle (3 h)

Productions formatives :

- contrat corrigé et tests de compatibilité ;
- matrice producteur/consommateur ;
- décision de versionnement URL ou en-tête ;
- adaptateur maintenant le client v1 ;
- politique de dépréciation, risques et solution de repli ;
- trace de transfert CDAN.

Un QCM individuel non noté de 30 minutes clôt la validation des acquis. Sortie : `checkpoint-versioning`, puis consolidation formateur dans `reference-final`.
