# Benchmark de sérialisation V1

Python : `3.12.6` ; plateforme : `Windows-11-10.0.26200-SP0`.
Graine `20260906`, warmup 2, 9 répétitions. Génération du corpus exclue.

| Événements | Format | Octets médiane | Sérialisation médiane ms | p95 ms | Désérialisation médiane ms | p95 ms |
|---:|---|---:|---:|---:|---:|---:|
| 1 | json | 471 | 0.0043 | 0.0077 | 0.0036 | 0.0367 |
| 1 | protobuf | 240 | 0.0032 | 0.0043 | 0.0028 | 0.0032 |
| 1 | avro | 223 | 0.0688 | 0.1272 | 0.0650 | 0.0866 |
| 10 | json | 4708 | 0.0389 | 0.1242 | 0.0289 | 0.0417 |
| 10 | protobuf | 2400 | 0.0288 | 0.0293 | 0.0248 | 0.0269 |
| 10 | avro | 2230 | 0.7591 | 1.1603 | 0.6869 | 0.8964 |
| 100 | json | 47074 | 0.4023 | 0.4801 | 0.3117 | 0.4472 |
| 100 | protobuf | 24000 | 0.2687 | 0.3721 | 0.2526 | 0.4044 |
| 100 | avro | 22300 | 8.7312 | 9.5571 | 7.7825 | 8.1848 |

## Interprétation bornée

Ces mesures décrivent ce corpus, ces codecs et cette machine. Taille, vitesse, lisibilité, gouvernance de schéma et écosystème restent des critères distincts. Aucun format n'est universellement meilleur.
