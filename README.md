# AstroBridge — Échange de données & interopérabilité

> Version documentaire : 0.1.0  
> Statut : spécification initiale, repository non encore implémenté  
> Module : Échange de données & interopérabilité — Bachelor 3 DEV  
> Volume : 14 heures — 6 h FFP + 8 h TDP

## Finalité du repository

`ynov-b3-formaflow-interop` permet d'étudier comment deux systèmes autonomes échangent une information sans partager leur modèle interne. Le fil rouge **AstroBridge** transforme un fait métier de FormaFlow Core en événement d'intégration `TrainingSessionCreated.v1`, puis confronte ce même sens métier à trois représentations, plusieurs modes de transport et une évolution v1 vers v2.

Le dépôt fournit un environnement incomplet mais reproductible : contrats à compléter, corpus synthétique, producteur et consommateurs partiels, scénarios de panne, client API v1, tests et gabarits de preuves. Il ne contient ni solution finale ni corrigé d'évaluation.

## Résultats pédagogiques attendus

À l'issue du module, l'étudiant doit pouvoir :

- distinguer donnée, format, protocole, contrat et pattern d'intégration ;
- formaliser et tester un contrat JSON Schema 2020-12 ;
- représenter un même message en JSON, Protocol Buffers et Avro ;
- expliquer les règles d'évolution propres à Protobuf et Avro ;
- mesurer taille et temps de sérialisation sans surinterpréter un micro-benchmark ;
- choisir entre échange synchrone, file de travail, publication/abonnement et webhook ;
- configurer un routage RabbitMQ et fiabiliser producteur et consommateurs ;
- gérer accusés de réception, doublons, retry borné, message poison et dead-letter queue ;
- versionner une API et un contrat sans confondre leurs cycles de vie ;
- démontrer la compatibilité par des tests et une matrice producteur/consommateur.

## Fil rouge

FormaFlow Core signale qu'une session de formation vient d'être créée. AstroBridge publie un message destiné à deux consommateurs fictifs et indépendants : préparation administrative et notification.

`TrainingSessionCreated.v1` est un **événement d'intégration** : il dérive d'un fait du domaine, mais n'expose ni l'agrégat interne, ni ses objets ORM, ni son événement de domaine. Le mapping, les unités, les formats, la nullabilité et la responsabilité de chaque champ doivent être explicités.

## Choix technique structurant

Python 3.12 est conservé pour rendre visibles les contrats, la génération et les mesures sans imposer le framework du module backend. FastAPI/uvicorn porte l'exemple d'API HTTP ; `jsonschema`, Protobuf, `fastavro`, `pika` et `pytest` couvrent validation, sérialisation, messagerie et tests.

RabbitMQ sous Docker Compose est l'unique broker requis. Redis Pub/Sub est étudié par comparaison documentée : aucun serveur Redis supplémentaire n'est nécessaire.

## Parcours des quatre séances

1. Formaliser et valider un contrat JSON avec JSON Schema.
2. Comparer JSON, Protobuf et Avro, puis éprouver leur évolution.
3. Transporter et fiabiliser l'événement avec RabbitMQ.
4. Construire une migration v1-v2 compatible et valider individuellement les acquis.

## Validation des acquis

Le syllabus indique que le module est **non évalué**. Il comporte donc un seul dispositif individuel : un QCM formatif non noté de 30 minutes en séance 4. Les contrats, benchmarks, services et preuves produits en binôme reçoivent du feedback, mais ne constituent pas une seconde évaluation.

Le QCM, ses variantes et son corrigé sont conservés dans un kit privé formateur, hors de ce repository.

## Arborescence cible

```text
ynov-b3-formaflow-interop/
├── README.md
├── CHANGELOG.md
├── manifest.yml
├── Makefile
├── pyproject.toml
├── compose.yml
├── .env.example
├── inputs/architecture-reference/
├── contracts/
│   ├── json-schema/
│   ├── protobuf/
│   └── avro/
├── src/
│   ├── api/
│   └── messaging/
├── tests/
│   ├── contracts/
│   └── integration/
├── benchmarks/
│   └── results/
├── compatibility/
├── diagrams/
├── docs/
│   ├── adr/
│   └── cdan/transfer.md
├── evidence/
│   ├── async/
│   └── versioning/
└── handoff/agility-reference/
```

## Commandes contractuelles

| Commande | Effet attendu |
|---|---|
| `make setup` | Vérifier Python, Docker et installer l'environnement local |
| `make start` | Démarrer RabbitMQ et l'API d'exemple |
| `make stop` | Arrêter uniquement les services du repository |
| `make reset-data` | Restaurer fixtures, queues et états synthétiques |
| `make contracts` | Générer Protobuf et valider les trois familles de contrats |
| `make benchmark` | Produire les mesures brutes et leur synthèse reproductible |
| `make test` | Exécuter les tests déterministes de contrat et d'intégration |
| `make smoke` | Publier un événement et vérifier les consommateurs et la DLQ |
| `make quality` | Vérifier formatage, types, tests et fichiers attendus |

## Branches, tags et checkpoints

- `course-start` ;
- `checkpoint-contract` ;
- `checkpoint-serialization` ;
- `checkpoint-async` ;
- `checkpoint-versioning` ;
- `reference-final`.

Chaque binôme travaille dans `work/<team-id>`. Les checkpoints structurent le feedback formatif ; ils ne produisent aucune note. `course-start` et `reference-final` sont des tags formateur immuables.

## Entrée canonique

`inputs/architecture-reference/` contient une copie figée de `handoff/interop-reference/`, publiée par `ynov-b3-formaflow-hexagonal` au tag `reference-final` : langage ubiquitaire, context map, frontières, invariants, événements de domaine, candidats à l'intégration, diagrammes et ADR.

Ces fichiers sont en lecture seule. Le dépôt embarque toutes les fixtures et simulations nécessaires : aucun projet étudiant antérieur ni installation du projet DDD n'est requis.

## Sortie canonique

Après consolidation, le formateur publie `handoff/agility-reference/` au tag `reference-final`. Le paquet traduit la migration technique en dossier projet compréhensible : demande d'évolution v1-v2, acteurs, dépendances, incident, critères d'acceptation, risques, contrats et matrice de compatibilité.

`ynov-b3-formaflow-agility` copiera ce paquet dans son propre dossier d'entrée. Les branches de binômes ne sont jamais transmises comme prérequis.

## Sécurité et données

Toutes les données sont synthétiques. Les webhooks restent locaux, leurs secrets sont factices et aucun service cloud, compte externe, email ou paiement réel n'est appelé. Les journaux d'exemple ne doivent contenir ni secret ni donnée personnelle réaliste.

## État de cette V1

Cette version fixe le contrat du repository. Restent à produire : contrats volontairement incomplets, fixtures, API FastAPI, producteur et consommateurs RabbitMQ, webhook local, scénarios de panne, benchmark, tests, Makefile, checkpoints Git réels, kit QCM privé et paquet canonique pour l'agilité.
