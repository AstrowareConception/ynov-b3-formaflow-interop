# Sources exécutables

`src/astrobridge/api/` contient l'API FastAPI V1/V2 et le webhook local. `src/astrobridge/messaging/` contient le producteur, les consommateurs, la topologie RabbitMQ, le retry et la dead-letter queue. Les adaptateurs et la validation aux frontières se trouvent dans `src/astrobridge/contracts/`.

`course-start` reste volontairement incomplet mais démarrable. Ses TODO sont bornés par des tests et ne révèlent pas directement la solution. Les responsabilités techniques n'altèrent pas le contrat public et n'importent pas le modèle interne de FormaFlow Core.
