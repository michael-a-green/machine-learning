#!/bin/tcsh




python trainer.py test_maze_01.txt | & tee logs/train_01.log

sleep 1

set i = 1

while ($i < 100)

    python tester.py test_maze_01.txt | & tee logs/test_01_${i}.log

    @ i++

end



python trainer.py test_maze_02.txt | & tee logs/train_02.log

sleep 1

set i = 1

while ($i < 100)

    python tester.py test_maze_02.txt | & tee logs/test_02_${i}.log

    @ i++

end


python trainer.py test_maze_03.txt | & tee logs/train_03.log

sleep 1

set i = 1

while ($i < 100)

    python tester.py test_maze_03.txt | & tee logs/test_03_${i}.log

    @ i++

end