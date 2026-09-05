# Sources exécutables

`src/api/` contiendra l'API FastAPI, le client v1, l'adaptateur v1-v2 et le webhook local. `src/messaging/` contiendra producer, consumers, validation aux frontières, idempotence, retry et dead-letter handling.

L'état initial doit être incomplet mais démarrable. Les TODO sont bornés par des tests et ne révèlent pas directement la solution. Les responsabilités techniques ne doivent pas altérer le contrat public ni importer le modèle interne de FormaFlow Core.
