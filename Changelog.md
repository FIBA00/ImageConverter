# MPS WORKER CODING LOG

- Working on the coding and finalizing. Test_worker_1_oop_template_1.py
- The workers flag resetting and assigning are used in the scraper to control the scraping data, that's why they have to be designed carefully.

## DAY 1

### C0: The brain code Tasks Done or about to be done are listed

- Task for adding status listener and responding system is added
  - message HANDLERS { - status - Error - Permission
    } are done coded
- Adding Realtime data handler:
  after the \_listen_to_worker() recieves the data it sends to \_process_data(),
  - here we separate into:
    > DATA_HANDLERS{- Realtime, - Comparison, - prediction} and send them to their respective handlers.
- Removed the data handlers from the {\_process_message() function and sent to \_process_data()} functions.
- Fixed bug in stopping the redis server from brain changed to using the function stop_all_existing_redis_servers()
- Converting the worker code into template to give the code the real workers of prediction, comparison, and scraper.
- created redis connection section, worker system management section,
- created send_assessment() function
- creating sending data section and data management section
- unfinished \_send_status_update() , \_send_info_to_brain(), \_send_data_to_brain() functions.
- finished {\_send_status_update(), \_send_error_to_brain(), \_send_info_to_brain(), }
  functions.

## DAY 2

### C0: The brain code progress Tasks and Reports

- Creating \_send_info_to_gui() not finished..
- Created \_send_data_to_brain()
- Created \_send_info_to_gui()
- Adding new feature \_send_info_to_worker()
- Added boolean control to the functions
- Added data classes and using the WorkerState class across the codes.
- Added \_is_working() to check wether the worker is working or idle
- Added \_resume_worker() to change the state of the worker based on the usage
- added logic example for external codes that control the worker and shared state between the functional and oop codes.
- TASK: Change the constants into the data class constants [DONE]
- Added \_load_log() and \_load_data()
- Adding the listeners and threading section
- Adding advanced listener function inspired by the brain[splitting info and data listeners]
- Creating new functions inside the worker

  > \_decode_message()[DONE],
  > \_process_info()[DONE],
  > \_process_data()[HOLDING],
  > \_listen_to_worker_message()[DONE],
  > \_handle_status_message()[DONE],
  > \_handle_command_message()[DONE],
  > \_handle_task_message()[DONE],

- changed the \_is_working() function to \_change_status()[DONE] that takes and argument of state:str that we can call in another function to change the workers stats.
- The process info logic will be updated from the initial idea to be more advanced.[DONE]
- Adding logic to except the change status command from the brain.[DONE]
- Adding logic to the \_handle_command_message()[DONE] to except different commands at the same time to change the status of the worker.
- [DONE] create the send_task_function to send specific task the worker. [DONE]
- [DONE] Update the brain to handle all the new upgraded command types and info types also task types.[DONE]
- Adding logic to the \_handle_task_message()[DONE],
- [TODO] Added new function called \_assess_worker()[IN-PROGRESS] to do bunch of checks on the worker.
- Added new function called \_send_task_update()[DONE] to handle the task progress updating the brain.
- Added new function called \_send_permission_request()[DONE] to handle the request to update internal systems from the brain.
- Used sub content splitting on the task message handling to handle the minute of the interval task
- Added threading section with \_start_threads() starting two different threads one for data sending and one for listening to brain.
- Added run() function to call all the functions
- Finished working on the entire code migrating into the OOP based system template.

## DAY 3

### C1: More of adding and removing and collecting codes

- Migrating the SCRAPER CODE into the worker 1:- if we cant do that we gonna have a pile of scripts we cant manage.
- Added logger utility function and replaced the entire print into logger.
- Adding the real time data scraper to worker for real management work, using the refernce codes that written by windsurf.
- Removing data processing for incoming data from brain instead we process the data saved by the worker and we send it to brain.
- Adding new function \_initialize_components()[DONE] to start the scraper system.
- remove the \_start_thread() since we cant control each thread instead we can change it to utility function.
- WE HAVE COLLISION OF CLASS METHODS EX: logger
- Fixed the collision by making the logger data class component, which means every class has access to the self.state.logger().
- Migrating the prints into logger[DONE], the special prints like errors need certain level loggers.
- Adding doc strings to the methods. migrating from MDSS [DONE]
- Bug fixing here and there and adding try and except blocks to stop the headaches when debugging.
- Removed the \_initialize_components() becuase its better to start them all at the main worker entry in separate threads.

