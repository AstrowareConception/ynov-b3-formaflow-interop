# Checkpoints et branches

## Règles Git

- le formateur publie `course-start` et `reference-final` ;
- chaque binôme crée `work/<team-id>` depuis `course-start` ;
- chaque checkpoint correspond à un état exécutable et documenté ;
- les commits décrivent une intention pédagogique observable ;
- aucun secret, environnement virtuel ou résultat non reproductible n'est versionné ;
- un checkpoint est formatif et n'est pas une note.

## Contrat des checkpoints

| Tag | Contenu minimal | Contrôle |
|---|---|---|
| `checkpoint-contract` | JSON Schema, mapping, exemples et tests | `make contracts && make test` |
| `checkpoint-serialization` | Trois contrats, benchmark et matrice | `make contracts && make benchmark && make test` |
| `checkpoint-async` | Producer, consumers, DLQ, idempotence et preuves | `make smoke && make test` |
| `checkpoint-versioning` | Migration v1-v2, compatibilité, ADR et trace CDAN | `make quality` |

Si un groupe n'atteint pas un checkpoint, la séance suivante peut repartir d'un état canonique intermédiaire distribué par le formateur. La continuité du cours ne dépend jamais d'une réussite antérieure.
