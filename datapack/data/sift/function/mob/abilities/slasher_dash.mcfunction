scoreboard players set @s sift.cool 0
effect give @s minecraft:speed 1 6 true
playsound minecraft:entity.warden.sniff hostile @a ~ ~ ~ 1.5 1.8
particle minecraft:sculk_charge_pop ~ ~0.5 ~ 0.4 0.3 0.4 0.05 10
function sift:mob/afterimage
schedule function sift:mob/afterimage_2 3t
schedule function sift:mob/afterimage_3 6t
