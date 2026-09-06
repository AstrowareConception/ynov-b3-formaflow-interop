# Glossaire

- API : frontière HTTP synchrone.
- Avro writer/reader : schémas employés respectivement à l'écriture et à la résolution de lecture.
- DLQ : file de dernier recours après retry borné.
- Événement métier : fait interne au modèle du domaine.
- Événement d'intégration : fait public stable pour consommateurs identifiés.
- Idempotence : même `eventId`, aucune répétition incontrôlée de l'effet.
- Protobuf unknown field : champ wire non connu du reader, ignoré et préservé selon l'implémentation testée.
- Publisher confirm : confirmation broker de prise en charge de la publication.
- Redelivery : nouvelle livraison après absence d'ack.
- Upcast/downcast : adaptation explicite vers une version plus récente ou plus ancienne.
- Webhook : appel HTTP sortant signé et retenté avec borne.

