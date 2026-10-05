advancement revoke @s only sift:kill/native
execute unless dimension sift:the_sift run return 0
scoreboard players add @s sift.souls 8
particle minecraft:sculk_soul ~ ~1 ~ 0.4 0.6 0.4 0.05 14
execute if score @s sift.souls matches 100.. run function sift:souls/overflow
