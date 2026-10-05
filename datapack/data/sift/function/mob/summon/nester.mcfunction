scoreboard players add #next sift.id 1
summon minecraft:husk ~ ~ ~ {Tags:["sift.mob","sift.native","sift.nester","sift.fresh"],Health:30f,attributes:[{id:"minecraft:max_health",base:30},{id:"minecraft:scale",base:1.0},{id:"minecraft:movement_speed",base:0.3},{id:"minecraft:attack_damage",base:4}],CustomName:{text:"Nicheur",color:"light_purple"},active_effects:[{id:"minecraft:invisibility",amplifier:0,duration:-1,show_particles:0b,show_icon:0b}],DeathLootTable:"sift:entities/nester"}
summon minecraft:item_display ~ ~ ~ {Tags:["sift.model","sift.model.nester","sift.fresh"],item_display:"none",teleport_duration:2,view_range:3.0f,brightness:{sky:13,block:9},item:{id:"minecraft:stick",count:1,components:{"minecraft:item_model":"sift:mob/nester"}},transformation:{translation:[0f,0.600f,0f],left_rotation:[0f,1f,0f,0f],right_rotation:[0f,0f,0f,1f],scale:[1.2f,1.2f,1.2f]}}
scoreboard players operation @e[tag=sift.fresh,distance=..2] sift.id = #next sift.id
scoreboard players set @e[tag=sift.fresh,distance=..2] sift.age 0
execute as @e[tag=sift.fresh,distance=..2] run function sift:mob/finish_fresh