## DAY 4

### C1: Connecting and the worker and scraper and imporvements

- Migrating the string constants for commands, status, and state to enums
- Added data classes:-
  > WorkerStatus(Enum)[DONE],
  > BWCmd(Enum)[DONE],
  > BWSysCheck(Enum)[DONE],
  > WorkerAssessment(Enum)[DONE].

## DAY 5

### C1: Changing code logic to simpler and short forms

- Added new function \_perform_system_check()[DONE] to do the system check and assign the string values to the self.system_check status setting.
- Moved the method \_perform_system_check() to the WorkerState data class to be a helper function managing the worker.
- Changed assessment_indicator: str = "" to task_indicator
- Added methods > update_tasker()[DONE], > adjust_sending_interval()[DONE], > \_update_state()[DONE], \_change_worker_status()[]
- Changed the WorkerStatus() to WorkerStatusUpdater() data classes and migrateing the state, changed the WorkerState() to WorkerStateData()[This class represents the worker's state, encapsulating attributes such as status, system_checl, sending_interval, and others.it manages the workers health, task_progress, and data sending frequency.].
- Changed the shared_state class call to the shared_state_data
- Renamed the WorkerStateUpdater() data Enum class to WorkerStatus()
- Added new method \_execute_command()[DONE] helper method to execute the necessary commands from the brain to worker.
- Adding new data class BWErCode(Enum)[DONE] that contains errors related to the running system and resource usage.
- Updating the \_handle_command_message(self) with the new helper method \_execute_command() [DONE].
- [DONE] MIGRATE THE STRING BASED KEY VALUE PAIRS TO ENUM
- Added REAL TIME Flag to the data sent to the brain for easy processing.
- [TODO] Add scraper started flag to indicate whether worker is idle or not, because the worker wont start the scraper if the flag is down.
- [TODO] Fix the \_send_error_to_brain() method to send different types of errors to the brain to handle.
- Added new flag PAUSED the flag between process stopping and holding, which helps us to transition between idle and stop.
- Removed the \_execute_command() method since we are directly calling the change_worker_status() and passing the commands
- Removed permission request function because we dont need to ask the brain to send data anymore since its controlled by the brain.
- Renamed \_change_worker_status() to \_change_status() since we are using it already in the handle command method, its better for all.
  > [TODO: LIST OF TODOS FOR THE REAL TIME DATA SCRAPER WORKER ]:
      - [TASK 1] Change the algorithm of sending fake data to the scraper.
      - [TASK 2] Add the flags that control the worker to the scraper logic.
      - [TASK 3] Add the stderr and stdout output routing to the GUI.
      - [TASK 4] Add feature to send any important information regarding the worker to the GUI without brain intervention.
      - [TASK 5] Control the scraper data sending if the duplicate number detected dont send it.[POTENTIAL BUG] control.
      - [TASK 6] Change the string based commands to enums all over the workers.

### C0: BRAIN CODE UPDATING BASED ON THE NEW WORKER COMMANDS AND SETUP.

- Removed log_file \*\*Args from the starting script with sub process since we already using the logger utility script.
- After the \_listen_to_worker() started the workers must received status check from the brain initially instead of the workers starting the process from down to up. [so i have to send the initial command on checking their status]. so send_command_to_worker("CHECK", worker_id) must be the starting code.
- Migrating the worker advanced codes to the brain for improvements.[DONE] But more in the future.
- Add the log utility script and add the data class BrainData()[DONE] to the brain.
- Removed redundant codes inside the \_send_command_to_worker() and replaced with simpler form that uses the \_send_info_to_worker() method and supply the task or command we need.
- Removed redundant methods: \_message_listener(), \_data_listener() while we have already a worker listener why are we listening again to the same channels twice, ?[DONE]
- Removed permission handler I don't need it anymore.
- Migrated the print to logger. Change the errors and debugs based on necessity [IN-PROGRESS]
- Renamed the real time data scraper to br_real_time_worker_1.py
- [DONE] Migrate the brain string status and commands to enums
- [DONE] Edit the logic for handling errors from workers inside the brain.
- [TODO] Add the system to convert the dictionary data to string inside all workers.
- [DONE] We need better mechanism to control the data flow, or we should just let it flow.
- [TODO] Edit the handle_comparison_data() send the saved data to the daily analysis by loading the file.
-

### C2: Working on the br_prediction_worker_2.py

#### TODO TASKS FOR THIS TO GO SMOOTHLY

> [TODO : Task list]:

    - [TASK 1] Edit and prepare the prediction system before the worker,
    - [TASK 2] Change the already written codes of the prediction AI to our specifics.
    - [TASK 3] Edit the worker 2 accept the prediction AI and control it.
    - [TASK 3.1] Add command excepting system from the Daily analysis ai.
    - [TASK 4] Prepare the worker to control the prediction AI out put to be send to the brain.
    - [TASK 5] Integrate the worker 2 into the brain ecosystem and test.
    - [TASK 6] Ask gpt to explain every aspect of the ai code to explain and create change able settings.
    - [TASK 7] Migrate the advanced codes for the prediction ai and add the missing codes to it.
    - [TASK 7.1] Migrate the prediction confidence calculation in the model_manager code.
    - [TASK 8] Make the prediction to save the data and send instead of directly sending the prediction on spot.
    - [TASK 9] Add task handling sent from the daily analyzer to train the model

### Working on the Test_pai_edit.py[which is the prediction AI]

> [TASK 1] Edit and prepare the prediction system before the worker,

- Added the channels for comms and data redis
- Added the \_prepare_data()[DONE] function to prepare the csv files for the training and prediction.
- Changing back to the oop i think there is a lot of things we don't understand her.
- added boolean and constant, is_training=False, self.feature_names=None
- Added \_prepare_single_prediction()[IN-PROGRESS] function to prepare the trained data output for one prediction.

## DAY 6

> [TASK 2] Change the already written codes of the prediction AI to our specifics.

- Finished \_prepare_single_prediction()[DONE]
- Added \_save_model()[DONE] and model_path in data class.
- Adding debugging print on every line.
- [TODO] Migrate the interpret_results() method to the worker instead of pai.
- Added \_train_model()[DONE] and data_file_path in data class.
- Added \_load_model()[DONE]
- Added \_predict_data()[DONE]
- > [TASK 3] Edit the worker 2 accept the prediction AI and control it.
- [DONE]Copy the template of oop worker 1 and prepare the prediction worker.
- Added try and except to the \_change_status() method.
- [DONE] Adjust the data sending system to the predict data method calling.
- [TODO] Fix bugs inside the PREDICTION DATA components splitting
- [DONE] Add the method to handle prediction data in the brain.
- [TODO] Add code to handle the task given from Daily analysis AI
- Renamed the \_send_data_continuously() to prediction_service()
- Added more error code to the BWErCode(Enum) class
- Adding \_listen_worker_message()[DONE] method for prediction ai to do a task sent from the DAA
- Updated the listeners thread clicking system
- Updated the thread closing system in brain and workers to services.

> [TASK 3.1] Add command excepting system from the Daily analysis ai.

-

### C4: Working on the daily analysis code to facilitate TASK 3.1

- [DONE] Migrating the worker code.
- [TASK] Add system to send task to the AI to train the model based on the output of the analysis
- [TASK]

### C3: Working on the comparison system test_c3_comparison and more

- Edit the comparison system to compare the two datas.
- Added the data class CompareData()[IN-PROGRESS]
- Added the RealTimeCompare()[DONE] class
- Added the \_compare_data()[UNDONE]
- Added the \_validate_data()[DONE]; uses the traditional which is no ML Models.
- Added the \_compare_each_data()[ONHOLD]
- [DONE] Add the compare system calling inside the brain
- [DONE] Migrating the worker oop template to the c3_Comparison_worker_3.py
- [TODO] Edit the process data logic to accept the worker data
- [THINK] Instead of rerouting the 2 datas through brain why not directly send it to the comparison,
- [THINK] NO > that means we have create brain like comparison system which adds another complexity on top of existing one.
- Removing unnecessary methods from the comparing system
- Added \_save_data()[IN-PROGRESS] method to save the results of comparison into differnt file types.
- Added \_process_data()[DONE] To handle the real time and prediction data comes from brain.
- Added \_handle_prediction_data() in BRAIN to handle the data between prediction and comparison
- [THINK] we received the data from brain 2: then we \_process_data().
  > but each starts with their unique identifier , so we can strip the unique identifier and
  > assign the rest to each respective data variables, then
  > we must pass the two datas to the \_compare_data() and give it to it,
- [C3 IS 50% DONE ONLY TASK LEFT IS TODO TASKS THAT ARE REQUIRED TO MAKE IT ADVANCED AND TESTING]
- [TODO] Handle the data sent from the brain inside the comparison which is combined we need to split it.
- [TASK] Create many comparison result columns with their respective data source. Ex. Multiplier difference, range and tolerance.
-

## DAY 7

### C5: GUI Controlling worker

- Migrating the worker codes to the existing code.[DONE]
- [THINK] after listening on channels without explicitly receiving the message from the worker can see the data.
- [THINK] the message is just displayed without the script sending the data which means intercepting.

- [TODO] Change the tasks in the GUI to new tasks different from the rest of workers.
- [TODO] Migrate the string status indicators to enum.
- [TODO] Update the listen to worker messages to handle all the infos from each of the worker.
- [TODO] Design new system to handle all the messages for the workers and brain in the gui.
-

### C0: Finish the brain code with the todo lists

- [DONE] Migrate the brain string status and commands to enums,
- [DONE] For all workers update the code for changing the workers status.
- [DONE] change the WorkerStateUpdater to WorkerStatus and
- [DONE] change all the status from IDLE to desired one.
- [DONE] Change the WorkerAssessment() to WorkerTaskIndicator()
- [TODO] We have to create a task logic to assess accidental stops and regular command based stops! 
- [DONE] Task indicator handler is done for now.
- [DONE] Add Data Rerouting function()
- [TASK] We need better mechanism to control the data flow, or we should just let it flow.
  > Make the prediction data flow to be file based instead of directly sending the prediction on spot.
- Added \_reroute_data() to send data to the comparison data worker.[DONE]
- [TODO] Check the message preparing to send to comparison for method to handle this datas together.
- Added \_send_data_worker() to send the data to any worker.[DONE]
- [TODO] Update the work flow manager in the brain.

### The rest of tasks done listed below

- Added \_send_task_to_pai() inside the DAA.[IN-PROGRESS]
- Created new test file for daily analysis code idea.
-

## DAY 8

- C1: Connecting the scraper to worker to send data to the brain.[DONE]
- C1: created \_prepare_data(data), and passing the data to the \_send_data_continuously(data).[DONE]
- C1: [TODO] Edit the data to be sent to the brain to match the prediction data.
- C1: [TODO] Add command accepting method for the scraper components.
- C1: [TODO] Update the thread to handle race conditions using thread.lock() in worker state.
- C1: Adding the setter and getter for the booleans to prevent lock.
- C1: [DINE] Update the shutdown mechanism.
- C1:

## DAY 9

- C1: Updating the if and else codes to more shortened form.

## DAY 10 JANUARY 15

- [DONE]CREATING THE ABSTRACT BASE SKELETON CLASS
- Adding all methods in the base worker skeleton[DONE]
- replacing all the logics with debug print.
- checking the logic flow [DONE]
- Created test abc_scraper_worker, abc_base_worker and abc_scraper_worker_test files
- Created worker class that inheretes from the base worker
- Successfully imported and used the base skeleton code from the base worker class.
- [DONE] Adding the necessary Enums and Data class methods to the skeleton.
- [DONE] Adding individual channels for each worker inside the base worker.
- [DONE] Editing each individual channels to fit the workers need.
- [DONE] Adding the channels usage with the methods.
- [DONE] Creating actual redis client starter method.
- [TODO] Use tqdm in the retry mechanisms to show the progress.
- [DONE] Adding all the methods to the base skeleton code which uses the id base.
- [DONE] Adding the send_data_to_worker codes.
- [TASK] Creating the task handler which is not quite done yet just lets create the idea.
- [DONE] Task handler method is done for now the basics.

## DAY 11 JAN 18

- [DONE] Editing the string constants into enums.
- [DONE] Adding data class methods
- [DONE] Adding the listen to worker messages method

* RELATED INFOS FROM BRAIN:
  - threading - the gui listener
  - threading - the worker message listener
  - threading - the worker data listener
  - Listening - for messages from gui
  - Listening - for messages from worker
  - Listening - for data from worker
  - processing - the messages from gui
  - processing - the messages from worker
  - processing - the data from worker
  - sending - to messages to gui
  - sending - to messages to worker
  - sending - to data to worker
    this all should be in a class as method, with only changing
  - the parameters and
  - scripts names and
  - channels we can make it real brain
    components we add later:
    add specific self.data.logger.logging service that is going to send toast notification on the gui
  - use modal that self destructs after given second, based on the severity of the info.

- [DONE] Added configs for other workers in the brain
- [TODO] Edit the channel configs in the brain to match the skeleton base.
- [DONE] Added redis service starting and stopping from worker for testing purposes.
- [DONE] Adding a redis manager packaging checking system before starting the process and serviceses.
- [DONE] Adding interface for the scripts when we use subprocess with sudo.
- [DONE] Redis manager needs clean up and refactoring.
- [DONE] Add this "redis-server --port 6380 --daemonize no" to the redis manager.
- [DONE] Editing the br_redis_manager to OOP.
- [DONE] added data class to manage some constants,
- [DONE] Renaming processes that use subprocesses to terminate later on if an error occurred.
- [DONE] Added class for Redis manager separate from system manager adding the methods now. 

## DAY 12 JAN 19
- [DONE] call and test the redis manager inside the worker code
- Moved bkp codes to the bkp folder.
- [DONE] migrate the new worker codes to the base code.
- [DONE] Start importing the other worker codes and connect to the brain.
- [DONE] Migrate the new redis manager code to the brain.
- [DONE] Fixing the brain codes with little tweaks and error handling.
- [DONE] Create the initial command center starting system. [FOr now the brain is just looking at the worker and not doing anything].
- [DONE] Migrate the channels and fix the enter comms.
- [DONE] Creating _start_monitor() that starts sending commands and tasks based on the workers ID , 
- [DONE] Add the code to start the initial status check command sending from brain.
- [DONE] Updating the channels to one unique way.

## DAY 13 JAN 20
- [DONE] deleted the monitor system , let the worker send initial status update.
- [DONE] Fixed status recognition error, while the worker is sending the status update the brain is comparing with enum the string.
- [DONE] Fix the base worker code for enum to string comparison error.
- [DONE] Created gracefull shutdown inside the worker code.
- [TASK] Worker on the Prediction ai to improve and understand it.
- [DONE] Updated the PAI system to use the worker base code and implement process data.
- [DONE] Bug fixed in the naming convection of using unique id based channels in the worker.

## DAY 14 JAN 21
- [DONE] Worker2 is initialized succesfully moving real time data sending system.
- [DONE] If worker sends the RUNNING status send task for each worker. Edit the brain to handle sending task to specific worker.
- [INPROGRESS] create a method tailarod to specific workers, realtime worker, prediction and more, which handles all the things.
- [DONE] handle task by routing the command to the specific worker methods, if REALITIME call the realtime worker.
- [DON] Adding method to send data to brain and worker 
- [DONE] All issues are resolved data sending successfull, state changing successfull.
- [INPROGRESS] Creating the compare system for the real time data and prediction data
- [INPROGRESS] Editing the scraper2 code into the comapare worker adding methods.
- [INPROGRESS] edit the usage of converting enums to string and instead use the direct storing of enums.


## DAY 15 JAN 22
- [INPROGRESS] Creating the comparison system base data receiving and printing system.
- [INPROGRESS] adding method to process the tasks from worker and also brain in the base.
- [THINK] Instead of rerouting the data from brain to comparison why not use the listen to worker system in the base.s
- [INPROGRESS] Add the logic to listen to worker inside the base.
- [INROGRESS] adding different processers: 
        /-process_brain_info(), 
        /-process_brain_data(), 
        /-process_worker_info(), 
        /-process_worker_data(),
        /-handle_brain_task(),
        /-handle_worker_task(),

- [INPROGRESS] Adding some docstrings
- [INPROGRESS] Add threading for each listener in worker, for brain and worker listener.
- [INPROGRESS] Added service setting method which starts the listeners on separate thread then the method is called inside the run_worker()
- [INP] Adding specialized channels for worker 3 to listen data and message 
  - info from worker 1 to worker 3.
  - info from worker 2 to worker 3
  - data from worker 1 to worker 3
  - data from worker 2 to worker 3
- [INP] We recieve task from real time and prediction worker inside the comparison worker.
- [THINK] if the brain sends task to comparison we have to load all the datas from csv file and compare it, instead of doing it on air, which adds more complexity, 
- [INP] Modify the comparison and base worker to only listen to brain and only process file based data instead of redis based.
- [INP] make the brain to recieve the datas then tell the comparison to check for new update in the file, [LATEST DATA IN THE FILE CHECKUP LOGIC.] The latest data must match one of the datas from brain sent to comparison.
- [DONE] Removed methods no more needed.
- [DONE] Update the brain to send comparison task to comparison worker.
- [HALF-DONE] Create the data structure for comparison to be sent to brain and recognizable.
- [TASK]  data checking system  for comparison,      
        - when the c1 and c2 sends data and comparison gets the data,  
        - we have to load the data and check for confirmation if it is the latest one,
        - by comparing one key from the data file and received data, this helps in preventing 
        - the data jumps or loop holes in data processing, this system applies in brain and comparison also, 


- [THINK] we have 2 options to compare the data, 1) directly recieving from the brain, 2) loading from the file, the question is which is effecient ?
- [HALF-DONE] Creating the optional data receiving and processing in c3
- [DONE] Store the datas sent from the real time and prediction to brain in the dictionary and send it to the comparison instead of just handling indivudally.
- [DONE] Updated the data structure for both prediction and real time data also in the brain.
- [TASK] Migrate some methods in c3 to c4 since it doesnt apply to this system.
- [DONE] Editing the c3 system. 
- [DONE] Editing the c2 system to send fake data to brain.
- [DONE] Fix the data recoginition inside the brain, list index out of range error.
- [DONE] Copying the template for sending data to the c2 from c3.
- [DONE] Adding new state changeing PAUSE.
- [DONE] Fixing bug in the brain to handle the message and routing the datas to comparison.
- [DONE] Fixing the comparison data recoginition system.
- [DONE] Handle brain data in c3 , thats why we didnt recognize the data. fixed bug where the start is splitted add cant be recognized in c3.
- [DONE] Direct data recieving is not working, FIX it !in c3

