execute as @e[type=!minecraft:item_display,tag=sift.mob] at @s run function sift:mob/sync
execute as @e[type=minecraft:item_display,tag=sift.model] at @s unless entity @e[type=!minecraft:item_display,tag=sift.mob,distance=..6] run function sift:mob/orphan
scoreboard players add @e[type=minecraft:item_display,tag=sift.afterimage] sift.age 1
kill @e[type=minecraft:item_display,tag=sift.afterimage,scores={sift.age=7..}]
