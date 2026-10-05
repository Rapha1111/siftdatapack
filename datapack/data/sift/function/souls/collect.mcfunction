kill @e[type=item_display,tag=sift.wisp,distance=..1.8,limit=1,sort=nearest]
scoreboard players add @s sift.souls 5
execute if score #tide sift.tmp matches 2 run scoreboard players add @s sift.souls 5
particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.05 12
playsound minecraft:block.amethyst_cluster.hit player @s ~ ~ ~ 1 1.8
playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.6 1.6
execute if score @s sift.souls matches 100.. run function sift:souls/overflow
advancement grant @s only sift:sift/soul_collector
