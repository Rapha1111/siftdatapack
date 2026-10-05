summon minecraft:marker ~ ~ ~ {Tags:["sift.probe"]}
spreadplayers ~ ~ 14 38 false @e[type=minecraft:marker,tag=sift.probe,distance=..2]
execute as @e[type=minecraft:marker,tag=sift.probe] at @s run function sift:mob/spawn_at
kill @e[type=minecraft:marker,tag=sift.probe]
