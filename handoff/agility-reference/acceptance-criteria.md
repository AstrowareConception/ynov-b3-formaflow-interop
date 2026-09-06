# Critères d'acceptation

- Un événement V2 valide porte mode et lieu synthétiques.
- Un ancien client V1 reste fonctionnel grâce au downcast identifié.
- JSON, Protobuf et Avro ont des scénarios writer/reader automatisés.
- Un doublon ne crée pas de second effet par consommateur.
- Retry est borné et un poison atteint la DLQ.
- Les appels V1 exposent dépréciation et Sunset.
- Le rollback conserve V1, les identifiants et l'idempotence.
- Aucune donnée personnelle, notification réelle ou secret n'est utilisé.

