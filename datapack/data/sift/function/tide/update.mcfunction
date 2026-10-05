execute store result score #clock sift.tmp run time of sift:tides query time
scoreboard players operation #clock sift.tmp %= #24000 sift.const
scoreboard players operation #tide sift.tmp = #clock sift.tmp
scoreboard players operation #tide sift.tmp /= #8000 sift.const
execute unless score #tide sift.tmp = #tide_last sift.tmp run function sift:tide/changed
