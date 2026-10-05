function sift:give/fork
function sift:give/chime
function sift:give/vial
give @s minecraft:sculk_catalyst 1
give @s minecraft:sculk_sensor 4
give @s minecraft:note_block 1
tellraw @s [{"text": "[Sift] ", "color": "light_purple"}, {"text": "Kit de départ : bâtissez la Machine à notes (catalyseur de sculk sous un bloc musical, 4 détecteurs de sculk autour) puis utilisez le Diapason.", "color": "gray"}]
