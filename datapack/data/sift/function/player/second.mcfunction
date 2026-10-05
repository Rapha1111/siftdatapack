execute if score #tide sift.tmp matches 0 run effect give @s minecraft:slow_falling 4 0 true
execute if score #tide sift.tmp matches 0 run effect give @s minecraft:jump_boost 4 1 true
execute if score #tide sift.tmp matches 1 run effect give @s minecraft:speed 4 0 true
execute if score #tide sift.tmp matches 2 run effect give @s minecraft:haste 4 0 true
execute store result score @s sift.tmp if entity @e[type=item_display,tag=sift.wisp,distance=..32]
execute if score @s sift.tmp matches ..11 if score #tide sift.tmp matches 0 if predicate sift:chance/wisp_calm run function sift:souls/spawn_wisp
execute if score @s sift.tmp matches ..17 if score #tide sift.tmp matches 1 if predicate sift:chance/wisp_surge run function sift:souls/spawn_wisp
execute if score @s sift.tmp matches ..7 if score #tide sift.tmp matches 2 if predicate sift:chance/wisp_ebb run function sift:souls/spawn_wisp
execute if block ~ ~ ~ minecraft:water unless score @s sift.veil matches 1.. run function sift:ichor/burn_player
function sift:mob/spawner
function sift:player/hud
function sift:sift/check_mastery