## DAY 16 JAN 23
- [DONE] Modifying the save result method to save all the inforamation necessary in one place
- [DONE] Debugging the c3 data saving system.
- [DONE] YOU KNOW WHAT DONT SEND ANY DATA TO BRAIN FROM COMPARISON.
- [DONE] Creating C4.
- [DONE] Migrating Core codes from original code.
- [INP] Update the brain for task content for c4. [C4 IS CALLED AT THE END OF THE LIFE CYCLE OF THE BRAIN.]


## DAY 17 JAN 24
- [DONE] Creating the C4 Functions and one function at a time to make the AI great.
- [THINK] Analyss of rows, how many rows were "Accurate" ?, Quantify the prediction error, spot patterns (accuracy by time period, ) find problem areas (frequent deviations for specific time periods.), send feedback to prediction ai, adjust thresholds or weights, highlight weak ares(poor predictins during specific periods)

- [DONE] Creating data filtering system for the c1 and c2 to test the c3 to create sample test data for c4.
- [done] Adding duplicate detection system in the brain and c1 and c2 
-

## DAY 18 JAN 25
- [DONE] Adding data flow control and task flow control in C3 and C0
- [DONE] After the task is sent to the c3 the brain must wait for the response from c3 before sending the next task.
- [DONE] After sendint the data from c1 and c2 they must also wait for the brain.
- [DONE] Renaming BWCmd, WorkerStatus, WorkerTaskIndicator, to small verions start with W..

