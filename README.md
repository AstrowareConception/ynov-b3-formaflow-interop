# AstroBridge - Échange de données et interopérabilité

Version `1.0.0` du module Bachelor 3 FormaFlow. Durée totale : **14 h**, soit **6 h de face-à-face pédagogique (FFP)** et **8 h de travaux dirigés et pratiques (TDP)**. Le module est officiellement **non évalué** : aucune évaluation sommative, note ou rendu noté n'existe dans ce dépôt.

## Rôle d'AstroBridge

AstroBridge est la frontière d'interopérabilité de FormaFlow. Il transforme la création métier d'une session en événement d'intégration `TrainingSessionCreated.v1` sans exposer agrégat, entité ORM, persistance ou structure interne. Administration et Notification le consomment indépendamment ; Notification écrit uniquement une trace synthétique locale et n'envoie jamais d'e-mail.

Le parcours étudie JSON/JSON Schema 2020-12, Protobuf, Avro, benchmark contextualisé, HTTP synchrone, publication/abonnement RabbitMQ, ack, confirms, idempotence, retry/DLQ, webhook HMAC, versionnement d'API et compatibilité V1/V2. Redis Pub/Sub est uniquement comparé dans [messaging.md](docs/messaging.md) : aucun Redis n'est déployé.

## Parcours étudiant

| Séance | Durée | FFP | TDP | Production formative | Checkpoint |
|---|---:|---:|---:|---|---|
| 1 - contrats | 4 h | 2 h | 2 h | mapping, JSON Schema, erreurs et preuve | `checkpoint-contract` |
| 2 - sérialisation | 3 h | 1 h 30 | 1 h 30 | Protobuf, Avro, matrice et benchmark | `checkpoint-serialization` |
| 3 - asynchrone | 4 h | 1 h 30 | 2 h 30 | deux consommateurs, retry/DLQ et webhook | `checkpoint-async` |
| 4 - versionnement | 3 h | 1 h | 2 h | adaptateurs, migration, incident et handoff | `checkpoint-versioning` |
| **Total** | **14 h** | **6 h** | **8 h** | preuves CDAN non notées | `reference-final` |

La séance 4 comprend 30 minutes de vérification individuelle formative non notée. [La politique publique](docs/qcm-policy.md) décrit seulement le cadre ; aucune question, réponse, banque, correction, donnée individuelle ou notation n'est versionnée.

Commencer à `course-start`, lire le brief de la séance, exécuter les tests du stade, puis comparer avec le checkpoint suivant seulement au moment prévu. Les TODO et `xfail` du début sont intentionnels et validés par stade.

## Prérequis et installation native

- Git ;
- Python 3.12 dans un environnement virtuel standard ;
- Docker Desktop ou Docker Engine avec Compose pour RabbitMQ ;
- Node/npx uniquement pour régénérer les SVG Mermaid côté formateur.

Sous Windows :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --require-hashes -r requirements.lock
python -m pip install --no-deps -e .
python scripts/tasks.py test
```

Raccourci PowerShell : `./scripts/tasks.ps1 setup`. Aucune installation globale Python n'est nécessaire. GNU Make est facultatif : chaque cible appelle `python scripts/tasks.py <commande>`.

## Exécution Docker

```text
python scripts/tasks.py start
python scripts/tasks.py smoke
python scripts/tasks.py stop
```

Compose utilise le projet déterministe `formaflow-interop`, expose API, AMQP et management uniquement sur `127.0.0.1`, et épingle Python/RabbitMQ par tag et digest. `stop` et `reset-data` exécutent exclusivement `docker compose -p formaflow-interop down --volumes --remove-orphans`. Voir [troubleshooting.md](docs/troubleshooting.md) pour Windows.

## Commandes

| Commande | Effet |
|---|---|
| `setup` | crée `.venv` et installe le verrou avec hashes |
| `start` / `stop` | démarre ou nettoie uniquement le projet Compose |
| `reset-data` | supprime volumes du projet et preuves locales résolues |
| `contracts` / `generate` | valide les contrats ou régénère Protobuf |
| `benchmark` | régénère corpus déterministe, brut JSON et synthèse |
| `test` / `test-unit` | lance tous les tests ou les unitaires |
| `test-contracts` / `test-compatibility` | cible contrats ou compatibilité |
| `test-integration` / `smoke` | vérifie RabbitMQ ou le parcours Docker complet |
| `lint` / `typecheck` / `quality` | Ruff, mypy ou pipeline complet |
| `validate-repo` / `validate-diagrams` | validateur central ou couples Mermaid/SVG |
| `validate-handoff` | contrôle le paquet Agilité isolable |
| `package` | génère le ZIP déterministe hors dépôt |

Les commandes formateur `quality`, `validate-repo`, `validate-diagrams`, `validate-handoff` et `package` sont détaillées dans [teacher-guide.md](docs/teacher-guide.md). Les requêtes HTTP et équivalents curl/PowerShell sont dans [api-examples.md](docs/api-examples.md) et `requests/astrobridge.http`.

## Checkpoints

- `course-start` : environnement, santé, briefs, messages ambigus et TODO sans contrats finaux ;
- `checkpoint-contract` : mapping, JSON Schema, invariants, erreurs et ADR ;
- `checkpoint-serialization` : Protobuf/Avro, génération, équivalence et benchmark ;
- `checkpoint-async` : RabbitMQ robuste, deux consommateurs et webhook local ;
- `checkpoint-versioning` : V2, adaptateurs, API versionnée, migration et incident ;
- `reference-final` et `interop-v1.0.0` : référence relue, validateurs et handoff autonome.

Chaque tag annoté indique sa validation et le checkpoint précédent. Aucun tag ou branche d'évaluation n'est créé.

## Contrats, sécurité et données

Le contrat est documenté dans [contracts/README.md](contracts/README.md). Toutes les fixtures sont manifestement synthétiques, les identifiants opaques et les valeurs de `.env.example` explicitement factices. Aucun service cloud, paiement, e-mail ou donnée personnelle réelle n'est utilisé. Les secrets de webhook servent seulement à la démonstration locale.

## Sources contrôlées

- squelette `ynov-b3-formaflow-interop` 0.1.0, SHA-256 `2a7f9445b4fd1b3e8dd304e2abf85b670bc03e0213a84db3e27180b306a2e42a` ;
- handoff `ynov-b3-formaflow-hexagonal` 1.0.0 au tag `reference-final`, SHA-256 `611c39062615a5f220b420b5b77ed399217d3bc7b460c6775f1fbf9e1a947750` ;
- référentiel `ynov-b3-formaflow-reference` 1.0.0, SHA-256 `9de0223729f0aa4b99c7d5d2ff260cd25f7540401566bb033b7a383c57b4d921` ;
- CDAN Evidence Kit 1.0.0, SHA-256 `845ff950bf6be288715b6edb0c4a84457c7827bb40caca238a411ba188e6665a`.

`_inputs/` est ignoré et exclu des commits, tags et distributions. Le handoff Hexagonal copié est autonome dans `inputs/architecture-reference/`; l'extrait FormaFlow de `course-start` ne révèle aucun contrat final. Les modèles CDAN adaptés restent formatifs et non notés.

## Handoff Agilité

`handoff/agility-reference/` transmet contexte produit, changement V1/V2, acteurs, dépendances, parcours, contrat, matrice, incident, critères, risques, décisions et questions ouvertes. Il se valide isolément sans l'application. Il ne contient ni code complet, environnement lourd, contenu d'évaluation, backlog résolu ou solution agile produite à la place des étudiants.

