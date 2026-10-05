scoreboard players set #tick sift.timer 0
function sift:tide/update
scoreboard players remove @a[scores={sift.cd=1..}] sift.cd 1
scoreboard players remove @a[scores={sift.veil=1..}] sift.veil 1
scoreboard players add @a sift.cd 0
scoreboard players add @a sift.souls 0
execute as @a at @s if dimension sift:the_sift run function sift:player/second
execute as @a at @s if dimension sift:the_sift run function sift:ichor/second
execute as @e[type=item_display,tag=sift.wisp] run function sift:souls/wisp_tick
execute as @e[type=marker,tag=sift.portal,tag=!sift.portal.exit] run function sift:portal/expire_tick
execute if entity @e[type=!item_display,tag=sift.mob,limit=1] run function sift:mob/second
scoreboard players enable @a sift_exit
