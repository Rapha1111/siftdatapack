scoreboard players set @s sift_exit 0
execute unless dimension sift:the_sift run tellraw @s [{"text":"[Sift] ","color":"light_purple"},{"text":"Vous n’êtes pas dans le Sift.","color":"gray"}]
execute if dimension sift:the_sift run function sift:portal/return_home
