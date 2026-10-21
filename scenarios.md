# 1
achete > 6

achete > stock

achete -1

achete 0

achete 2 ticket avec code promo exp

| Scénario | Règle ou contrainte concernée | Statut attendu (400 / 404 / 409 / 422) | Pourquoi CE statut ? |
|---|---|---|---|
| Acheter 7 tickets | RM3 | 400 | Enfreint la RM |
| Acheter plus de ticket que le stock dispo | RM1 | 409 | Conflit de stock aevc des tickets déja reservés |
| Acheter -1 ticket | RM3 | 400 | Enfreint la RM3 : 1-6 tickets |
| Acheter 0 tciket | RM3 | 400 | Enfreint la RM3 : 1-6 tickets |
| Acheter 2 tickets avec un code promo expiré | RM4 | 400 | ? |
| Acheter des tickets avec un code promo inexistant | RM4 | 404 | ? |
| Acheter des "B" tickets | RM3 | 422 | Valeur non autorisée |
| Acheter 2 ticket d'un catégorie, 4 d'une autre et 1 d'une autre | RM3 | 400 | Enfreint la RM max 6 tickets |
