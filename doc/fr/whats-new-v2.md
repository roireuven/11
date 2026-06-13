# Quoi de neuf dans la v2.3 / v2.4

Ce guide résume les principales fonctionnalités ajoutées dans **stable v2.3** et **stable v2.4** de HotelRestaurantMini-MartManagement.

**Sites stables en direct :**

| Version | URL |
|---------|-----|
| **v2.3** | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) |
| **v2.4** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) |
| **Développement** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

---

## Interface complète en 21 langues

L'interface utilisateur de l'application Web est disponible dans **21 langues** : anglais, espagnol, français, allemand, japonais, coréen, arabe, hindi, thaï, vietnamien, indonésien, turc, russe, italien, néerlandais, polonais, hébreu, laotien, portugais (Brésil), chinois (simplifié) et chinois (traditionnel).

### Où changer de langue

| Écran | Comment |
|--------|-----|
| **Connexion / configuration** | Liste déroulante des langues dans l'en-tête (avant la connexion) |
| **Après la connexion** | Sélecteur de paramètres régionaux dans la barre supérieure ou **Localisation** dans le menu |
| **Paramètres** | Section de langue de l'application |

La préférence est enregistrée dans le stockage du navigateur (`hotel_mgr_uiLocale`).

### RTL (de droite à gauche)

**Arabe** et **Hébreu** activent la mise en page RTL pour l'ensemble de l'application. Les formulaires modaux utilisent un alignement amélioré afin que les étiquettes et les entrées soient lues correctement dans les langages LTR et RTL.

---

## Première configuration (traduit)

L'assistant de configuration est entièrement localisé :

- Nom de l'entreprise/de l'hôtel
- Texte d'en-tête du système
- Champs de nom d'utilisateur, d'e-mail et de mot de passe de l'administrateur
- Tous les boutons et messages de validation

Après la configuration, le nom de l'hôtel est stocké et affiché dans l'en-tête de l'application là où il est configuré.

---

## Actions rapides du tableau de bord (grille PMS)

Le **Tableau de bord** affiche une grille de boutons bleus **+** pour les tâches courantes :

| Bouton | Ouvre |
|--------|--------|
| Ajouter une pièce | Nouvelle forme de chambre |
| Ajouter une réservation | Nouveau formulaire de réservation |
| Ajouter un invité | Nouveau formulaire d'invité |
| Ajouter une tâche | Nouveau ticket de maintenance |
| Ajouter un service | Nouvelle demande de service |
| Ajouter une facture | Nouveau formulaire de facture |
| Ajouter du stock | Nouvel article d'inventaire |
| Ajouter un menu | Nouvel élément de menu |
| Ajouter un article de boutique | Nouvel article de magasin / supérette |
| Ajouter un utilisateur | Nouveau compte du personnel |

**Remarque :** *Ajouter un nettoyage* et *Ajouter une transaction* ont été supprimés de cette grille (v2.4). Utilisez la barre latérale pour **Housekeeping** et **Transactions** si nécessaire.

---

## Formulaires modaux traduits

Les boîtes de dialogue d'ajout et de modification sont localisées dans les 21 langues, notamment :

- **Maintenance** — nouveau ticket (salle, priorité, problème, notes)
- **Facture** — ajouter/modifier (invité, chambre, dates, montants, statut du paiement)
- **Inventaire** — ajouter/modifier un article (nom, code-barres, catégorie, quantité, disponibilité du point de vente)
- **Élément de menu** — ajouter/modifier (nom, icône, prix, catégorie, image, lien boursier)
- **Article du magasin** — ajouter/modifier (nom, prix, catégorie, icône d'étagère, code-barres, stock)- **Compte utilisateur** — ajouter/modifier (nom, email, mot de passe, rôle)

Les étiquettes de téléchargement d’images (« depuis l’appareil », « ou URL de l’image ») suivent la langue active.

---

## Réservation → Nouvel invité

Lors de la création d'une **réservation**, si le client n'est pas encore dans l'annuaire :

1. Appuyez sur **+ Nouveau voyageur** (ou équivalent) sur le formulaire de réservation.
2. Remplissez le modal **Nouvel invité** (nom, passeport, nationalité, date de naissance, mode de paiement, contact, notes).
3. Appuyez sur **Ajouter un invité et revenir** : vous revenez à la réservation avec le nouveau invité sélectionné.

Le sélecteur de nationalité (liste de recherche) est également traduit.

---

##Documents

- Ce guide **Quoi de neuf** est disponible dans les 21 langues de documentation.
- Ouvrez les documents depuis l'application : **barre supérieure → Documentation**, **☰ Aide → Documentation** ou **navigation inférieure → Docs**.
- URL autonome : `/doc/?lang={code}#/whats-new-v2`

---

## Pour les administrateurs

| Tâche | Où |
|------|--------|
| Former le personnel au changement de langue | [Localization](localization.md) |
| Configurer la propriété après la mise à niveau | [Settings & configuration](settings-and-configuration.md) |
| Déployer les mises à jour | [Deployment](deployment.md) — `npm run deploy:stable` publie vers v2.3 et v2.4 |

---

## Guides associés

- [Localization](localization.md) — langues, RTL, fichiers de paramètres régionaux
- [First-time setup](first-time-setup.md) — configuration initiale
- [Navigation & UI](navigation-and-ui.md) — tableau de bord, barre latérale, navigation mobile
- [Hotel operations](hotel-operations.md) — réservations et invités
- [Deployment](deployment.md) — développement vs stable v2.3 / v2.4