## DAY 19 JAN 26
- [DONE] Added feature to check for latestness of the data being recieved from the c1 and c2.
- [DONE] Fixed path problems in all scripts and moved all the scripts into root of the project.

## DAY 20 JAN 27
- [DONE] Migrating the path configuration into data class path configs and setting up the system and usage for easiness.
- [DONE] added ploting and methods to analyze the data for comparison in C4
- [DONE] Reducing the amount of data we are saving into comparison also, the needed data field from the prediction and scraper.
- ALL we need from original data:
  - "RT_PNum",
	- "RT_STime",
	- "RT_LDate",
	- "RT_TimePeriod",
	- "PD_PNum",
	- "PD_STime",
	- "PD_LDate",
	- "PD_TimePeriod",
	- "PD_Confidence",

- [TODO] Control the command excepting system, check if the state is already the given command, and reject commands,


## DAY 21 JAN 28
- [DONE] Updating C4 with feedback generation system
- [INP] 

## DAY 22 JAN 29
- [DONE] C4 Creating the system from ground up from different scripts.
- [INP] C2 working on the predcition worker to generate the prediction according to our need.
- [INP] C2 from the mpsai1 we have to derive the code implementation and use it to our advantage.
- [INP] C2 Successfully created the model training flow with some TODO's and fixed the path issues with data saving 


