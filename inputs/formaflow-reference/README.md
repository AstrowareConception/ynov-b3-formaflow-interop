# Extrait pédagogique FormaFlow Reference

Extrait volontairement limité de `ynov-b3-formaflow-reference` version `1.0.0`, archive SHA-256 `9de0223729f0aa4b99c7d5d2ff260cd25f7540401566bb033b7a383c57b4d921`, copié le `2026-09-06`.

Le contrat JSON Schema canonique et son mapping résolu ne sont pas copiés : ils constituent une référence formateur dévoilée seulement aux checkpoints concernés. Toutes les données ci-dessous sont synthétiques.

## Vocabulaire et acteurs utiles

- Une **formation** (`TRN-####`) décrit l'offre ; une **session** (`SES-YYYY-####`) planifie cette formation.
- `training-management` possède la création de session.
- AstroBridge adapte le fait source en événement d'intégration.
- Administration et Notification sont deux consommateurs indépendants ; Notification ne produit qu'une trace synthétique.

## Invariants et données fonctionnelles

- Une session appartient à une formation de référence.
- Sa fin est strictement postérieure à son début pour ce module.
- Sa capacité est un entier strictement positif.
- Un prix est un montant entier en unité mineure et une devise explicite.
- Le statut initial est `SCHEDULED`.
- Un événement d'intégration a un identifiant stable, une version, un instant UTC et un identifiant de corrélation.
- Les données personnelles et structures ORM sont exclues.

## Exemples non résolus

Les fichiers de `fixtures/` illustrent volontairement des noms, formats et unités à discuter. Ils ne constituent ni le mapping final, ni un contrat final, ni une interprétation de benchmark.

