effect give @s minecraft:slow_falling 12 0 true
effect give @s minecraft:resistance 12 4 true
spreadplayers ~ ~ 0 3 false @s
function sift:portal/build_exit
scoreboard players add @s sift.visits 1
title @s times 20 80 40
title @s subtitle {"text":"Là où chantent les âmes…","color":"light_purple","italic":true}
title @s title {"text":"LE SIFT","color":"aqua","bold":true}
playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 2 0.5
playsound minecraft:block.note_block.chime player @s ~ ~ ~ 1 1.5
advancement grant @s only sift:sift/enter_the_sift
execute if score #tide sift.tmp matches 0 run function sift:tide/announce_0
execute if score #tide sift.tmp matches 1 run function sift:tide/announce_1
execute if score #tide sift.tmp matches 2 run function sift:tide/announce_2