## DAY 22 FEB 1
- [DONE] C1 working on the scraper program to check functionality and maintain it.
- [DONE] C1 Decenteralizing the components of scraper for easy maintenance
- [DONE] C1 created different files for different classes. 
    / - s1_data_manager.py
    / - s3_scraper_process.py
    / - s2_game_data_ex.py
    / - s4_main.py
    / - real_time_data.py
- [DONE] introducing the dataclasses if it is possible.
- [DONE] C1 Declassify the scraper process since it does need the class its functional.
- [DONE] C1 Testing done , now integrate into the worker base class.
- [DONE] C1 importing and defining the methods, 
- [DONE] C1 fixed the worker base import and initializing of driver, passed the driver to main process method for the extracter to use the methods.
- [DONE] Removed bug in the state and moved the mechanics methods to the main class.
- [DONE] Fixed the error handling system in the C1,
- [DONE] Moved all scripts from their folder and out into the root, we fix the path later.

## DAY 23 FEB 2
- [DONE] C0 adding update in the manage work flow to control the real time and prediction workers 
- [DONE] Added thread based on boolean setting and added inital boolean 
- [DONE] Added scraper based status check since it takes time to load.
- [DONE] Fixing the data receiving and rerouting the data to comparison.
- [DONE] Fixed the waiting and delay time for the real time data to be ready.

