scoreboard objectives add sift.tmp dummy
scoreboard objectives add sift.const dummy
scoreboard objectives add sift.timer dummy
scoreboard objectives add sift.souls dummy
scoreboard objectives add sift.cd dummy
scoreboard objectives add sift.ox dummy
scoreboard objectives add sift.oy dummy
scoreboard objectives add sift.oz dummy
scoreboard objectives add sift.odim dummy
scoreboard objectives add sift.veil dummy
scoreboard objectives add sift.age dummy
scoreboard objectives add sift.id dummy
scoreboard objectives add sift.cool dummy
scoreboard objectives add sift.visits dummy
scoreboard objectives add sift_exit trigger
scoreboard players set #24000 sift.const 24000
scoreboard players set #8000 sift.const 8000
scoreboard players set #0 sift.const 0
scoreboard players set #100 sift.const 100
scoreboard players set #2 sift.const 2
scoreboard players set #5 sift.const 5
scoreboard players set #10 sift.const 10
scoreboard players set #20 sift.const 20
scoreboard players set #tide_last sift.tmp -1
time of sift:tides resume
tellraw @a [{"text":"[Sift] ","color":"light_purple","bold":true},{"text":"Data pack chargé — le chant des âmes résonne.","color":"aqua","bold":false}]
