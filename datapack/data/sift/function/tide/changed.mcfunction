scoreboard players operation #tide_last sift.tmp = #tide sift.tmp
execute if score #tide sift.tmp matches 0 as @a if dimension sift:the_sift run function sift:tide/announce_0
execute if score #tide sift.tmp matches 1 as @a if dimension sift:the_sift run function sift:tide/announce_1
execute if score #tide sift.tmp matches 2 as @a if dimension sift:the_sift run function sift:tide/announce_2
