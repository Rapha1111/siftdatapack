title @s times 10 70 30
title @s subtitle {"text":"L'ichor se retire, les âmes se font rares mais denses.","color":"gray","italic":true}
title @s title {"text":"Marée Basse","color":"gold","bold":true}
execute at @s run playsound minecraft:block.sculk_catalyst.bloom ambient @s ~ ~ ~ 1.5 0.5
advancement grant @s only sift:sift/three_tides ebb
