# 🌌 Le Sift — data pack + resource pack pour Minecraft Java 26.3

> *« Beautiful, vibrant, and teeming with souls. »* — Mojang, à propos du Sift

Ce dépôt contient une **recréation jouable de la dimension du Sift** (la 4ᵉ dimension annoncée au Minecraft Live de
septembre 2026, disponible dans *Minecraft Dungeons II* dès le 29/09/2026 et prévue pour Java/Bedrock en 2027) pour la
**dernière version de Minecraft Java : 26.3** (format de data pack `121.0`, format de resource pack `97.1`).

| Dossier / archive | Contenu |
|---|---|
| `datapack/` → `dist/SiftDataPack.zip` | La dimension, ses biomes, ses structures, ses mécaniques, ses créatures, ses succès |
| `resourcepack/` → `dist/SiftResourcePack.zip` | Modèles 3D et textures des créatures/objets, **6 musiques originales**, langues FR/EN |
| `tools/` | Les générateurs Python (tout est reconstructible : `python3 tools/build.py`) + les validateurs |

> ⚠️ **Honnêteté technique** — je n'ai pas pu lancer Minecraft dans l'environnement de développement (pas d'accès aux
> serveurs Mojang). Tout a été **validé hors-jeu** contre les données vanilla 26.3 (voir [Validation](#-validation))
> mais le pack n'a pas été testé en jeu. Si un détail se comporte mal, ouvrez le journal du jeu : les messages d'erreur
> de chargement pointent directement le fichier fautif.

---

## 🚀 Installation

1. Récupérez `dist/SiftDataPack.zip` **et** `dist/SiftResourcePack.zip`.
2. **Nouveau monde (recommandé)** : *Créer un monde → Plus d'options → Data packs → ajouter `SiftDataPack.zip`*. Ajoutez le resource pack dans *Options → Packs de ressources*.
   **Monde existant** : copiez le zip dans `<monde>/datapacks/`, puis **redémarrez le monde/serveur** (une nouvelle dimension n'est prise en compte qu'au chargement).
3. Serveur : mettez le resource pack dans `server.properties` (`resource-pack=`) ; les modèles de créatures n'apparaissent que côté client avec le resource pack.
4. Dans le jeu : `/function sift:give/starter` (kit de départ), puis suivez [Entrer dans le Sift](#-entrer-dans-le-sift).

> Les créatures, objets et la jauge d'âmes fonctionnent **sans** le resource pack (ils auront alors l'apparence de leurs
> entités de base invisibles / de bâtons), mais l'expérience complète — modèles, musiques, ciel — le requiert.

---

## 🔎 Ce que l'on sait (ou croit) du Sift

Recherches menées sur la presse spécialisée et les wikis (liste des sources en bas). J'ai séparé **ce qui est confirmé**
par Mojang, **ce qui est établi par le jeu *Dungeons II*** et **ce qui est supposé / théorique**.

### ✅ Confirmé par Mojang (Minecraft Live, sept. 2026)
- Quatrième dimension, première nouvelle dimension en plus de 14 ans ; arrive en 2027 sur Java & Bedrock.
- Ambiance : *vibrante et foisonnante d'âmes*, pierre **rouge et orange**, végétation **verte**, **sculk**, liquide dangereux : l'**ichor**.
- Biomes nommés : les **prairies** (*Meadows*, « Singer's Meadow ») et la **Carapace** (*Carapace*).
- Des blocs dangereux changent la façon d'explorer ; des **marées changeantes** affectent le joueur et son entourage.
- De nouvelles créatures, alliées ou hostiles ; « de nouvelles règles à apprendre ».

### 🎮 Établi par *Minecraft Dungeons II* (wiki & presse)
- **Singer's Meadow** : sculk rouge sous une haute herbe bleue/turquoise, fleurs vertes et jaunes, arbres bleus enveloppés de lianes bleu pâle, **bassins d'ichor** ; première zone, près du portail.
- **Carapace** : désert osseux — pierre bleu foncé, sable, **gouffres et ravins**, ichor dans les creux, herbe rouge et jaune par taches.
- **Ichor** : liquide épais multicolore ; enflamme d'un **feu d'âme** les créatures du monde normal (héros, illagers) et **draine leur âme** ; sans effet sur les natifs du Sift.
- **Trois marées** qui influencent la récolte des âmes et le déplacement.
- **Accès** : portail du *Deep Dark* ouvert grâce à la **Machine à notes** (*Note Block Machine*) et au chant des Singers ; aussi par les failles ouvertes par le sceptre du *Grand Illusioner*.
- **Habitants** : *Sifters* (natifs), *Singers* (chanteurs passifs, des « avertisseurs en bonne santé » qui apaisent les Wardens), *Echo Golems* (propulsés par des blocs d'âmes, créés par les Singers). Les illagers envahissent le Sift pour ses ressources et ses âmes. Le **sculk corrompu** vient d'une maladie née dans le Sift ; le sculk sain y prospère.
- **Créatures natives listées** : Blub (la mascotte, lapin bleu clair), Crested Sentinel, Echo Golem, Groobler Sentinel, Licker (cousin du sniffer à grande langue), Nester (bondit après un temps de recharge), Sculk Mage, Sculk Slasher (longues griffes, ruée, images rémanentes), Seedling (petit corps-à-corps), Singer, Sprout (soutien « calmar »), Trill (minuscules effets volants dans le ciel).

### 🤔 Supposé / théories de la communauté
- Le Sift serait le « **Nextworld** » évoqué par l'arbalète *Voidcaller*, ou le « **Fateworld** ».
- Le Blub serait le « visage » du Sift comme l'Enderman l'est pour l'End.
- Un troisième liquide (ichor) arriverait dans le jeu de base, avec des mécaniques proches de *Dungeons II*.

### 🎨 Libertés créatives de ce pack (non canoniques — signalées comme telles)
- Les noms/effets exacts des **trois marées** (Calme / Haute / Basse), la **jauge d'âmes** (0-100), le **voile d'ichor**, le **Diapason** et le **Carillon**.
- Les biomes **Marais d'ichor**, **Crêtes résonantes** et **Résonance de sculk** (cavernes) — le jeu n'en nomme que deux.
- La forme exacte de la Machine à notes, les structures (sanctuaire, avant-poste, obélisque) et toutes les musiques.
- Comme un data pack ne peut pas ajouter de *fluide*, l'ichor est de l'**eau teintée** (couleur propre à chaque biome : magenta, ambre, turquoise, rubis, violet) + un effet de gameplay.

---

## ✨ Ce que contient le pack

### 🌍 La dimension `sift:the_sift`
- Génération **100 % données** (sans mod) : densité sur-mesure, relief de collines douces, **bassins** d'ichor, **crêtes** rouges coiffées de calcite, **ravins** profonds dans la Carapace (remplis d'ichor), grottes et canyons.
- **5 biomes** : *Prairie du Chanteur*, *Carapace*, *Marais d'ichor*, *Crêtes résonantes*, *Résonance de sculk* (souterrain).
- Strates rouge/orange en « bandlands », arbres de bois *warped* à feuillage bleu pâle et lianes, herbe teintée par biome, tapis de sculk, géodes, cristaux d'améthyste, sculk, lanternes d'âmes, ossements géants, minerais (houille, fer, cuivre, or, redstone, lapis, diamant, émeraude…).
- **Ciel permanent** : étoiles éclatantes et lune géante fixe ; couleurs de ciel et de brouillard **par biome** ; particules d'ambiance (notes, âmes, lucioles, cendres blanches…).
- **Horloge `sift:tides` + timeline** : le ciel se teinte au rythme des **marées** (cycle de 24 000 ticks = 3 × 8 000).
- **Structures** : *Sanctuaire du Chanteur* (Machine à notes + coffres), *Avant-poste de Sentinelles*, *Obélisque d'ichor* — avec tables de butin.

### 🌊 Mécaniques
| Mécanique | Description |
|---|---|
| **Machine à notes** | Bloc musical sur un **catalyseur de sculk**, entouré de **4 détecteurs de sculk**. Visez-la et **maintenez clic droit avec le Diapason** : une mélodie retentit et le portail s'ouvre 5 min. |
| **Portail / retour** | Entrez dans le portail (particules) → arrivée sur une plateforme avec une Machine à notes permanente et sa passerelle de retour. `/trigger sift_exit` ramène aussi à l'origine (Overworld, Nether ou End). |
| **Marées** | **Calme** (chute lente + saut renforcé), **Haute** (vitesse, afflux d'âmes, plus de monstres), **Basse** (célérité, âmes plus rares mais doubles). Annonce à l'écran, ciel et brouillard teintés. |
| **Âmes** | Des âmes errantes (orbes) flottent et se ramassent en les touchant. Jauge **0-100** dans la barre d'action ; à 100 : *Débordement* (XP, absorption, régénération). Tuer des natifs rapporte aussi des âmes. |
| **Ichor** | Toute « eau » du Sift est de l'ichor : elle brûle l'âme des joueurs (dégâts + perte d'âmes) et des créatures non natives. Immunité : **Fiole d'ichor** (3 min) / **Éclat d'ichor** (1 min). |
| **Faune** | 11 créatures natives apparaissent selon le **biome** et la **marée** (cf. ci-dessous). |

### 🧿 Créatures (modèles 3D originaux, entités de base invisibles + `item_display` synchronisé)
| Créature | Base | Comportement |
|---|---|---|
| **Blub** | lapin | Passif, mascotte lumineuse |
| **Chanteur (Singer)** | vache | Passif, **chante** (notes), régénère les joueurs proches |
| **Lécheur (Licker)** | vache | Passif, grande langue, mousse et champignons sur le dos |
| **Pousse (Sprout)** | allay | Vole, **soigne** joueurs et natifs alentour |
| **Golem d'écho** | golem de fer | **Allié** invocable (Carillon, 20 âmes, 5 min) |
| **Plantule (Seedling)** | endermite | Petit combattant |
| **Lacérateur de sculk** | endermite | **Ruée** avec **images rémanentes** |
| **Nicheur (Nester)** | husk | **Bond** après recharge |
| **Sentinelle à crête** | squelette | À distance |
| **Sentinelle Groobler** | vindicator | Brute à carapace |
| **Mage de sculk** | sorcière | Jette des potions |

### 🎒 Objets (`/function sift:give/<nom>`) et recettes
`fork` (Diapason du Chanteur) · `chime` (Carillon d'âmes) · `vial` (Fiole d'ichor) · `essence` (Essence d'âme : +20 âmes) · `ichor_shard` (Éclat d'ichor) · `starter` · `all`.
Recettes artisanales pour le Diapason, le Carillon, la Fiole, le catalyseur et le détecteur de sculk (éclat d'écho requis — les Chanteurs en laissent).

### 🏆 Succès
Onglet **« Le Sift »** : 13 succès (chanter pour le Sift, entrer, cueillir une âme, débordement, les trois marées, un chant pur, voile d'ichor, écho fidèle, trois chasses, *Maître du Sift*).

### 🎵 Musiques & art
6 pistes **synthétisées par code** (une par biome + une générale) · textures pixel-art d'objets · 11 modèles 3D à pavés texturés procéduralement · icône de pack et fond d'onglet de succès.

---

## 🛠️ Commandes utiles (opérateurs)
```
/function sift:give/starter        kit de départ (Diapason, Carillon, Fiole, blocs de la Machine)
/function sift:admin/enter         saute directement dans le Sift
/function sift:admin/leave         revient à l'origine
/function sift:admin/tide_0|1|2    force la marée Calme / Haute / Basse
/function sift:admin/build_machine construit la Machine à notes là où vous êtes
/function sift:admin/souls_full    jauge d'âmes pleine
/function sift:admin/kill_mobs     supprime les créatures natives
/execute in sift:the_sift run tp @s ~ 150 ~
/locate biome sift:carapace        (et singers_meadow, ichor_fens, resonant_crags, sculk_resonance)
/place structure sift:singer_shrine
```

---

## ✅ Validation
Faute de client Minecraft, trois outils maintenus dans `tools/` vérifient le pack contre les données **vanilla 26.3**
(dépôts `misode/mcmeta` et `SpyglassMC/vanilla-mcdoc`) :

- `tools/validate.py` : tous les JSON sont valides et **chaque identifiant** (`minecraft:…` / `sift:…`) existe (registres vanilla 26.3 + contenu du pack).
- `tools/cmdcheck.py` : chaque ligne des **111 fonctions** est analysée contre l'**arbre de commandes** 26.3, identifiants et appels `function` compris.
- `tools/shapecheck.py` : compare la forme (clés) de chaque ressource avec les fichiers vanilla du même dossier.

```
python3 tools/build.py      # régénère datapack/ et resourcepack/
python3 tools/package.py    # produit dist/*.zip
```

## 🧱 Notes techniques
- Données basées sur le format **26.3** : attributs d'environnement et **timelines** (nouveauté 26.x), `world_clock`, `material_rule`, bruits `base_octave/octave_count`, loot tables `modifier`/`condition`, etc.
- Les couleurs de ciel/brouillard sont définies **par biome** puis **multipliées** par la teinte de marée de la timeline.
- Les créatures de base sont **invisibles**, silencieuses (pour les passives) et pilotées par un `item_display` suivi à chaque tick (`teleport_duration` pour la fluidité). Un nettoyage supprime les modèles orphelins.
- Si une version ultérieure change un format, modifiez `tools/` puis relancez `build.py` : tout est généré.

## 📚 Sources
- [Engadget — Minecraft is getting a new dimension called The Sift in 2027](https://www.engadget.com/2269867/minecraft-is-getting-a-new-dimension-called-the-sift-in-2027/)
- [Xbox Wire — Minecraft Dungeons II's New Dimension Coming to Minecraft Java & Bedrock](https://news.xbox.com/en-us/2026/09/26/minecraft-new-dimension-sift-dungeons-2/)
- [Minecraft.net — Minecraft Live: September 2026 Recap](https://www.minecraft.net/en-us/article/mclive_sept2026_recap)
- [Minecraft Wiki — The Sift](https://minecraft.wiki/w/The_Sift) · [Dungeons II:The Sift](https://minecraft.wiki/w/Dungeons_II:The_Sift) · [Singer's Meadow](https://minecraft.wiki/w/Dungeons_II:Singer%27s_Meadow) · [Echo Golem](https://minecraft.wiki/w/Dungeons_II:Echo_Golem) · [Singer](https://minecraft.wiki/w/Dungeons_II:Singer) · [Ichor](https://minecraft.wiki/w/Dungeons_II:Ichor)
- [Minecraft Lore Wiki — Sift](https://minecraftlore.miraheze.org/wiki/Sift)
- [Dot Esports](https://dotesports.com/minecraft/news/the-sift-minecraft-live) · [Beebom](https://beebom.com/minecraft-dungeons-2-singer-mob-holds-the-key-to-sift-dimension-portal/) · [TheGamer](https://www.thegamer.com/minecraft-dungeons-2-warden-the-singer-lore/) · [Sportskeeda](https://www.sportskeeda.com/minecraft/the-sift-dimension-minecraft-dungeons-ii-enemies-mechanics-things-know)
- Formats 26.3 : [misode/mcmeta](https://github.com/misode/mcmeta) · [SpyglassMC/vanilla-mcdoc](https://github.com/SpyglassMC/vanilla-mcdoc)

*Projet de fan, non affilié à Mojang/Microsoft. « Minecraft » est une marque de Mojang AB.*
