execute store result score @s sift.tmp if entity @e[tag=sift.native,tag=sift.mob,type=!minecraft:item_display,tag=!sift.ally,distance=..48]
execute if score @s sift.tmp matches ..14 if predicate sift:chance/spawn_try run function sift:mob/spawn_roll
