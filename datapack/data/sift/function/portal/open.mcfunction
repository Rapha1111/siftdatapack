execute if dimension sift:the_sift run tellraw @a[distance=..8] [{"text":"[Sift] ","color":"light_purple"},{"text":"Vous êtes déjà dans le Sift. Utilisez la passerelle de retour.","color":"gray"}]
execute unless dimension sift:the_sift unless entity @e[type=marker,tag=sift.portal,distance=..3] run function sift:portal/open_confirm
