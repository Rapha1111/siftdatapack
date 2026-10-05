execute if entity @s[gamemode=!creative,gamemode=!spectator] run damage @s 2 minecraft:magic
particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.02 14
particle minecraft:sculk_soul ~ ~1.2 ~ 0.3 0.4 0.3 0.02 6
scoreboard players remove @s sift.souls 8
scoreboard players operation @s sift.souls > #0 sift.const
playsound minecraft:block.fire.extinguish player @a ~ ~ ~ 0.6 0.6
title @s actionbar {"text":"L’ichor brûle votre âme !","color":"dark_purple","bold":true}
effect give @s minecraft:slowness 2 0 true
