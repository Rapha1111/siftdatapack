scoreboard players add @s sift.cool 1
execute if score @s sift.cool matches 5.. if entity @a[gamemode=!creative,gamemode=!spectator,distance=3..11] run function sift:mob/abilities/slasher_dash
