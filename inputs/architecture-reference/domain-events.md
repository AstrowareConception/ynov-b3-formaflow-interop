# Événements de domaine locaux

| Événement | Moment | Données réellement nécessaires | Publication locale |
|---|---|---|---|
| `EnrollmentConfirmed` | inscription confirmée | identifiant inscription, instant UTC | après transaction réussie |
| `EnrollmentCancelled` | première annulation acceptée | identifiant inscription, instant UTC, pourcentage décidé | après transaction réussie, une fois |

Ces classes ne sont ni des événements d'intégration, ni des messages de broker, ni des journaux techniques. Aucun événement n'est produit sur refus ou répétition idempotente.
