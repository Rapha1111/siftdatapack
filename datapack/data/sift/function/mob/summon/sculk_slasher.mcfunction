scoreboard players add #next sift.id 1
summon minecraft:endermite ~ ~ ~ {Tags:["sift.mob","sift.native","sift.sculk_slasher","sift.fresh"],Health:34f,attributes:[{id:"minecraft:max_health",base:34},{id:"minecraft:scale",base:3.2},{id:"minecraft:movement_speed",base:0.38},{id:"minecraft:attack_damage",base:5}],CustomName:{text:"Lacérateur de sculk",color:"light_purple"},active_effects:[{id:"minecraft:invisibility",amplifier:0,duration:-1,show_particles:0b,show_icon:0b}],DeathLootTable:"sift:entities/sculk_slasher"}
summon minecraft:item_display ~ ~ ~ {Tags:["sift.model","sift.model.sculk_slasher","sift.fresh"],item_display:"none",teleport_duration:2,view_range:3.0f,brightness:{sky:13,block:9},item:{id:"minecraft:stick",count:1,components:{"minecraft:item_model":"sift:mob/sculk_slasher"}},transformation:{translation:[0f,0.625f,0f],left_rotation:[0f,1f,0f,0f],right_rotation:[0f,0f,0f,1f],scale:[1.25f,1.25f,1.25f]}}
scoreboard players operation @e[tag=sift.fresh,distance=..2] sift.id = #next sift.id
scoreboard players set @e[tag=sift.fresh,distance=..2] sift.age 0
execute as @e[tag=sift.fresh,distance=..2] run function sift:mob/finish_fresh
