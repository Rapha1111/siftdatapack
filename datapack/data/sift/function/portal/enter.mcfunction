scoreboard players set @s sift.cd 6
execute store result score @s sift.ox run data get entity @s Pos[0]
execute store result score @s sift.oy run data get entity @s Pos[1]
execute store result score @s sift.oz run data get entity @s Pos[2]
scoreboard players set @s sift.odim 0
execute if dimension minecraft:the_nether run scoreboard players set @s sift.odim 1
execute if dimension minecraft:the_end run scoreboard players set @s sift.odim 2
playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.6
particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.4 60
execute in sift:the_sift run tp @s ~ 220 ~
execute in sift:the_sift as @s at @s run function sift:portal/arrive
