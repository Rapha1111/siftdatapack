advancement revoke @s only sift:use/fork
scoreboard players set #ray sift.tmp 70
execute anchored eyes positioned ^ ^ ^ run function sift:portal/ray
execute if score #ray sift.tmp matches 0.. run title @s actionbar {"text":"Le diapason ne trouve aucune Machine à notes…","color":"gray"}
