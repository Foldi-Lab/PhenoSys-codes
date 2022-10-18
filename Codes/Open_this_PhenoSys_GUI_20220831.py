# -----------------------------------------------------------------------------

# Choose the default values in the GUI.

import sys
import PySimpleGUI as sg
default = {}

# Choose the test and type of analysis.
default["Task"] = '2VDLR'
default["Analysis"] = 'Organisation'

# Choose the import and export locations
# Note that these locations should have no slash at the end.
default["Import location"] = 'C:/Users/hazza/Desktop/Phenosys data/Import folder'
default["Export location"] = 'C:/Users/hazza/Desktop/Phenosys data/Export folder'

# Choose where the analysed data should go and the length of the time bin in mins.
# This should be "Add to new file" or "Add to original file".
default["Analysis location"] = "Add to new file"
default["Time bin"] = 1

# Choose the import locations of the raw excel file and video.
# These two destinations should have the files included at the end.
default["Excel import destination"] = 'C:/Users/hazza/Desktop/Phenosys data/Import folder/Raw data.xlsx'
default["Video import destination"] = 'C:/Users/hazza/Desktop/Phenosys data/Import folder/Video.mp4'

# Choose the export location for the snipped videos and the output video format.
# This location should have no slash at the end.
default["Video export location"] = 'C:/Users/hazza/Desktop/Phenosys data/Export folder'
default["Video format"] = '.mp4'

# -----------------------------------------------------------------------------


# Import the GUI module.


no_runs = 1  # One run is defined as a one loop through all the GUI windows.
every = {}  # The input values for every run are stored here.

