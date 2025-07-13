import structlog

logger = structlog.get_logger()

def get_panier(session, magasin_id):
    panier = session.get("panier", {})
    return panier.get(str(magasin_id), {})

def ajouter_au_panier(session, magasin_id, produit_id, quantite):
    panier = session.get("panier", {})

    magasin_id_str = str(magasin_id)
    produit_id_str = str(produit_id)
    quantite = int(quantite)

    if magasin_id_str not in panier or not isinstance(panier[magasin_id_str], dict):
        panier[magasin_id_str] = {}

    if produit_id_str in panier[magasin_id_str]:
        panier[magasin_id_str][produit_id_str] += quantite
    else:
        panier[magasin_id_str][produit_id_str] = quantite

    session["panier"] = panier
    session.modified = True

def retirer_du_panier(session, magasin_id, produit_id):
    panier = session.get("panier", {})
    logger.info("Panier avant retrait", panier=panier)

    magasin_id_str = str(magasin_id)
    produit_id_str = str(produit_id)

    magasin_panier = panier.get(magasin_id_str)
    if not isinstance(magasin_panier, dict):
        logger.warning("Panier magasin invalide ou inexistant", magasin_id=magasin_id_str)
        return

    if produit_id_str in magasin_panier:
        magasin_panier.pop(produit_id_str)
        logger.info("Produit retiré", produit_id=produit_id_str)
    else:
        logger.warning("Produit non présent dans panier", produit_id=produit_id_str)

    if not magasin_panier:
        panier.pop(magasin_id_str)
        logger.info("Panier magasin vidé, supprimé du panier global", magasin_id=magasin_id_str)

    session["panier"] = panier
    session.modified = True
    logger.info("Panier après retrait", panier=session["panier"])

def vider_panier(session, magasin_id):
    panier = session.get("panier", {})
    if str(magasin_id) in panier:
        del panier[str(magasin_id)]
        session.modified = True

def get_quantite(session, magasin_id, produit_id):
    return get_panier(session, magasin_id).get(str(produit_id), 0)