## DAY 24 FEB 3
- [DONE] C0 Fixed bug in the process worker message.
- [DPNE] C1 there is issue with the data sending the data is being saved and sent at the same time i think there is race condtion going on.
- [DONE] C2 and C1 needs to wait for the command from the brain to resume when pausing instead of going into readys state.
- [DONE] Bug fixed in pausing and resuming the workers and created simple data handler instead of checking the data just reroute let c3 bother about the data.

## DAY 25 FEB 4
### Added
- [DONE] Using __init__.py to fix some path issues and importing issues.
- [DONE] Created 5 packages to simplify the project structure, C0 - C5 ,
- [DONE] Created __init__.py and used the __all__ , import * to import the packages and modules in the brain and c1_abc_main.py for now,
- [DONE] Created new system to check the scraping website status before login or proceeding to scraper.
- [DONE] C1 check_website_with_request and driver is created,
- [DONE] C1 added the chrome options from the old scraper system.
- [DONE] s4_main.py updated the main entry to stop execution of main process if the driver is not returned.
- [DONE] C0 added new shutdown system in which every steps is sequential and in order
- [DONE] C1 added new threads control system and started the brain listener and driver starter in separate thread.
- [DONE] C1 the old scraping method into one file, with maintainable system.
- [DONE] C1 Used new system to receive data from the scraper by launching it through subprocess and pipeline.
- [DONE] C1 using json we can now receive the dict value from terminal and skip unncecessary ones.
- [DONE] Now the brain starts the redis manager as subprocess and controls and the workers can recieve commands before shutdown.

