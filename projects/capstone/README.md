# Machine Learning Engineer Nanodegree
## Capstone Project: Robot Motion Planning

<!--
**Note**

The Capstone is a two-staged project. The first is the proposal component, where you can receive valuable feedback about your project idea, design, and proposed solution. This must be completed prior to your implementation and submitting for the capstone project. 

You can find the [capstone proposal rubric here](https://review.udacity.com/#!/rubrics/410/view), and the [capstone project rubric here](https://review.udacity.com/#!/rubrics/108/view). Please ensure that you are following directions correctly when submitting these two stages which encapsulate your capstone.

You will find an `open_projects` folder in these files. This will be where pre-curated capstone projects are available, should you choose to work on a project already partially designed for you. 

Please email [machine-support@udacity.com](mailto:machine-support@udacity.com) if you have any questions.
-->


### Software required

1. Python 2.7.12 Installation. Anaconda Python 4.3.23 was used as part of this project.
1. Use a recent version of Linux or MacOS machine using a recent version of tcsh. macOS Sierra 10.12.6 and tcsh version `6.18.01 (Astron) 2012-02-14 (x86_64-apple-darwin)` were used for this project.
1. MacBook Pro with 16GB of LPDDR3 DRAM, 2.9GHz i7-6920HQ, and AMD Radeon 460 with 4GB of GDDR5 RAM was used to develop and run this project. You need about 5GB of storage to run the training and testing scripts.

### Steps to Produce Results Described in the Project Report

1. `cd open_projects/robot_motion_planning`
1. `mkdir logs logs2`
1. To train the robot on mazes 01, 02, 03, and 04, and run the benmark random behavior robot in maze 04 run this command: `tcsh train_then_test.csh`
1. To run the benmark robot on mazes 01, 02, 03 run this command: `tcsh train_then_test2.csh`
1. To visualize a solution run this command: `python showmaze_robot_movements.py --testname <Name of Test Maze Text File> --coordinates <Listing of Coordinates For a Solution>`

example:

`python showmaze_robot_movements.py --testmaze test_maze_04.txt --coordinates logs/test_04_8_coordinates.txt`

There are various ways to parse out the coordinates. Here's an example:

`grep "position" logs/test_random_04_3304.log | awk '{print $5 $6}' | sed "s/\]\,/]/g" | & tee logs/test_random_04_3304_coordinates.txt`

### Documents

The name of the proposal is `proposal.pdf`
The name of the project report is `report.pdf`

Here is a link to the proposal [review] 


[review]: https://review.udacity.com/?utm_medium=email&utm_campaign=reviewsapp-submission-reviewed&utm_source=blueshift&utm_content=reviewsapp-submission-reviewed&bsft_clkid=b4c73447-ebe3-409f-a156-d3b4c91f6405&bsft_uid=0072092b-be5a-4c0a-a91a-06edfca359ff&bsft_mid=4ef10896-f393-4b4a-b79d-b13aa0419d48&bsft_eid=6f154690-7543-4582-9be7-e397af208dbd&bsft_txnid=7c8904bf-de20-40ad-9eb1-e79284f1f3b5#!/reviews/704766

