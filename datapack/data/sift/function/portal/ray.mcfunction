scoreboard players remove #ray sift.tmp 1
execute if block ~ ~ ~ minecraft:note_block align xyz positioned ~0.5 ~0.5 ~0.5 run function sift:portal/try
execute unless block ~ ~ ~ minecraft:note_block if score #ray sift.tmp matches 1.. positioned ^ ^ ^0.1 run function sift:portal/ray
