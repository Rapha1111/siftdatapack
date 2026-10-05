scoreboard players remove @s sift.souls 20
execute positioned ^ ^ ^2.2 run function sift:mob/summon_ally
particle minecraft:sculk_charge_pop ~ ~1 ~ 0.6 0.6 0.6 0.1 30
playsound minecraft:block.sculk_catalyst.bloom player @a ~ ~ ~ 1.5 0.8
playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1.5 0.7
effect give @s minecraft:regeneration 5 1 true
advancement grant @s only sift:sift/echo_ally
