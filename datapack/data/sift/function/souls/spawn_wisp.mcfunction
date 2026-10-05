summon item_display ~ ~ ~ {Tags:["sift.wisp","sift.new"],billboard:"center",view_range:2.0f,brightness:{sky:15,block:15},item:{id:"minecraft:stick",count:1,components:{"minecraft:item_model":"sift:wisp"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f],translation:[0f,0f,0f]}}
spreadplayers ~ ~ 3 20 false @e[type=item_display,tag=sift.new,distance=..2]
execute as @e[type=item_display,tag=sift.new] at @s positioned over motion_blocking run tp @s ~ ~1.4 ~
scoreboard players set @e[type=item_display,tag=sift.new] sift.age 0
tag @e[type=item_display,tag=sift.new] remove sift.new
