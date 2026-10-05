scoreboard players add #next sift.id 1
summon minecraft:rabbit ~ ~ ~ {Tags:["sift.mob","sift.native","sift.blub","sift.fresh"],Health:8f,attributes:[{id:"minecraft:max_health",base:8},{id:"minecraft:scale",base:1.0},{id:"minecraft:movement_speed",base:0.3}],CustomName:{text:"Blub",color:"light_purple"},active_effects:[{id:"minecraft:invisibility",amplifier:0,duration:-1,show_particles:0b,show_icon:0b}],DeathLootTable:"sift:entities/blub",Silent:1b}
summon minecraft:item_display ~ ~ ~ {Tags:["sift.model","sift.model.blub","sift.fresh"],item_display:"none",teleport_duration:2,view_range:3.0f,brightness:{sky:13,block:9},item:{id:"minecraft:stick",count:1,components:{"minecraft:item_model":"sift:mob/blub"}},transformation:{translation:[0f,0.675f,0f],left_rotation:[0f,1f,0f,0f],right_rotation:[0f,0f,0f,1f],scale:[1.35f,1.35f,1.35f]}}
scoreboard players operation @e[tag=sift.fresh,distance=..2] sift.id = #next sift.id
scoreboard players set @e[tag=sift.fresh,distance=..2] sift.age 0
execute as @e[tag=sift.fresh,distance=..2] run function sift:mob/finish_fresh
