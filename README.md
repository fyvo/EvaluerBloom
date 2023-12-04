# Bloume
Bloom, un modèle de langue pour le francais ?

## Contexte et Objectifs

### Contexte
Le projet [BigScience](https://bigscience.huggingface.co/) a permis d'entraîner un grand modèle de langue multilingue selon les principes de la science ouverte. Ce modèle existe en plusieurs tailles, le plus petit comprenant 560M de paramètres, le plus gros 176B de paramètres. Ce modèle est présenté dans une [publication collective](https://arxiv.org/abs/2211.05100); d'autres publications ont été réalisées également pour documenter des aspects particuliers du modèle (par exemple le coût carbone de l'apprentissage https://arxiv.org/abs/2211.02001), ou encore une dérivation du modèle par fine-tuning donnant lieux aux familles [mT0 et Bloomz](https://arxiv.org/abs/2211.01786).

Ce modèle est doublement intéressant: (a) il est complètement disponible, et tous les détails concernant son apprentissage (y compris les corpus) et son exploitation sont publics, ce qui permet d'étudier son fonctionnement en profondeur; (b) par rapport à d'autres modèles il a été entrainé avec un mélange de documents qui accorde une large part au français (15% des données d'apprentissage) et aux langues romanes (35% des données), et dans un autre genre, aux langages de programmation.

Dans le cadre de la préparation de la [publication "générale"](https://arxiv.org/abs/2211.05100) des premiers éléments d'évaluation du modèle ont été produits pour comparer ce modèle avec des modèles comparables en taille et en ambition. Ainsi, les performances de BLOOM comme système de traduction automatique ont été mesurées en étudiant quelques aspects: importance de la formulation de l'instruction (prompt), performance pour divers couples de langues en fonction de la taille des données d'apprentissage (en particulier depuis et vers le français), importance des grands contextes. 

### Résultats
Ce projet a permis de tester BLOOM pour un large évantail de tâches standard pour le traitement automatique de la langue française (en réutilisant certaines tâches de [FLUE](https://github.com/getalp/Flaubert/tree/master/flue) ainsi que d'autres tâches équivalentes comme WikiAnn ou mSum) qui pourraient être mise à disposition de la communauté. Les résultats obtenus confirment les principaux résultats observés sur la langue anglaise, et mettent en évidence le (léger) bénéfice de disposer d'invites rédigés en langue française. Ces résultats fournissent également un ensemble de résultats de base qui pourront servir dans le cadre de comparaison avec des modèles plus récents ou de plus petite taille.

En parallèle nous avons pu documenter et faciliter l'utilisation de BLOOM pour en faciliter l'usage sur Jean Zay, et réaliser diverses améliorations des divers outils logiciels ([promptsource](https://github.com/bigscience-workshop/promptsource) et[lm-harness](https://github.com/EleutherAI/lm-evaluation-harness)) utilisés pour l'évaluation.

## Ressources

### Modèles
Les modèles produits par BigScience, disponibles depuis le Hub huggingface (et sur JZ)
- [Bloom](https://huggingface.co/bigscience/bloom) dans toutes ses versions, un modèle de langue causal multilingue (pur décodeur)
- [Bloomz et mT0](https://huggingface.co/bigscience/bloomz), dérivés respectivement de Bloom et mT5

### Outils d'évaluation

- [promptsource](https://github.com/ncassereau-idris/promptsource)
- [eval-harness](https://github.com/bigscience-workshop/lm-evaluation-harness)

### Tâches et datasets

- Classification de sentiments: [Amazon_reviews_multi](https://huggingface.co/datasets/amazon_reviews_multi)
- Implication textuelle: [XNLI](https://huggingface.co/datasets/xnli/)
- Entités nommées: [wikiNER_fr](https://huggingface.co/datasets/Jean-Baptiste/wikiner_fr) et [quaero](https://huggingface.co/datasets/bigbio/quaero)
- Traduction automatique: [WMT_14](https://huggingface.co/datasets/wmt14xnli) et [Flores](https://huggingface.co/datasets/facebook/flores)
- Résumé de textes: [wiki_lingua](https://huggingface.co/datasets/GEM/wiki_lingua)
- Biais et stéréotypes: [Crows_pairs_multilingual](https://huggingface.co/datasets/BigScienceBiasEval/crows_pairs_multilingual) et [bias_shades](https://huggingface.co/datasets/BigScienceBiasEval/bias-shades)
