# Checkpoints et branches

## Tags formateur

Le bundle de référence distribue les sept tags annotés suivants :

| Tag | État |
|---|---|
| `course-start` | environnement guidé et lacunes pédagogiques contrôlées |
| `checkpoint-contract` | mapping, JSON Schema, exemples et tests |
| `checkpoint-serialization` | JSON, Protobuf, Avro, benchmark et matrice |
| `checkpoint-async` | RabbitMQ, webhook, idempotence, retry et DLQ |
| `checkpoint-versioning` | V2, compatibilité, API, migration et incident |
| `reference-final` | référence formateur consolidée |
| `interop-v1.0.0` | alias de release du même commit final |

Chaque tag se valide avec la commande indiquée dans son annotation. Un checkpoint conforme à son stade n'est pas présenté comme défectueux.

## Branches étudiant

Les tags formateur sont immuables pour le parcours distribué. Chaque binôme peut créer localement une branche `work/<team-id>` depuis `course-start`. Cette branche de travail n'est ni un tag canonique, ni une branche d'évaluation, ni un mécanisme de rendu noté.

Si un groupe n'atteint pas un checkpoint, la séance suivante peut repartir du tag canonique intermédiaire. La continuité du cours ne dépend pas de la réussite d'une étape précédente.

Les commits décrivent une intention observable et n'incluent aucun secret, environnement virtuel ou résultat local non reproductible.