while True:
    
    print('\nInputs for run '+str(no_runs))

    # Create a dictionary for the types of analysis for each task.
    tasks = {}
    tasks['GTPT234'] = ['Organisation', 'Shorter organisation',
                        'Time bins of sessions', 'Daily and cumulative time bins',
                        'Video snipping']
    tasks['GTPT5'] = ['Organisation', 'Shorter organisation',
                      'Time bins of sessions', 'Daily and cumulative time bins',
                      'Video snipping']
    tasks['2VDLR'] = ['Organisation', 'Time bins of sessions',
                      'Daily and cumulative time bins', 'Video snipping']
    tasks['5CSRTT'] = ['Organisation', 'Time bins of sessions',
                       'Daily and cumulative time bins', 'ITIs and SDs separated',
                       'ITIs and SDs together', 'Video snipping']
    tasks['TUNL'] = ['Organisation', 'Time bins of sessions',
                     'Daily and cumulative time bins', 'Video snipping']
    # Create a dictionary for the number of arguments in each corresponding function.
    # 4 refers to types of analysis with 4 function arguments, 5 refers to 5 arguments
    # and V refers to video snipping.
    arguments = {}
    arguments['4'] = ['Organisation', 'Shorter organisation', 'ITIs and SDs separated',
                      'ITIs and SDs together']
    arguments['5'] = ['Time bins of sessions',
                      'Daily and cumulative time bins']
    arguments['V'] = ['Video snipping']
    # Create a dictionary for the inputs into the GUI.
    inputs = {}

    # Create a GUI for choosing the task.
    sg.theme("DarkTeal2")
    layout = [
        [sg.T("")], [sg.Text("Choose the test"),
                     sg.Combo(list(tasks.keys()), key="Task", enable_events=True,
                              default_value=default["Task"])],
        [sg.T("")], [sg.Button("Submit")]
    ]
    window = sg.Window('My File Browser', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            sys.exit()
        elif event == "Submit":
            inputs["Task"] = values["Task"]
            window.close()
            break
    print('Task is ' + inputs["Task"])

    # Create a GUI for choosing the type of analysis.
    sg.theme("DarkTeal2")
    layout = [
        [sg.T("")], [sg.Text("Choose the analysis"),
                     sg.Combo(tasks[inputs["Task"]], key="Analysis", enable_events=True,
                              default_value=default["Analysis"])],
        [sg.T("")], [sg.Button("Submit")]
    ]
    window = sg.Window('My File Browser', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            sys.exit()
        elif event == "Submit":
            inputs["Analysis"] = values["Analysis"]
            window.close()
            break
    print('Analysis is ' + inputs["Analysis"])

    # Create a GUI for the inputs to the functions corresponding to the type
    # of analysis.

    sg.theme("DarkTeal2")
    layout = []

    # For the types of analysis in arugments['4'], an import location, export
    # location and location for the analysis are needed.
    if inputs["Analysis"] in (arguments['4'] + arguments['5']):
        layout += [
            [sg.T("")], [sg.Text("Choose a folder for the import location"),
                         sg.Input(key="Import", enable_events=True,
                                  default_text=default["Import location"]), sg.FolderBrowse()],
            [sg.T("")], [sg.Text("Choose a folder for the export location"),
                         sg.Input(key="Export", enable_events=True,
                                  default_text=default["Export location"]), sg.FolderBrowse()],
            [sg.T("")], [sg.Text("Choose where the analysis should go"),
                         sg.Combo(["Add to new file", "Add to original file"], key="Location",
                                  enable_events=True, default_value=default["Analysis location"])]]
        # For the types of analysis in arguments['5'], a time bin length is also needed.
        if inputs["Analysis"] in arguments['5']:
            layout += [[sg.T("")], [sg.Text("Choose the time bin length (in mins)  "),
                                    sg.Input(key="Time bin", enable_events=True,
                                             default_text=default["Time bin"], size=(10, 1))]]

    # The type of analysis in arguments['V'] (video snipping) needs 4 different input arguments.
    elif inputs["Analysis"] in arguments['V']:
        layout += [
            [sg.T("")], [sg.Text("Choose the excel file to import     "),
                         sg.Input(key="Import1", enable_events=True,
                                  default_text=default["Excel import destination"]), sg.FileBrowse()],
            [sg.T("")], [sg.Text("Choose the video to import          "),
                         sg.Input(key="Import2", enable_events=True,
                                  default_text=default["Video import destination"]), sg.FileBrowse()],
            [sg.T("")], [sg.Text("Choose the video export location  "),
                         sg.Input(key="Export1", enable_events=True,
                                  default_text=default["Video export location"]), sg.FolderBrowse()],
            [sg.T("")], [sg.Text("Choose the video format (eg .mp4)"),
                         sg.Input(key="Video format", enable_events=True,
                                  default_text=default["Video format"])]]

    layout += [[sg.T("")], [sg.Button("Submit"),
                            sg.Text(137*" "), sg.Button("Queue")]]
    window = sg.Window('My File Browser', layout)

    # After pressing submit, assign the GUI values to variables.
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            sys.exit()
        elif event in ["Submit", "Queue"]:
            if inputs["Analysis"] in (arguments['4'] + arguments['5']):
                import_location = values["Import"]
                export_location = values["Export"]
                import_location += '/'
                export_location += '/'
                if values["Location"] == "Add to original file":
                    add_data_to_original_file = True
                    add_data_to_new_file = False
                elif values["Location"] == "Add to new file":
                    add_data_to_original_file = False
                    add_data_to_new_file = True
                location = values["Location"]
                if inputs["Analysis"] in arguments['5']:
                    time_step = float(values["Time bin"])
            elif inputs["Analysis"] in arguments['V']:
                import_destination_excel = values["Import1"]
                import_destination_video = values["Import2"]
                export_location_video = values["Export1"]
                export_location_video += '/'
                video_format = values["Video format"]
            if event == "Queue":
                add_to_queue = True
            else:
                add_to_queue = False
            break

    # Print the results in the console, so they can be checked.
    if inputs["Analysis"] in (arguments['4'] + arguments['5']):
        print('Import location is ' + import_location)
        print('Export location is ' + export_location)
        print('Add analysis ' + location[4:])
        if inputs["Analysis"] in arguments['5']:
            print('Time bin is ' + str(time_step) + ' mins')
    elif inputs["Analysis"] in arguments['V']:
        print('Excel import destination is ' + import_destination_excel)
        print('Video import destination is ' + import_destination_video)
        print('Video export location is ' + export_location_video)
        print('Video format is ' + video_format)

    # Run the correct Phenosys code.

    # Each code is wrapped around one function and those are imported.
    from Code_GTPT234 import fGTPT234
    from Code_GTPT234_Simpler import fGTPT234_Simpler
    from Code_GTPT234_Time_Bins_of_Sessions import fGTPT234_Time_Bins_Sessions
    from Code_GTPT234_Time_Bins_Overall import fGTPT234_Time_Bins_Overall
    from Code_GTPT5 import fGTPT5
    from Code_GTPT5_Simpler import fGTPT5_Simpler
    from Code_GTPT5_Time_Bins_of_Sessions import fGTPT5_Time_Bins_Sessions
    from Code_GTPT5_Time_Bins_Overall import fGTPT5_Time_Bins_Overall
    from Code_2VDLR import f2VDLR
    from Code_2VDLR_Time_Bins_of_Sessions import f2VDLR_Time_Bins_Sessions
    from Code_2VDLR_Time_Bins_Overall import f2VDLR_Time_Bins_Overall
    from Code_5CSRTT import f5CSRTT
    from Code_5CSRTT_Time_Bins_of_Sessions import f5CSRTT_Time_Bins_Sessions
    from Code_5CSRTT_Time_Bins_Overall import f5CSRTT_Time_Bins_Overall
    from Code_5CSRTT_with_ITIs_and_SDs_Separated import f5CSRTT_ITIs_SDs_Separated
    from Code_5CSRTT_with_ITIs_and_SDs_Together import f5CSRTT_ITIs_SDs_Together
    from Code_TUNL import fTUNL
    from Code_TUNL_Time_Bins_of_Sessions import fTUNL_Time_Bins_Sessions
    from Code_TUNL_Time_Bins_Overall import fTUNL_Time_Bins_Overall
    from Code_Video_Snipping import fVideo_Snipping

    # Organise the functions for each code by the tasks and types of analysis.
    functions = {}
    functions['GTPT234'] = {'Organisation': fGTPT234,
                            'Shorter organisation': fGTPT234_Simpler,
                            'Time bins of sessions': fGTPT234_Time_Bins_Sessions,
                            'Daily and cumulative time bins': fGTPT234_Time_Bins_Overall,
                            'Video snipping': fVideo_Snipping}
    functions['GTPT5'] = {'Organisation': fGTPT5,
                          'Shorter organisation': fGTPT5_Simpler,
                          'Time bins of sessions': fGTPT5_Time_Bins_Sessions,
                          'Daily and cumulative time bins': fGTPT5_Time_Bins_Overall,
                          'Video snipping': fVideo_Snipping}
    functions['2VDLR'] = {'Organisation': f2VDLR,
                          'Time bins of sessions': f2VDLR_Time_Bins_Sessions,
                          'Daily and cumulative time bins': f2VDLR_Time_Bins_Overall,
                          'Video snipping': fVideo_Snipping}
    functions['5CSRTT'] = {'Organisation': f5CSRTT,
                           'Time bins of sessions': f5CSRTT_Time_Bins_Sessions,
                           'Daily and cumulative time bins': f5CSRTT_Time_Bins_Overall,
                           'ITIs and SDs separated': f5CSRTT_ITIs_SDs_Separated,
                           'ITIs and SDs together': f5CSRTT_ITIs_SDs_Together,
                           'Video snipping': fVideo_Snipping}
    functions['TUNL'] = {'Organisation': fTUNL,
                         'Time bins of sessions': fTUNL_Time_Bins_Sessions,
                         'Daily and cumulative time bins': fTUNL_Time_Bins_Overall,
                         'Video snipping': fVideo_Snipping}

    # Assign the function arguments to 'variables'.
    if inputs["Analysis"] in arguments['4']:
        inputs["Variables"] = [import_location, export_location, add_data_to_new_file,
                               add_data_to_original_file]
    elif inputs["Analysis"] in arguments['5']:
        inputs["Variables"] = [import_location, export_location, add_data_to_new_file,
                               add_data_to_original_file, time_step]
    elif inputs["Analysis"] in arguments['V']:
        inputs["Variables"] = [import_destination_excel, import_destination_video,
                               export_location_video, video_format]

    # Add to queue if this is selected.
    every["Run "+str(no_runs)] = inputs
    if add_to_queue == False:
        for run_no in every.keys():

            inputs = every[run_no]

            print('\n'+run_no)

            print('\nStarted analysis')

            functions[inputs['Task']][inputs['Analysis']](*inputs["Variables"])

            print('Finished analysis\n')
        
        window.close()
        break

    # Update the default values with the input values for the next run.
    default["Task"] = inputs["Task"]
    default["Analysis"] = inputs["Analysis"]
    if inputs["Analysis"] in (arguments['4'] + arguments['5']):
        default["Import location"] = import_location
        default["Export location"] = export_location
        if add_data_to_new_file == True:
            default["Analysis location"] = "Add to new file"
        elif add_data_to_new_file == False:
            default["Analysis location"] = "Add to original file"
        if inputs["Analysis"] in arguments['5']:
            default["Time bin"] = time_step
    elif inputs["Analysis"] in arguments['V']:
        default["Excel import destination"] = import_destination_excel
        default["Video import destination"] = import_destination_video
        default["Video export location"] = export_location_video
        default["Video format"] = video_format

    window.close()
    no_runs += 1
