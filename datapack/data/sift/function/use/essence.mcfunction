advancement revoke @s only sift:use/essence
scoreboard players add @s sift.souls 20
particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.05 14
execute if score @s sift.souls matches 100.. run function sift:souls/overflow
