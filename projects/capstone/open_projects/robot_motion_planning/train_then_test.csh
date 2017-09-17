#!/bin/tcsh
# 
# 
# 
# 
# python trainer.py test_maze_01.txt | & tee logs/train_01.log
# 
# sleep 1
# 
# set i = 1
# 
# while ($i < 100)
# 
#     python tester.py test_maze_01.txt | & tee logs/test_01_${i}.log &f
#     #python tester_random.py test_maze_01.txt | & tee logs/test_random_01_${i}.log
#     set mod_i=`expr $i % 10`
#     
#     if ($mod_i == 0) then
#         echo ""
#         echo "waiting with i = $i"
#         echo ""
#         wait;
#     endif
# 
#     @ i++
# 
# end
# 
# 
# python trainer.py test_maze_02.txt | & tee logs/train_02.log
# 
# sleep 1
# 
# set i = 1
# 
# while ($i < 100)
# 
#     python tester.py test_maze_02.txt | & tee logs/test_02_${i}.log &
#     #python tester_random.py test_maze_02.txt | & tee logs/test_random_02_${i}.log
#     set mod_i=`expr $i % 10`
#     
#     if ($mod_i == 0) then
#         echo ""
#         echo "waiting with i = $i"
#         echo ""
#         wait;
#     endif
# 
# 
#     @ i++
# 
# end
# 
# 
# 
# python trainer.py test_maze_03.txt | & tee logs/train_03.log
# 
# sleep 1
# 
# set i = 1
# 
# while ($i < 100)
# 
#     python tester.py test_maze_03.txt | & tee logs/test_03_${i}.log &
#     #python tester_random.py test_maze_03.txt | & tee logs/test_random_03_${i}.log
#     set mod_i=`expr $i % 10`
#     
#     if ($mod_i == 0) then
#         echo ""
#         echo "waiting with i = $i"
#         echo ""
#         wait;
#     endif
# 
#     @ i++
# 
# end
# 


python trainer.py test_maze_04.txt | & tee logs/train_04.log

sleep 1
set i = 1


while ($i < 100)

    python tester.py test_maze_04.txt | & tee logs/test_04_${i}.log &
    set mod_i=`expr $i % 10`
    
    if ($mod_i == 0) then
        echo ""
        echo "waiting with i = $i"
        echo ""
        wait;
    endif
    @ i++

end


sleep 1
set i = 1

while ($i < 5000)

    python tester_random.py test_maze_04.txt | & tee logs/test_random_04_${i}.log &
    set mod_i=`expr $i % 10`
    
    if ($mod_i == 0) then
        echo ""
        echo "waiting with i = $i"
        echo ""
        wait;
    endif
    @ i++

end

