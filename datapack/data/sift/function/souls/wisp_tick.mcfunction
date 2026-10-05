scoreboard players add @s sift.age 1
execute if score @s sift.age matches 150.. run function sift:souls/wisp_fade
execute if entity @s[tag=sift.up] run function sift:souls/wisp_down
execute unless entity @s[tag=sift.up] run function sift:souls/wisp_up
