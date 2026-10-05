summon marker ~ ~1.6 ~ {Tags:["sift.portal","sift.portal.entry"]}
scoreboard players set @e[type=marker,tag=sift.portal,distance=..3] sift.age 0
playsound minecraft:block.note_block.bell block @a ~ ~ ~ 2 0.5
schedule function sift:portal/melody_2 6t
particle minecraft:end_rod ~ ~1 ~ 0.5 1.2 0.5 0.1 60
advancement grant @a[distance=..8] only sift:sift/sing_to_the_sift
