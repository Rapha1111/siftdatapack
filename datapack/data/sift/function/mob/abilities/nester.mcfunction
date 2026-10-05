scoreboard players add @s sift.cool 1
execute if score @s sift.cool matches 6.. if entity @a[gamemode=!creative,gamemode=!spectator,distance=2..10] run function sift:mob/abilities/nester_lunge
