scoreboard players operation #cur sift.id = @s sift.id
execute as @e[type=minecraft:item_display,tag=sift.model,distance=..5] if score @s sift.id = #cur sift.id run tp @s ~ ~ ~ ~ ~
