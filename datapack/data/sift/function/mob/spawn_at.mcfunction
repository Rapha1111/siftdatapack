execute if block ~ ~ ~ minecraft:water run return 0
execute if block ~ ~-1 ~ minecraft:water run return 0
scoreboard players set #h sift.tmp 0
execute if score #tide sift.tmp matches 0 if predicate sift:chance/spawn_hostile_calm run scoreboard players set #h sift.tmp 1
execute if score #tide sift.tmp matches 1 if predicate sift:chance/spawn_hostile_surge run scoreboard players set #h sift.tmp 1
execute if score #tide sift.tmp matches 2 if predicate sift:chance/spawn_hostile_ebb run scoreboard players set #h sift.tmp 1
execute store result score #r sift.tmp run random value 1..100
execute if biome ~ ~ ~ sift:singers_meadow run function sift:mob/pick_meadow
execute if biome ~ ~ ~ sift:carapace run function sift:mob/pick_carapace
execute if biome ~ ~ ~ sift:ichor_fens run function sift:mob/pick_fens
execute if biome ~ ~ ~ sift:resonant_crags run function sift:mob/pick_crags
particle minecraft:sculk_soul ~ ~0.5 ~ 0.3 0.5 0.3 0.03 8
