scoreboard players add #tick sift.timer 1
scoreboard players add #p sift.timer 1
execute as @a at @s if dimension sift:the_sift run function sift:player/tick
execute if entity @e[type=item_display,tag=sift.wisp,limit=1] if score #p sift.timer matches 5.. run function sift:souls/wisp_fx
execute if entity @e[type=marker,tag=sift.portal,limit=1] if score #p sift.timer matches 5.. run function sift:portal/portal_fx
execute if entity @e[type=marker,tag=sift.portal,limit=1] run function sift:portal/portal_tick
execute if score #p sift.timer matches 5.. run scoreboard players set #p sift.timer 0
execute if entity @e[type=!item_display,tag=sift.mob,limit=1] run function sift:mob/tick
execute as @a[scores={sift_exit=1..}] run function sift:portal/trigger_exit
execute if score #tick sift.timer matches 20.. run function sift:second
