execute as @e[type=marker,tag=sift.portal.entry] at @s as @a[distance=..2.3,scores={sift.cd=0}] at @s unless dimension sift:the_sift run function sift:portal/enter
execute as @e[type=marker,tag=sift.portal.exit] at @s as @a[distance=..2.3,scores={sift.cd=0}] at @s if dimension sift:the_sift run function sift:portal/leave