### Fixed
- [DONE] Fixed the cleanup process which required the driver to be present before cleaning up.
- [DONE] Fixed the scraper process driver initialization after setting self.driver = None, then recalling preload chrome method to start the driver.
- [DONE] Fixed the import issue for subprocess, and the relative import in the packages.
- [DONE] Fixed the login and handling and banner handling if the banner is not appeared skip the banner closing and go straight to the login.
- [DONE] Fixed the shutdown sytem in the worker base,
- [DONE] Fixed bug in the thread system,
- [DONE] Fixed shutdown issues, and redis system manager issues,

### Removed
- [DONE] Removed some files with tests and redundant codes.
- [DONE] C1_utility folder is no more needed, and the separate files and modules are also deleted.
- [DONE] All the ini__.py imports are removed

- [THINK] - What if we can create subprocess for scraping program then, get the data from the file by checking if its the newest data[but that would result in late incomes] - what if we can start the subprocess but return the data to the main program and then send it to the brain, that would be more efficient and faster. but through what ? do we have to call the function or what, we are running through subprocess the data comes in dict or str that must be passed to the brain and then to the comparison.


## DAY 26 FEB 5
### Added
- [DONE] C0 Multiple commands to launch the subprocesses for easy kill.
- [DONE] New worker shutdown processes for redis servers in the redis manager.
- [DONE] Added the subprocess killing mechanism for all the workers and redis manager script
- [DONE] Added new temproray terminal command and permament terminal command for the subprocesses to run on, this will be converted to settings later.
- [DONE] added new temp terminal command again to start the child processes as new session.
-  

