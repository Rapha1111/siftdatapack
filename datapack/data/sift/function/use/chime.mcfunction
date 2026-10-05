advancement revoke @s only sift:use/chime
execute unless dimension sift:the_sift run title @s actionbar {"text":"Le carillon ne résonne que dans le Sift.","color":"gray"}
execute if dimension sift:the_sift if score @s sift.souls matches ..19 run title @s actionbar {"text":"Pas assez d’âmes (20 requises).","color":"red"}
execute if dimension sift:the_sift if score @s sift.souls matches 20.. run function sift:use/chime_cast
