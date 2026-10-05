title @s times 10 70 30
title @s subtitle {"text":"Les âmes affluent par vagues : cueillez-les vite !","color":"gray","italic":true}
title @s title {"text":"Marée Haute","color":"light_purple","bold":true}
execute at @s run playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 1.5 1.2
advancement grant @s only sift:sift/three_tides surge
