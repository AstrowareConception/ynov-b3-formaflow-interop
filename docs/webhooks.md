# Webhook local

Le sender signe `timestamp.idempotencyKey.body` en HMAC-SHA256 avec un secret factice configurable. Le récepteur local refuse signature invalide, horodatage hors fenêtre de cinq minutes et réutilisation d'une clé. Le client applique timeout et trois tentatives bornées. Cette démonstration ne contacte aucun service externe.

