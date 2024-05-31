import pandas as pd
import PySimpleGUI as sg
import os
from tqdm import tqdm
import numpy as np
import sys

import_location = r"C:\Users\hazza\Downloads\2VDLR_Tests\Import"
export_location = r"C:\Users\hazza\Downloads\2VDLR_Tests\Export"
sg.theme("DarkTeal2")
layout = [
    [sg.T("")], [sg.Text("Import a folder of raw 2VDLR excel files and export an "+
                         "excel file with the latency data.")],
    [sg.T("")], [sg.Text("Choose a folder for the import location"), 
                 sg.Input(default_text=import_location,key="Import",
                          enable_events=True),sg.FolderBrowse(key="Import2")],
    [sg.T("")], [sg.Text("Choose a folder for the export location"),
                 sg.Input(default_text=export_location,key="Export",
                          enable_events=True),sg.FolderBrowse(key="Export2")],
    [sg.T("")], [sg.Button("Submit")]
         ]
window = sg.Window('Options for analysis', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        window.close()
        sys.exit()
    elif event == "Submit":
        import_location = values["Import"]
        export_location = values["Export"]
        window.close()
        break

# Create a loop over every excel file in the import location.

master = pd.DataFrame()

import_files = [file for file in os.listdir(import_location) if 
                (file.endswith(".xlsx") and file.startswith("~$")==False)]

for filename in tqdm(import_files, ncols=70):
    
    # Import the excel data
    
    import_name = filename
    import_destination = os.path.join(import_location, import_name)
    
    df = pd.read_excel(import_destination, sheet_name=0, usecols=['DateTime','IdRFID','IdLabel','outLabel','SystemMsg','MsgValue1','MsgValue2','MsgValue3'])
    
    # Add 'positive' string from column 'outLabel' to column 'SystemMsg'.
    for i in range(len(df['outLabel'])):
        if df.at[i,'outLabel'] == 'positive':
            df.at[i,'SystemMsg'] = df.at[i,'outLabel']
            
    # Delete rows in the imported data if the entry in column 'SystemMsg' is not 'end exp', 'incorrect', 'omission', 'positive', 'start exp' or 'premature'.
    # Delete column M ('outLabel').
    # Identify the start and end times of the experiment.
    
    del_indicies = []
    start_time = ''
    end_time = ''
    list_keywords = ['correct', 'incorrect', 'omission', 'response latency', 'collection latency', 'start exp', 'end exp']
    
    for i in range(len(df['SystemMsg'])):
        if df.at[i,'SystemMsg'] not in list_keywords:
            del_indicies.append(i)
        if df.at[i,'SystemMsg'] == 'start':
            start_time = df.at[i,'DateTime']
        if df.at[i,'SystemMsg'] != 'end':
            end_time = df.at[i,'DateTime']
            
    df = df.drop(del_indicies)
    df = df.drop(columns=['outLabel'])
    df.index = list(range(len(df)))
    
    # If the dataframe is emtpy, skip this file.
    if len(df) == 0:
        continue
    
    # Ensure that the DateTime column is in a datetime format and not a string.
    if type(df['DateTime'].iloc[0]) == str:
        possible_formats = [None, '%d/%m/%Y %H.%M.%S.%f']
        for form in possible_formats:
            df['DateTime'] = pd.to_datetime(df['DateTime'], format=form, errors='ignore')
            if type(df['DateTime'].iloc[0]) != str:
                start_time = pd.to_datetime(start_time, format=form)
                end_time   = pd.to_datetime(end_time, format=form)
                break
        if type(df['DateTime'].iloc[0]) == str:
            print('A new datetime format needs to be included in the code.')
            sys.exit()
            
    # Sort all the rows by the column 'IdLabel'.
    # Within those identical entries in 'IdLabel', sort by the column 'DateTime'.
    
    df = df.sort_values(by=['IdLabel','DateTime'], na_position='last')

    # Find the length of the longest session in the file.
    # A session is a section from 'start exp' to 'end exp'.
    # At the same time, find all unique image positions and if there is no end exp before a start exp, add one in.
    
    best_counter = 0
    counter = 0
    list_image_positions = []
    no_end_exp = []
    df.index = list(range(len(df)))
    
    for i in range(len(df['SystemMsg'])):
        counter += 1
        if df['SystemMsg'].iloc[i] == 'end exp':
            if counter > best_counter:
                best_counter = counter
            counter = 0
            
        if i!=0 and df['SystemMsg'].iloc[i]=='start exp' and df['SystemMsg'].iloc[i-1]!='end exp':
            no_end_exp.append(i-1)
            
        # Add 'positive' or 'negative' to the 'response latency' events.
        if df.at[i,'SystemMsg'] == 'response latency':
            df.at[i,'SystemMsg'] = df.at[i,'SystemMsg'] + ' (' + df.at[i,'MsgValue2'] + ')'

    for ind in no_end_exp:
        df.loc[ind+0.5] = df.loc[ind]
        df.at[ind+0.5,'DateTime'] = np.nan
        df.at[ind+0.5,'SystemMsg'] = 'end exp'
    df = df.sort_index()
    df.index = list(range(len(df)))
    
    # Add extra time and session columns to the 'Overall sheet', so the sessions can be sliced out of the videos.
    current_session = 0
    current_idlabel = df['IdLabel'].iloc[0]
    session_record = []
    
    for i in range(len(df['DateTime'])):
        if current_idlabel != df['IdLabel'].iloc[i]:
            current_idlabel = df['IdLabel'].iloc[i]
            current_session = 0
        if df['SystemMsg'].iloc[i] == 'start exp':
            current_session += 1
        session_record.append(current_session)
    df.insert(0, 'Session number', session_record, True)

    # Import the data and exclude rows that do not record latencies.
    # path = r"C:\Users\hazza\Desktop\Import 2\(ITIs and SDs Together) Organised 2VDLR-22.05.12 Sys20.xlsx"
    # df = pd.read_excel(path)
    df['Filename'] = os.path.basename(import_destination)
    df = df[df['SystemMsg'].str.contains('latency')]
    
    # Group these results by animal and then type of latency.
    df_results = df.groupby(by=['Filename','IdLabel','Session number','SystemMsg']).agg(list)
    df_results = df_results.rename(columns={'MsgValue1': 'List of latencies'})
    
    df_results['Sum of latencies']     = df_results['List of latencies'].apply(sum)
    df_results['Number of latencies']  = df_results['List of latencies'].apply(len)
    df_results['Average of latencies'] = df_results['Sum of latencies'] / df_results['Number of latencies']
    
    keep_columns = ['Sum of latencies', 'Number of latencies', 'Average of latencies']
    df_results = df_results[keep_columns]
    
    master = pd.concat([master, df_results])

if len(master) == 0:
    print("There is no response or latency data to collect.")
    sys.exit()

master = master.reset_index()
files  = master['Filename'].str.split('-',expand=True)[1]
date   = files.str.split(' ',expand=True)[0]
date   = pd.to_datetime(date, yearfirst=True)
system = files.str.split(' ',expand=True)[1]
master.insert(1, 'Date', date)
master.insert(2, 'System', system)
export_name = 'Master.xlsx'
export_destination = os.path.join(export_location, export_name)
master.to_excel(export_destination, index=False)