### Changed
- [DONE] C2_fake_data testing script is changed.
- [DONE]

### Fixed

- [DONE] RM Multiple server kill calling BUG that was killing already launching server instead of old ones, 
- [DEON] The old prediction system is working perfectly.

### Removed
- [DONE] stop redis method is no longer needed if we can kill the server using the subprocess
- [DONE] C0 Redudant code for shutting down the redis manager servers, before killing the subprocess must servers die.

## DAY 27 FEB 6
### Added
- [DONE] C0 new data processing system, br_process_data.py and br_combine_data.py which combines and sorts does all the job for the ai.
- [DONE] C2_abc_pai_detailed.py which is more commented and structured version of prediction system
- [DONE] C2_abc_pai_setting_based.py which is the setting based system that can be tuned to train the model using the json.
- [DONE] C2 Added cyclical time features in sin and cos form
- [DONE] In the data combiner now duplicates are drop in two stages, and new tdiff is calculated the way we want it.
- [DONE] C2 Added more settings option to the json.
- [DONE] C2 Feature engineering completed successfully with 126 columns in total.
- [DONE] C2 Added the new metrics settings.
- [DONE] C2 added the parameter configuration into settings based 
- [DONE] C2 added new metrics for prediction and model evaluation.


### Changed

- [DONE] Data file processing system is now updated to accomodate the white trailing and any data can be processed by it.
- [DONE] Data combiner now drops all the duplicates using the round no identification system.


### Fixed
- [DONE] The data source for all the prediction is in one place
- [DONE] The gitignore will now doesnt ignore the csv and models 
- [DONE] Optimization on the data frame insertation while training.
- [DONE] Even better more optimization and control over feature addtion and removeing by creating separate data class.
- [DONE] Bugs fixed and feature naming and self.feature_names population with different features.

### Removed
- [DONE] Removed the tdiff creation in the prepare data method.
- 


## DAY 28 FEB 7
### Added
- [DONE] C2 defualt stats calcualtion and optimization
- [DONE] C2 the single prediction features now use calculated values instead of placeholder

### Fixed
- [DONE] C2 the path of model saving.
- [DONE] Fixes the Overwriting Issue: win_features now accumulates correctly.
- [DONE] Prevents "Scalar Value Without Index" Error: All new feature DataFrames have at least one row.
- [DONE] Ensures All Features Are Properly Merged: No more empty or missing values.


## DAY 29 FEB 17

### Added
- [DONE] Created separate scripts on the new real time worker code.
- [DONE] Created the scraper worker update version 2 with no redis.

### Fixed

- [DONE] Successfully separated the codes from the new versions into their own scripts.
- [DONE] Formatted and fixed some typos in the C0 brain code.


### Removed

- [DONE] Removed the old real time worker code.
- [DONE] Removed the codes inside `M1_main.py` which were used in the other ms.
- [DONE] Removed the old prediction worker code.



## DAY 30 FEB 18

### Added

- [INP] Using railway oriented programming for the prediction system.


## DAY 31 MARCH 06
### Added

### Fixed 
- [DONE] Path issues in stime by importing the path from the config file.
- [DONE] Created separate trainer and model finder for the stime model.
- [TODO] Implement the report interpretation from the old code.
- [TODO] Implement the same logic for the pnum model finder the model report interpretation using api.