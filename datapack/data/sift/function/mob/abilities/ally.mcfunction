scoreboard players add @s sift.age 1
particle minecraft:sculk_soul ~ ~1.2 ~ 0.4 0.6 0.4 0.01 2
execute if score @s sift.age matches 300.. run function sift:mob/ally_fade
