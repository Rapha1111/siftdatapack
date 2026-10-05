fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 minecraft:deepslate_tiles
fill ~-2 ~ ~-2 ~2 ~5 ~2 minecraft:air
setblock ~ ~-1 ~ minecraft:sculk_catalyst
setblock ~ ~ ~ minecraft:note_block
setblock ~1 ~ ~ minecraft:sculk_sensor
setblock ~-1 ~ ~ minecraft:sculk_sensor
setblock ~ ~ ~1 minecraft:sculk_sensor
setblock ~ ~ ~-1 minecraft:sculk_sensor
setblock ~2 ~-1 ~2 minecraft:chiseled_deepslate
setblock ~-2 ~-1 ~2 minecraft:chiseled_deepslate
setblock ~2 ~-1 ~-2 minecraft:chiseled_deepslate
setblock ~-2 ~-1 ~-2 minecraft:chiseled_deepslate
setblock ~2 ~ ~2 minecraft:soul_lantern
setblock ~-2 ~ ~2 minecraft:soul_lantern
setblock ~2 ~ ~-2 minecraft:soul_lantern
setblock ~-2 ~ ~-2 minecraft:soul_lantern
kill @e[type=marker,tag=sift.portal.exit,distance=..6]
summon marker ~ ~1.6 ~ {Tags:["sift.portal","sift.portal.exit"]}
tp @s ~1 ~ ~1
