# Tests

Le futur jeu de tests couvrira :

- exemples JSON valides et invalides ;
- chemins d'erreur de validation ;
- génération et round-trip Protobuf/Avro ;
- équivalence sémantique des trois formats ;
- compatibilité writers/readers v1-v2 ;
- routage RabbitMQ, acknowledgements et publisher confirms ;
- redelivery, idempotence, retry borné et DLQ ;
- signature, timeout, 5xx et rejeu du webhook ;
- maintien d'un client API v1 pendant la migration.

Les tests déterministes s'exécutent par `make test`. Les tests nécessitant RabbitMQ sont identifiés clairement et disposent d'un timeout.
