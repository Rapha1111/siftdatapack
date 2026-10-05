scoreboard players set @s sift.souls 0
experience add @s 40 points
effect give @s minecraft:absorption 30 1 true
effect give @s minecraft:regeneration 8 1 true
particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.3 40
playsound minecraft:block.beacon.activate player @a ~ ~ ~ 1 1.6
title @s actionbar {"text":"✦ Débordement d’âmes ! ✦","color":"light_purple","bold":true}
advancement grant @s only sift:sift/soul_overflow
