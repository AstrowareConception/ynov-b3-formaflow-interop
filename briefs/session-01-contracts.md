# Séance 1 - Du message ambigu au contrat

**Durée :** 4 h, dont 2 h FFP et 2 h TDP. **Contexte :** AstroBridge doit publier un fait de création sans exposer le modèle interne.

## Objectifs et apport FFP

Distinguer événement métier et événement d'intégration, expliciter un mapping, découvrir JSON Schema 2020-12, invariants, propriété et erreurs lisibles.

## Travail pratique

Partir de `fixtures/valid/starter-session.json`, `fixtures/invalid/ambiguous-message.json` et `src/astrobridge/application/mapping.py`. Construire le mapping et le contrat, puis des exemples synthétiques valides et invalides.

## Production formative et preuve CDAN

Produire un contrat testé et une fiche de preuve transférable. Auto-vérifier les chemins d'erreur, l'absence de donnée personnelle, le refus des propriétés imprévues et la différence domaine/intégration.

## Commandes, erreurs fréquentes et checkpoint

`python -m pytest tests/unit tests/contracts` puis `python scripts/tasks.py contracts`. Éviter les dates locales, montants flottants, identifiants instables et copies d'ORM. Fin : `checkpoint-contract`.

