# Benchmarks et preuves

## Protocole

Le corpus représente les mêmes événements dans les trois formats. `benchmarks/run.py` mesure taille encodée, sérialisation et désérialisation après vérification de l'équivalence.

Le protocole fixe la graine, sépare la génération du corpus, effectue un warmup, répète les mesures et publie médiane et p95 avec le contexte Python et matériel.

## Emplacements

- corpus déterministe : `benchmarks/corpus/` ;
- résultats bruts lisibles par machine : `benchmarks/raw/` ;
- synthèses Markdown : `benchmarks/reports/`.

Les preuves complémentaires couvrent round-trips, compatibilité V1/V2, événement nominal, doublon, poison, DLQ et idempotence.

## Interprétation

Une mesure locale ne démontre pas qu'un format est toujours meilleur. La recommandation distingue résultat observé, coût d'outillage, lisibilité, gouvernance du schéma, écosystème et durée de vie du contrat. Les captures d'écran ne remplacent pas une sortie textuelle reproductible.
