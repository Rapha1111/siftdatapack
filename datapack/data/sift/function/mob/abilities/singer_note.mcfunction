execute store result score #r sift.tmp run random value 0..4
execute if score #r sift.tmp matches 0 run playsound minecraft:block.note_block.chime neutral @a ~ ~1 ~ 2 0.7
execute if score #r sift.tmp matches 1 run playsound minecraft:block.note_block.chime neutral @a ~ ~1 ~ 2 0.84
execute if score #r sift.tmp matches 2 run playsound minecraft:block.note_block.chime neutral @a ~ ~1 ~ 2 1.05
execute if score #r sift.tmp matches 3 run playsound minecraft:block.note_block.bell neutral @a ~ ~1 ~ 2 0.7
execute if score #r sift.tmp matches 4 run playsound minecraft:block.note_block.bell neutral @a ~ ~1 ~ 2 1.26
particle minecraft:note ~ ~3.2 ~ 0.6 0.4 0.6 1 3
particle minecraft:sculk_soul ~ ~2.4 ~ 0.4 0.8 0.4 0.02 4
