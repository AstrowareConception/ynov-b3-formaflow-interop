# Séance 2 - Trois représentations, un même sens

**Durée :** 3 h, dont 1 h 30 FFP et 1 h 30 TDP. **Contexte :** le contrat V1 doit être encodé en JSON, Protobuf et Avro.

## Objectifs et apport FFP

Comprendre schéma, génération, round-trip, évolution par format et limites d'un benchmark.

## Travail pratique

À partir du checkpoint précédent, compléter `.proto` et `.avsc`, générer le code, vérifier l'équivalence et mesurer un corpus déterministe après warmup.

## Production formative et preuve CDAN

Produire matrice writer/reader, résultats bruts et benchmark argumenté. Auto-vérifier graine, répétitions, médiane, percentiles, contexte et absence de conclusion universelle.

## Commandes, erreurs fréquentes et checkpoint

`python scripts/tasks.py generate`, `contracts`, `benchmark`, `test-contracts`. Ne pas comparer des objets de sens différent ni inclure la génération dans le temps d'exécution. Fin : `checkpoint-serialization`.

