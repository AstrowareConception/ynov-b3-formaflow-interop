# Matrice de compatibilité

| Writer | Reader | Résultat | Mécanisme |
|---|---|---|---|
| JSON V1 | JSON V1 | compatible | direct |
| JSON V2 | JSON V1 | compatible sous condition | downcast explicite |
| Protobuf V2 | Protobuf V1 | wire-compatible | champs inconnus, numéros non réutilisés |
| Avro V1 | Avro V2 | compatible | défauts reader |
| Avro V2 | Avro V1 | compatible | alias et champs ignorés |
| capacité texte | lecteur V2 | incompatible | changement de type |

