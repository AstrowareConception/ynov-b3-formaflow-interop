# Checkpoints et états canoniques

| Tag | Propriétaire | Contenu minimal |
|---|---|---|
| `course-start` | formateur | entrée DDD figée, contrats et services incomplets, fixtures et scénarios |
| `checkpoint-contract` | formateur | JSON Schema, mappings, exemples et tests de contrat consolidés |
| `checkpoint-serialization` | formateur | JSON, Protobuf, Avro, mesures brutes, compatibilité et ADR de choix |
| `checkpoint-async` | formateur | producteur, consommateurs, webhook, idempotence, DLQ et preuves d'exploitation |
| `checkpoint-versioning` | formateur | stratégies de versionnement, compatibilité et dossier v1-v2 consolidés |
| `reference-final` | formateur | version corrigée et paquet `handoff/agility-reference/` publiable |
| `interop-v1.0.0` | formateur | alias de release locale pointant exactement sur `reference-final` |

Les binômes travaillent dans `work/<team-id>`. Les tags sont des états communs de reprise et ne créent aucune note. Le temps individuel final reste formatif et non noté.

Chaque tag est annoté avec sa commande de validation et son prédécesseur. Pour une validation native, exécuter `python scripts/validate_repo.py --stage <tag>` puis les tests présents au stade. Aucun tag ou branche d'évaluation n'appartient à cette histoire.
