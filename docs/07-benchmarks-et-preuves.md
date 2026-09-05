# Benchmarks et preuves

## Protocole minimal

Le corpus représente exactement les mêmes objets dans les trois formats. Le script mesure au minimum taille encodée, temps de sérialisation et temps de désérialisation.

Le protocole documente :

- versions de Python et des bibliothèques ;
- machine et conditions d'exécution utiles ;
- taille et distribution du corpus ;
- warm-up et nombre de répétitions ;
- médiane et mesure de dispersion ;
- exclusion éventuelle du coût de génération ou d'initialisation ;
- vérification préalable de l'équivalence sémantique.

## Règles d'interprétation

Une mesure locale ne démontre pas qu'un format est toujours meilleur. La recommandation distingue résultat observé, coût d'outillage, lisibilité, écosystème, durée de vie du contrat et besoin opérationnel.

## Preuves attendues

- résultats bruts versionnés dans `benchmarks/results/` ;
- synthèse lisible et commande exacte de reproduction ;
- tests d'équivalence du décodage ;
- journaux d'un événement nominal, d'un doublon et d'un poison message ;
- état de la DLQ et preuve d'idempotence ;
- tests de compatibilité v1-v2 ;
- limites et incidents rencontrés.

Les captures d'écran ne remplacent jamais une sortie textuelle ou un test automatisé lorsqu'une preuve reproductible est possible.
