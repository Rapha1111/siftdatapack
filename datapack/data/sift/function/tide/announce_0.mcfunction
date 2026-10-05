title @s times 10 70 30
title @s subtitle {"text":"Les âmes retiennent leur souffle : le sol est léger.","color":"gray","italic":true}
title @s title {"text":"Marée Calme","color":"aqua","bold":true}
execute at @s run playsound minecraft:block.amethyst_block.resonate ambient @s ~ ~ ~ 1.5 0.6
advancement grant @s only sift:sift/three_tides calm
