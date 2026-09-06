# Exemples API locaux

## curl

`curl http://localhost:8000/health`

`curl -X POST "http://localhost:8000/api/v2/events" -H "Content-Type: application/json" --data-binary "@contracts/examples/training-session-created.v2.valid.json"`

## PowerShell

`Invoke-RestMethod http://localhost:8000/health`

`Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v2/events -ContentType application/json -InFile contracts/examples/training-session-created.v2.valid.json`

Ajouter `?publish=true` pour publier localement après validation. Sans ce paramètre, la route démontre uniquement validation et adaptation. Les erreurs ont un code stable, un message avec chemin et le correlation ID.

