def f2VDLR(import_location, export_location, add_data_to_new_file, add_data_to_original_file):
    
    import os
    import pandas as pd
    from openpyxl import load_workbook
    import sys
    import numpy as np
    from tqdm import tqdm
    
    # Define functions for color coding.
    
    def text_color(val):
        
        if type(val) != str or 'P+I' in val or 'Number' in val or '(ms)' in val:
            return 'color: %s' % 'black'
    
        if 'end' in val:
            color = '#FFFFFF' # White for 'end'
        elif 'start' in val:
            color = '#FFFFFF' # White for 'start'
        elif 'omis' in val:
            color = '#9C5600' # Dark yellow for 'omis'
        elif 'posi' in val:
            color = '#4E7C3E' # Dark green for 'posi'
        elif val == 'correct':
            color = '#4E7C3E' # Dark green for 'posi'
        elif 'inco' in val:
            color = '#9C1B14' # Dark red for 'inco'
        elif val == 'response latency':
            color = '#63503c' # Dark indigo for 'response latency'
        elif val == 'collection latency':
            color = '#4472C4' # Blue for 'collection latency'
            
        else:
            color = 'black'
            
        return 'color: %s' % color
    
    def cell_color(val): 
        
        if type(val) != str or 'P+I' in val or 'Number' in val or '(ms)' in val:
            return 'background-color: %s' % 'none'
    
        if 'end' in val:
            color = '#000000' # Black for 'end'
        elif 'start' in val:
            color = '#6C2C9D' # Purple for 'start'
        elif 'omis' in val:
            color = '#FCEB9C' # Yellow for 'omis'
        elif 'posi' in val:
            color = '#C3EFCC' # Green for 'posi'
        elif val == 'correct':
            color = '#C3EFCC' # Green for 'posi'
        elif 'inco' in val:
            color = '#FBC4CD' # Red for 'inco'
        elif val == 'response latency':
            color = '#fae0c5' # Indigo for 'response latency'
        elif val == 'collection latency':
            color = '#D9E1F2' # Light blue for 'collection latency'
            
        else:
            color = 'none'
            
        return 'background-color: %s' % color
    
    def bold_titles(val):
        return 'font-weight: bold'
    
    # Create a loop over every excel file in the import location.
    
    import_files = [file for file in os.listdir(import_location) if (file.endswith(".xlsx") and file.startswith("~$")==False)]
    
    for filename in tqdm(import_files, ncols=70):

        # Import the excel data
        
        import_name = filename
        import_destination = import_location + import_name
        export_name = 'Organised ' + import_name
        export_destination = export_location + export_name
        
        df = pd.read_excel(import_destination, sheet_name=0, usecols=['DateTime','IdRFID','IdLabel','outLabel','SystemMsg','MsgValue1','MsgValue2','MsgValue3'])
        #df = pd.read_excel(import_destination, sheet_name=0, usecols="A,B,C,M,N,O,P,Q")
        
        # Add 'positive' string from column 'outLabel' to column 'SystemMsg'.
        
        for i in range(len(df['outLabel'])):
            if df.at[i,'outLabel'] == 'positive':
                df.at[i,'SystemMsg'] = df.at[i,'outLabel']
                
        # Delete rows in the imported data if the entry in column 'SystemMsg' 
        # is not 'end exp', 'incorrect', 'omission', 'positive' or 'start exp'.
        # Also delete column M ('outLabel').
        
        del_indicies = []
        include_names = ['start exp', 'end exp', 'positive', 'incorrect', 'omission', 'response latency', 'collection latency']
        
        for i in range(len(df['SystemMsg'])):
            if df.at[i,'SystemMsg'] not in include_names:
                del_indicies.append(i)
            if df.at[i,'SystemMsg'] == 'start':
                start_time = df.at[i,'DateTime']
            if df.at[i,'SystemMsg'] == 'end':
                end_time = df.at[i,'DateTime']
                
        df = df.drop(del_indicies)
        df = df.drop(columns=['outLabel'])
        
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
        # At the same time, if there is no end exp before a start exp, add one in.
        
        best_counter = 0
        counter = 0
        no_end_exp = []
        df.index = list(range(len(df)))
        
        for i in range(len(df['SystemMsg'])):
            
            # # Put all the latency information into one cell.
            # # For example, this might be 'response latency,right,50000'
            # if df['SystemMsg'].iloc[i] == 'response latency':
            #     new_name = [df['SystemMsg'].iloc[i], df['MsgValue2'].iloc[i], str(df['MsgValue1'].iloc[i])]
            #     new_name = ','.join(new_name)
            #     df['SystemMsg'].iloc[i] = new_name
            
            counter += 1
            if df['SystemMsg'].iloc[i] == 'end exp':
                if counter > best_counter:
                    best_counter = counter
                counter = 0
            if i!=0 and df['SystemMsg'].iloc[i]=='start exp' and df['SystemMsg'].iloc[i-1]!='end exp':
                no_end_exp.append(i-1)
                
        for ind in no_end_exp:
            df.loc[ind+0.5] = df.loc[ind]
            df.at[ind+0.5,'DateTime'] = np.nan
            df.at[ind+0.5,'SystemMsg'] = 'end exp'
        df = df.sort_index()
        df.index = list(range(len(df)))
        
        # Organise the sessions in column 'SystemMsg' into separate sheets.
        
        list_labels = []
        list_dfs = []
        list_cols = []
        list_cols_val1 = []
        list_cols_val2 = []
        list_cols_time = []
        list_titles = []
        
        for i in range(len(df['SystemMsg'])):
            
            label_name = df['IdLabel'].iloc[i]
            system_name = df['SystemMsg'].iloc[i]
            msgvalue_name = df['MsgValue1'].iloc[i]
            msgvalue2_name = df['MsgValue2'].iloc[i]
            time_name = df['DateTime'].iloc[i]
            if i!=len(df['SystemMsg'])-1:
                next_system_name = df['SystemMsg'].iloc[i+1]
            
            # Starting a new rat ID label (in column 'IdLabel').
            if (label_name not in list_labels) and (system_name == 'start exp'):
                    
                time_name = df['DateTime'].iloc[i]
                code_name = df['IdRFID'].iloc[i]
                list_labels.append(label_name)                
                list_dfs.append(pd.DataFrame({'':[]}))
                list_cols.append([])
                list_cols_val1.append([])
                list_cols_val2.append([])
                list_cols_time.append([])
                list_titles.append(label_name)
                
                g_tot_startexp = 0
                g_tot_correctlatency = 0
                g_tot_incorrectlatency = 0
                g_tot_omissionlatency = 0
                g_tot_correctlatency_count = 0
                g_tot_incorrectlatency_count = 0
                g_tot_omissionlatency_count = 0
                g_tot_positive = 0
                g_tot_incorrect = 0
                g_tot_omission = 0
                g_tot_endexp = 0
                g_tot_trials = 0
                g_tot_collection = 0
                g_tot_collection_count = 0
            
            # Starting a new session (in column 'SystemMsg').
            elif (label_name in list_labels) and (system_name == 'start exp'):
                
                time_name = df['DateTime'].iloc[i]
                list_cols.append([])
                list_cols_val1.append([])
                list_cols_val2.append([])
                list_cols_time.append([])
            
            # Recording the event (in column 'SystemMsg').
            list_cols[-1].append(system_name)
            list_cols_time[-1].append(time_name)
            list_cols_val1[-1].append(msgvalue_name)
            list_cols_val2[-1].append(msgvalue2_name)
            
            # Ending a session (in column 'SystemMsg').
            if system_name == 'end exp' or next_system_name == 'start exp':
                
                while len(list_cols[-1]) < best_counter:
                    list_cols[-1].append('')
                    list_cols_time[-1].append('')
                    list_cols_val1[-1].append('')
                    list_cols_val2[-1].append('')
                    
                # Add data about each session.
                tot_startexp = 0
                tot_correctlatency = 0
                tot_incorrectlatency = 0
                tot_omissionlatency = 0
                tot_correctlatency_count = 0
                tot_incorrectlatency_count = 0
                tot_omissionlatency_count = 0
                tot_positive = 0
                tot_incorrect = 0
                tot_omission = 0
                tot_endexp = 0
                tot_trials = 0
                tot_collection = 0
                tot_collection_count = 0
                
                #for event in list_cols[-1]:
                    
                for ind in range(len(list_cols[-1])):
                    
                    event = list_cols[-1][ind]
                    val1  = list_cols_val1[-1][ind]
                    val2  = list_cols_val2[-1][ind]
                    
                    if event == 'start exp':
                        tot_startexp += 1
                    elif event == 'positive':
                        tot_positive += 1
                    elif event == 'incorrect':
                        tot_incorrect += 1
                    elif event == 'omission':
                        tot_omission += 1
                    elif event == 'end exp':
                        tot_endexp += 1
                    elif 'latency' in event:
                        if 'response' in event:
                            if val2 == 'correct':
                                tot_correctlatency         += val1
                                tot_correctlatency_count   += 1
                            elif val2 == 'incorrect':
                                tot_incorrectlatency       += val1
                                tot_incorrectlatency_count += 1
                            elif val2 == 'omission':
                                tot_omissionlatency        += val1
                                tot_omissionlatency_count  += 1
                        elif 'collection' in event:
                            tot_collection                 += val1
                            tot_collection_count           += 1
                tot_trials = tot_positive + tot_incorrect + tot_omission
                        
                g_tot_startexp += tot_startexp
                g_tot_correctlatency += tot_correctlatency
                g_tot_incorrectlatency += tot_incorrectlatency
                g_tot_omissionlatency += tot_omissionlatency
                g_tot_correctlatency_count += tot_correctlatency_count
                g_tot_incorrectlatency_count += tot_incorrectlatency_count
                g_tot_omissionlatency_count += tot_omissionlatency_count
                g_tot_positive += tot_positive
                g_tot_incorrect += tot_incorrect
                g_tot_omission += tot_omission
                g_tot_endexp += tot_endexp
                g_tot_trials += tot_trials
                g_tot_collection += tot_collection
                g_tot_collection_count += tot_collection_count
                        
                for j in range(len(list_cols[-1])):
                    if list_cols[-1][j] == 'start exp':
                        temp_time1 = list_cols_time[-1][j]
                    elif list_cols[-1][j] == 'end exp':
                        temp_time2 = list_cols_time[-1][j]
                
                if pd.isna(temp_time2) or pd.isna(temp_time1):
                    len_session = np.nan
                else:
                    len_session = temp_time2 - temp_time1
                    # Make the session lengths time in minutes.
                    len_session = len_session.total_seconds() / 60
                    
                ### positive, incorrect and omission analysis ###
                if (tot_positive + tot_incorrect) == 0:
                    prop_positive_PI = 0
                    prop_incorrect_PI = 0
                else:
                    prop_positive_PI = (tot_positive * 100) / (tot_positive + tot_incorrect)
                    prop_incorrect_PI = (tot_incorrect * 100) / (tot_positive + tot_incorrect)
                    
                if (tot_positive + tot_incorrect + tot_omission) == 0:
                    prop_positive_PIO = 0
                    prop_incorrect_PIO = 0
                    prop_omitted_PIO = 0
                else:
                    prop_positive_PIO = (tot_positive * 100) / (tot_positive + tot_incorrect + tot_omission)
                    prop_incorrect_PIO = (tot_incorrect * 100) / (tot_positive + tot_incorrect + tot_omission)
                    prop_omitted_PIO = (tot_omission * 100) / (tot_positive + tot_incorrect + tot_omission)
                total_PI  = prop_positive_PI + prop_incorrect_PI
                total_PIO = prop_positive_PIO + prop_incorrect_PIO + prop_omitted_PIO
                
                ### grand total positive, incorrect and omission analysis ###
                if (g_tot_positive + g_tot_incorrect) == 0:
                    g_prop_positive_PI = 0
                    g_prop_incorrect_PI = 0
                else:
                    g_prop_positive_PI = (g_tot_positive * 100) / (g_tot_positive + g_tot_incorrect)
                    g_prop_incorrect_PI = (g_tot_incorrect * 100) / (g_tot_positive + g_tot_incorrect)
                    
                if (g_tot_positive + g_tot_incorrect + g_tot_omission) == 0:
                    g_prop_positive_PIO = 0
                    g_prop_incorrect_PIO = 0
                    g_prop_omitted_PIO = 0
                else:
                    g_prop_positive_PIO = (g_tot_positive * 100) / (g_tot_positive + g_tot_incorrect + g_tot_omission)
                    g_prop_incorrect_PIO = (g_tot_incorrect * 100) / (g_tot_positive + g_tot_incorrect + g_tot_omission)
                    g_prop_omitted_PIO = (g_tot_omission * 100) / (g_tot_positive + g_tot_incorrect + g_tot_omission)
                g_total_PI  = g_prop_positive_PI + g_prop_incorrect_PI
                g_total_PIO = g_prop_positive_PIO + g_prop_incorrect_PIO + g_prop_omitted_PIO
                
                ### Latency analysis ###
                if tot_correctlatency_count == 0:
                    tot_correctlatencyavg = 0
                else:
                    tot_correctlatencyavg = (tot_correctlatency / tot_correctlatency_count)
                if tot_incorrectlatency_count == 0:
                    tot_incorrectlatencyavg = 0
                else:
                    tot_incorrectlatencyavg = (tot_incorrectlatency / tot_incorrectlatency_count)
                if tot_omissionlatency_count == 0:
                    tot_omissionlatencyavg = 0
                else:
                    tot_omissionlatencyavg = (tot_omissionlatency / tot_omissionlatency_count)
                if tot_collection_count == 0:
                    tot_collectionavg = 0
                else:
                    tot_collectionavg = (tot_collection / tot_collection_count)
                    
                ### Grand total latency analysis ###
                if g_tot_correctlatency_count == 0:
                    g_tot_correctlatencyavg = 0
                else:
                    g_tot_correctlatencyavg = (g_tot_correctlatency / g_tot_correctlatency_count)
                if g_tot_incorrectlatency_count == 0:
                    g_tot_incorrectlatencyavg = 0
                else:
                    g_tot_incorrectlatencyavg = (g_tot_incorrectlatency / g_tot_incorrectlatency_count)
                if g_tot_omissionlatency_count == 0:
                    g_tot_omissionlatencyavg = 0
                else:
                    g_tot_omissionlatencyavg = (g_tot_omissionlatency / g_tot_omissionlatency_count)
                if g_tot_collection_count == 0:
                    g_tot_collectionavg = 0
                else:
                    g_tot_collectionavg = (g_tot_collection / g_tot_collection_count)
                
                # Put these statistics above the event data colours.
                ex_vals   = []
                ex_names  = []
                ex_vals  += [ tot_startexp,                 tot_omission,                tot_positive,                tot_incorrect,                tot_endexp,                 tot_trials,                '']
                ex_names += ['Number of start exp trials', 'Number of omission trials', 'Number of positive trials', 'Number of incorrect trials', 'Number of end exp trials', 'Number of trials (P+I+O)', '']
                ex_vals  += [ tot_omissionlatency,                       tot_correctlatency,                       tot_incorrectlatency,                       tot_collection                   ]
                ex_names += ['Sum of omission response latencies (ms)', 'Sum of correct response latencies (ms)', 'Sum of incorrect response latencies (ms)', 'Sum of collection latencies (ms)']
                ex_vals  += [ tot_omissionlatencyavg,                     tot_correctlatencyavg,                   tot_incorrectlatencyavg,                     tot_collectionavg                 , '']
                ex_names += ['Average omission response latencies (ms)', 'Average correct response latency (ms)', 'Average incorrect response latencies (ms)', 'Average collection latencies (ms)', '']
                ex_vals  += [ prop_positive_PI,                 prop_incorrect_PI,                 total_PI      ]
                ex_names += ['Proportion positive of P+I (%)', 'Proportion incorrect of P+I (%)', 'P+I Total (%)']
                ex_vals  += [ prop_omitted_PIO,                  prop_positive_PIO,                  prop_incorrect_PIO,                   total_PIO,        '']
                ex_names += ['Proportion omitted of P+I+O (%)', 'Proportion positive of P+I+O (%)', 'Proportion incorrect of P+I+O (%)',  'P+I+O total (%)', '']
                ex_vals  += [ len_session,               '']
                ex_names += ['Length of session (mins)', '']
                
                list_cols[-1] = ex_vals + list_cols[-1]
                list_cols_val1[-1] = len(ex_vals)*[''] + list_cols_val1[-1]
                list_cols_val2[-1] = len(ex_vals)*[''] + list_cols_val2[-1]
                list_cols_time[-1] = len(ex_vals)*[''] + list_cols_time[-1]
                list_dfs[-1][str(time_name)+str(i)] = list_cols[-1].copy()
                list_dfs[-1]['Col '+str(i*3+1)] = list_cols_val1[-1].copy()
                list_dfs[-1]['Col '+str(i*3+2)] = list_cols_val2[-1].copy()
                list_dfs[-1][str(i)] = list_cols_time[-1].copy()
                list_dfs[-1][''] = ex_names + best_counter*['']
                
                # Add the total columns.
                if i==len(df['SystemMsg'])-1 or ((df['IdLabel'].iloc[i+1] not in list_labels) and (df['SystemMsg'].iloc[i+1] == 'start exp')):
                    
                    total_values   = []
                    total_headers  = []
                    total_values  += [ g_tot_startexp,    g_tot_omission,   g_tot_positive,   g_tot_incorrect,   g_tot_endexp,    g_tot_trials,          '']
                    total_headers += ['Start exp total', 'Omission total', 'Positive total', 'Incorrect total', 'End exp total', 'Total trials (P+I+O)', '']
                    total_values  += [ g_tot_omissionlatency,                             g_tot_correctlatency,                             g_tot_incorrectlatency,                             g_tot_collection                         ]
                    total_headers += ['Overall sum of omission response latencies (ms)', 'Overall sum of correct response latencies (ms)', 'Overall sum of incorrect response latencies (ms)', 'Overall sum of collection latencies (ms)']
                    total_values  += [ g_tot_omissionlatencyavg,                           g_tot_correctlatencyavg,                         g_tot_incorrectlatencyavg,                           g_tot_collectionavg,                        '']
                    total_headers += ['Overall average omission response latencies (ms)', 'Overall average correct response latency (ms)', 'Overall average incorrect response latencies (ms)', 'Overall average collection latencies (ms)', '']
                    total_values  += [ g_prop_positive_PI,                       g_prop_incorrect_PI,                       g_total_PI            ]
                    total_headers += ['Overall proportion positive of P+I (%)', 'Overall proportion incorrect of P+I (%)', 'Overall P+I Total (%)']
                    total_values  += [ g_prop_omitted_PIO,                        g_prop_positive_PIO,                        g_prop_incorrect_PIO,                        g_total_PIO,              '']
                    total_headers += ['Overall proportion omitted of P+I+O (%)', 'Overall proportion positive of P+I+O (%)', 'Overall proportion incorrect of P+I+O (%)', 'Overall P+I+O total (%)', '']
                    total_values  += [ g_tot_startexp,  '']
                    total_headers += ['Total sessions', '']
                    
                    # list_dfs[-1][str(i+1)] = total_headers + (len(ex_vals)-len(total_headers))*[''] + best_counter*['']
                    # list_dfs[-1][str(i+2)] = total_values + (len(ex_vals)-len(total_headers))*[''] + best_counter*['']
                    list_dfs[-1][str(i+1)] = total_headers + (len(list_dfs[-1])-len(total_headers))*['']
                    list_dfs[-1][str(i+2)] = total_values  + (len(list_dfs[-1])-len(total_values ))*['']
                    
        # Color code the entries that came from column 'SystemMsg'.
        # This uses the rules in the functions at the top of the code.
        
        df_export = df.style.applymap(text_color, subset = ['SystemMsg','MsgValue2']).applymap(cell_color, subset = ['SystemMsg','MsgValue2'])
        
        list_dfs_export = list_dfs.copy()
        for i in range(len(list_dfs)):
            list_dfs_export[i] = list_dfs[i].style.applymap(text_color).applymap(cell_color)
            #list_dfs_export[i] = list_dfs[i].style.applymap(text_color).applymap(cell_color).applymap(bold_titles,subset=[''])
            
        # Change the existing data.
        
        if add_data_to_new_file == True:
        
            with pd.ExcelWriter(export_destination) as writer:
                df_export.to_excel(writer, sheet_name='Overall sheet', engine='openpyxl', index=False)
                for i in range(len(list_dfs_export)):
                    list_dfs_export[i].to_excel(writer, sheet_name=str(list_titles[i]), engine='openpyxl', index=False, header=False)
                  
        elif add_data_to_original_file == True:
            
            with pd.ExcelWriter(import_destination, mode='a', engine='openpyxl') as writer:
                df_export.to_excel(writer, sheet_name='Overall sheet', engine='openpyxl', index=False)
                for i in range(len(list_dfs_export)):
                    list_dfs_export[i].to_excel(writer, sheet_name=str(list_titles[i]), engine='openpyxl', index=False, header=False)
            os.rename(import_destination, import_location + 'Organised ' + filename)

# Uncomment this section below to run the code manually.
# import_location = 'C:/Users/hazza/Desktop/Phenosys data/Import folder/'
# export_location = 'C:/Users/hazza/Desktop/Phenosys data/Export folder/'
# add_data_to_new_file = True
# add_data_to_original_file = False
# f2VDLR(import_location, export_location, add_data_to_new_file, add_data_to_original_file)