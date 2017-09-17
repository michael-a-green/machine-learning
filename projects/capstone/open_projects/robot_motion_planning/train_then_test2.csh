#!/bin/tcsh




#python trainer.py test_maze_01.txt | & tee logs2/train_01.log

# sleep 1

# set i = 1

# while ($i < 5000)

# #    python tester.py test_maze_01.txt | & tee logs2/test_01_${i}.log
#     python tester_random.py test_maze_01.txt | & tee ~/Downloads/logs2/test_random_01_${i}.log &

#     set mod_i=`expr $i  % 8`
#     echo "mod_i = $mod_i"

#     if ($mod_i == 0) then
#         echo ""
#         echo "waiting with i = $i"
#         echo ""
#         wait ;
#     endif


#     @ i++

# end

# wait;


# #python trainer.py test_maze_02.txt | & tee logs2/train_02.log

sleep 1

set i = 1

while ($i < 10000)

#    python tester.py test_maze_02.txt | & tee logs2/test_02_${i}.log
    python tester_random.py test_maze_02.txt | & tee ~/Downloads/logs2/test_random_02_${i}.log &

    set mod_i=`expr $i  % 8`
    echo "mod_i = $mod_i"

    if ($mod_i == 0) then
        echo ""
        echo "waiting with i = $i"
        echo ""
        wait ;
    endif

    @ i++

end

wait;

#python trainer.py test_maze_03.txt | & tee logs2/train_03.log

sleep 1

# set i = 1

# while ($i < 5000)

# #    python tester.py test_maze_03.txt | & tee logs2/test_03_${i}.log
#     python tester_random.py test_maze_03.txt | & tee ~/Downloads/logs2/test_random_03_${i}.log &

#     set mod_i=`expr $i  % 8`
#     echo "mod_i = $mod_i"

#     if ($mod_i == 0) then
#         echo ""
#         echo "waiting with i = $i"
#         echo ""
#         wait ;
#     endif

#     @ i++

# end


# wait;
