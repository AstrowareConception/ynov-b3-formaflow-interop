# Contrats

Ce dossier accueillera trois représentations de `TrainingSessionCreated` :

- `json-schema/` : sources JSON Schema 2020-12, exemples valides et invalides ;
- `protobuf/` : fichiers `.proto` et configuration de génération ;
- `avro/` : fichiers `.avsc` et scénarios writer/reader.

Le sens métier commun et les règles de mapping sont documentés hors du code généré. Les versions v1/v2 doivent coexister assez longtemps pour exécuter les tests de compatibilité. Aucun fichier généré ne devient la source de vérité.
