# Séance 4 - Faire évoluer sans casser

**Durée :** 3 h, dont 1 h FFP et 2 h TDP. **Contexte :** V2 ajoute mode et lieu de diffusion tout en préservant un ancien client V1.

## Objectifs et apport FFP

Comparer compatibilités JSON, Protobuf et Avro, concevoir adaptateur, dépréciation, rollback et migration.

## Travail pratique

Tester `/api/v1` et `/api/v2`, le downcast V2 vers V1, les cas incompatibles et compléter le handoff Agilité. Un temps individuel formatif non noté de 30 minutes clôt la séance ; aucun contenu associé n'est dans le dépôt.

## Production formative et preuve CDAN

Produire stratégie de versionnement, matrice, incident et transfert. Auto-vérifier ancien client, défauts explicites, champs réservés et headers de dépréciation.

## Commandes, erreurs fréquentes et checkpoint

`python scripts/tasks.py test-compatibility`, `quality`, `validate-handoff`. Ne pas renommer silencieusement ni supposer l'ajout toujours compatible. Fin : `checkpoint-versioning`.

