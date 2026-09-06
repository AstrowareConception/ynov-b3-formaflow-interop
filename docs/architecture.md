# Architecture AstroBridge

Le domaine amont reste propriétaire de `InternalTrainingSession`. L'application mappe explicitement ce modèle vers une enveloppe d'intégration stable. Les contrats JSON, Protobuf et Avro représentent le même sens ; aucun codec n'est le modèle métier.

L'adaptateur HTTP expose santé, disponibilité, validation V1/V2, publication optionnelle, webhook local et preuves synthétiques. L'adaptateur RabbitMQ configure un topic exchange, deux files indépendantes, retry à TTL et DLQ. Les consommateurs écrivent leurs effets dans un store local idempotent. Ce store est pédagogique et n'est pas présenté comme une solution distribuée de production.

Le trajet asynchrone est au moins une fois : publisher confirm, message persistant, ack manuel après effet ou republication, et `eventId` comme clé d'idempotence. Le `correlationId` traverse message et preuve.

V2 est validée à sa frontière puis downcastée explicitement vers V1 pour le routage historique. Le rollback coupe V2 sans retirer V1 ni réutiliser de numéro Protobuf.

Les sources et rendus des huit vues sont dans `docs/diagrams/`. `python scripts/render_diagrams.py --check` détecte un rendu absent ou obsolète.

