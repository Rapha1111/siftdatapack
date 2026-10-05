execute store result storage sift:tmp x int 1 run scoreboard players get @s sift.ox
execute store result storage sift:tmp y int 1 run scoreboard players get @s sift.oy
execute store result storage sift:tmp z int 1 run scoreboard players get @s sift.oz
effect give @s minecraft:slow_falling 6 0 true
execute if score @s sift.odim matches 0 run function sift:portal/return_overworld with storage sift:tmp
execute if score @s sift.odim matches 1 run function sift:portal/return_nether with storage sift:tmp
execute if score @s sift.odim matches 2 run function sift:portal/return_end with storage sift:tmp
execute unless score @s sift.odim matches 0..2 in minecraft:overworld run tp @s 0 120 0
title @s actionbar {"text":"Vous quittez le Sift.","color":"gray"}
