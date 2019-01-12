import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
from matplotlib import cm
import numpy as np
from scipy.fftpack import rfft
from scipy.io import wavfile as wav
from scipy import signal
from scipy.signal import butter, lfilter
import json


first_deriv_peak_prominence = 10

#1st iteration constants
cell_duration_1st_iter = 2
elements_to_desegment_1st_iter = 1
shaper_1st_iter = 0.2
percent_match_const_coef_1st_iter = 0.1
round_const_1st_iter = 1
fft_divide_const_1st_iter = 5
prominence_const_1st_iter = 57
edge_margin_1st_iter = 1.2

#2nd iteration constants
cell_duration_2nd_iter = 1
elements_to_desegment_2nd_iter = 3
shaper_2nd_iter = 0.0
percent_match_const_coef_2nd_iter = 1.2
round_const_2nd_iter = 1
fft_divide_const_2nd_iter = 2
prominence_const_2nd_iter = 0.3
edge_margin_2nd_iter = 1.2

#3rd iteration constants
cell_duration_3rd_iter = 0.1
elements_to_desegment_3rd_iter = 3
shaper_3rd_iter = 0.0
percent_match_const_coef_3rd_iter = 1
round_const_3rd_iter = 1
fft_divide_const_3rd_iter = 1
prominence_const_3rd_iter = 0.3


rate1_orig = 0
data1_orig = 0
data1 = 0
rate1 = 0

rate2_orig = 0
data2_orig = 0
data2 = 0
rate2 = 0

duration1_total = 0
duration2_total = 0


order = 6
cutoff = 5000  # desired cutoff frequency of the filter, Hz

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def ArrangeSongsSegments(matched_indexes, matched_x, matched_y, duration, cell_duration, elements_to_desegment, edges_of_song1, edges_of_song2):
    np_matched_indexes = np.array(matched_indexes)
    if(len(np_matched_indexes) > 0):
        peaks_matched_indexes, _ = signal.find_peaks(np_matched_indexes[:,3],prominence=first_deriv_peak_prominence)
        print(peaks_matched_indexes)
    
        if(len(peaks_matched_indexes) > 0):
            k = 1
            for i in range(0, len(peaks_matched_indexes)+1):        
                if(i == 0):
                    start = 0
                    end = peaks_matched_indexes[i]
                elif(i == len(peaks_matched_indexes)):
                    start = peaks_matched_indexes[i-1]
                    end = int(round(duration / cell_duration - elements_to_desegment, 0)) + 1
                else:
                    start = peaks_matched_indexes[i-1]
                    end = peaks_matched_indexes[i]

                print("start = " + str(start))
                print("end = " + str(end))

                if(end - start > 0):
                    avg_offset = sum(np.array(np_matched_indexes[:,2])[start:end]) / (end - start)
                    print("avg_offset = " + str(avg_offset))

                    minI = int(min(np.array(np_matched_indexes[:,0])[start:end]))
                    print("Before minI = " + str(minI))
                    maxI = int(max(np.array(np_matched_indexes[:,0])[start:end]))
                    print("Before maxI = " + str(maxI))
                    minJ = int(min(np.array(np_matched_indexes[:,1])[start:end]))
                    print("Before minJ = " + str(minJ))
                    maxJ = int(max(np.array(np_matched_indexes[:,1])[start:end]))
                    print("Before maxJ = " + str(maxJ))

                    startJ = minI - int(round(avg_offset, 0))
                    endJ = maxI - int(round(avg_offset, 0)) # 6 + (-11) = -5

                    if(minJ < startJ):
                        minJ = startJ
                        print("After minJ = " + str(minJ))
                    if(maxJ > endJ): # 20 > -5
                        maxJ = endJ
                        print("After maxJ = " + str(maxJ))


                    #avg_offset = 0
                    #minI = np_matched_indexes[start][0]
                    #maxI = np_matched_indexes[start][0]
                    #minJ = np_matched_indexes[start][1]
                    #maxJ = np_matched_indexes[start][1]

                    #for j in range(start, end):
                    #    avg_offset += np_matched_indexes[j][2]

                    #    if(np_matched_indexes[j][0] < minI):
                    #        minI = np_matched_indexes[j][0]
                    #    if(np_matched_indexes[j][0] > maxI):
                    #        maxI = np_matched_indexes[j][0]
                    #    if(np_matched_indexes[j][1] < minJ):
                    #        minJ = np_matched_indexes[j][1]
                    #    if(np_matched_indexes[j][1] > maxJ):
                    #        maxJ = np_matched_indexes[j][1]

                    #avg_offset = avg_offset / (end - start)

                    #isOnBorder_I = False
                    #isOnBorder_J = False
                    #if(minI == 0):
                    #    minJ = avg_offset
                    #    isOnBorder_I = True
                    #if(minJ == 0):
                    #    minI = -avg_offset
                    #    isOnBorder_J = True
                    #if((maxI + elements_to_desegment) * cell_duration  >= duration):
                    #    maxJ = duration + avg_offset
                    #    isOnBorder_I = True
                    #if((maxJ + elements_to_desegment) * cell_duration  >= duration):
                    #    maxI = duration - avg_offset
                    #    isOnBorder_J = True

                    #if(not(isOnBorder_I)):
                    #    error_rate_I = maxI - minI - abs(avg_offset)
                    #    print("error_rate_I = " + str(error_rate_I))
                    #    if(error_rate_I > 0):
                    #        maxI = int(maxI - error_rate_I / 2)
                    #        minI = int(minI + error_rate_I / 2)
                    #    elif(error_rate_I < 0):
                    #        maxI = int(maxI + error_rate_I / 2)
                    #        minI = int(minI - error_rate_I / 2)  

                    #if(not(isOnBorder_J)):
                    #    error_rate_J = maxJ - minJ - abs(avg_offset)
                    #    print("error_rate_J = " + str(error_rate_J))
                    #    if(error_rate_J > 0):
                    #        maxJ = int(maxJ - error_rate_J / 2)
                    #        minJ = int(minJ + error_rate_J / 2)
                    #    elif(error_rate_I < 0):
                    #        maxJ = int(maxJ + error_rate_J / 2)
                    #        minJ = int(minJ - error_rate_J / 2)

                    #print("minI = " + str(minI))
                    #print("maxI = " + str(maxI))

                    print("minI = " + str(minI))
                    print("maxI = " + str(maxI))
                    for j in range(minI, maxI):
                        matched_x[j] = k

                    #print("minJ = " + str(minJ))
                    #print("maxJ = " + str(maxJ))

                    for j in range(minJ, maxJ):
                        matched_y[j] = k   

                    print("k = " + str(k))
                    print("matched_x = ")
                    print(matched_x)
                    print("matched_y = ")
                    print(matched_y)
                    #matched_x[minI:maxI] = k
                    #matched_y[minJ:maxJ] = k

                    edges_of_song1.append([k, minI*cell_duration, maxI*cell_duration])
                    edges_of_song2.append([k, minJ*cell_duration, maxJ*cell_duration])

                    k+=1    
        else:
            print("In else")
            k = 1
            np_differences = np.array([0] * len(np_matched_indexes))
            for a in range(1, len(np_matched_indexes)):
                np_differences[a] = abs(np_matched_indexes[a][0] - np_matched_indexes[a-1][0])
            np_differences_peaks, _1 = signal.find_peaks(np_differences,prominence=2)
            print("np_differences_peaks = ")
            print(np_differences_peaks)


            for i in range(0, len(np_differences_peaks)+1):  
                if(len(np_differences_peaks) == 0): #When there is a different segment in the start
                    start = 0
                    end = int(round(duration / cell_duration - elements_to_desegment, 0)) + 1
                elif(i == 0): # When there is a "hole"
                    start = 0
                    end = np_differences_peaks[i]
                elif(i == len(np_differences_peaks)):
                    start = np_differences_peaks[i-1]
                    end = int(round(duration / cell_duration - elements_to_desegment, 0)) + 1
                else:
                    start = np_differences_peaks[i-1]
                    end = np_differences_peaks[i]

                minI = int(min(np.array(np_matched_indexes[:,0])[start:end]))
                maxI = int(max(np.array(np_matched_indexes[:,0])[start:end]))
                minJ = int(min(np.array(np_matched_indexes[:,1])[start:end]))
                maxJ = int(max(np.array(np_matched_indexes[:,1])[start:end]))

                for j in range(minI, maxI):
                    matched_x[j] = k

                for j in range(minJ, maxJ):
                    matched_y[j] = k     

                edges_of_song1.append([k, minI*cell_duration, maxI*cell_duration])
                edges_of_song2.append([k, minJ*cell_duration, maxJ*cell_duration])

                k+=1


            #for a in range(0, len(matched_indexes)):
            #    i = matched_indexes[a][0]
            #    j = matched_indexes[a][1]

            #    if(a in np_differences_peaks):
            #        k+=1

            #    matched_x[i] = k
            #    matched_y[j] = k
        

def Filter_edges(matched_x, matched_y, cell_duration, start):
    edges = []
    for i in range(0, len(matched_x) - 1):
        if(matched_x[i] != matched_x[i+1] or matched_y[i] != matched_y[i+1]):
            edges.append((i+1) * cell_duration + start)
    
    return edges


def Round_fft(fft_out_list_norm, round_const):
    for i in range (0, len(fft_out_list_norm)):
        fft_out_list_norm[i] = abs(round(fft_out_list_norm[i], round_const))


def Normalize_fft(fft_out_list):
    max_element = max(fft_out_list)
    fft_out_list_norm = []

    for ele in fft_out_list:
        fft_out_list_norm.append(ele/max_element)
    
    return fft_out_list_norm


def List_data(fft_out):
    fft_out_list = []
    for i in range(0, len(fft_out)):
        old_imag = fft_out[i].imag
        #fft_out1[i] = 0.0 + old_imag*1j
        fft_out_list.append(old_imag)
    
    return fft_out_list


def Normalize_data(data_trimmed):
    data_norm = []
    max_element = max(data_trimmed)
    data_norm = []
    for ele in data_trimmed:
        data_norm.append(ele/max_element)
    
    return data_norm


def Desegment(fft_data_list ,start_index , elements_to_desegment):
    fft_data_list_modified = [0] * len(fft_data_list[0])
    for a in range(start_index, elements_to_desegment + start_index):
        #fft_data_list_modified = [fft_data_list_modified[i] + fft_data_list[a][i] for i in range(len(fft_data_list[a]))]
        for i in range(0, len(fft_data_list[a])):
            fft_data_list_modified[i] += fft_data_list[a][i]           
    return fft_data_list_modified


def CalculateMatchPercent_old(elem1, elem2, shaper):
    sum = 0
    count = 0
    for i in range(0, len(elem1)):
        #if(elem1[i] != 0.0 and elem2[i] != 0.0):
        if(elem1[i] > shaper and elem2[i] > shaper):
            sum += (min(elem1[i], elem2[i]) / max(elem1[i],elem2[i]))
            #sum += elem1[i] / elem2[i]            
        #if(elem1[i] != 0.0 or elem2[i] != 0.0):
        if(elem1[i] > shaper or elem2[i] > shaper):
            count += 1
        #elif(elem1[i] == 0.0 and elem2[i] == 0.0):
        #    sum+=1
    #percent = sum / len(elem1) * 100
    if count == 0:
        percent = 0.0
    else:
        percent = sum / count * 100
    return percent

    
def CalculateMatchPercent(elem1, elem2, shaper):
    return np.corrcoef(elem1, elem2)[0][1]*100


def Trim(data, rate, start, end):
    data_trimmed = []
    start_in_frames = int(round(start*rate, 0))
    end_in_frames = int(round(end*rate, 0))
    
    for i in range(start_in_frames, end_in_frames):
        data_trimmed.append(data[i])
        
    return data_trimmed


def Analyze_sound(start, end, cell_duration, elements_to_desegment, shaper, percent_match_const_coef, round_const, fft_divide_const, prominence_const, edges_of_song1, edges_of_song2):   
    duration1 = end - start
    duration2 = end - start
    
    i = start
    starts1 = []
    while(i < duration1 + start):
        starts1.append(i)
        i = round(i + cell_duration,1)

    i = start
    starts2 = []
    while(i < duration2 + start):
        starts2.append(i)
        i = round(i + cell_duration,1)
        
    
    fft_data1_list = []
    fft_data2_list = []
    for start1 in starts1:
        if(start1 + cell_duration > duration1 + start):
            end1 = duration1 + start
        else:   
            end1 = round(start1 + cell_duration, 1)  

        #trimming
        data1_trimmed = Trim(data1, rate1, start1, end1)

        #normalizing data
        data1_norm = Normalize_data(data1_trimmed)

        #fourier transform
        fft_out1 = rfft(data1_norm, int(cell_duration*rate1/fft_divide_const))

        #listing
        #fft_out1_list = List_data(fft_out1)

        #normalizing fft
        #fft_out1_list_norm = Normalize_fft(fft_out1_list)
        fft_out1_list_norm = Normalize_fft(fft_out1)

        #rounding fft
        Round_fft(fft_out1_list_norm, round_const)

        fft_data1_list.append(fft_out1_list_norm)
    print(len(fft_data1_list[0]))




    for start2 in starts2:
        if(start2 + cell_duration > duration2 + start):
            end2 = duration2 + start
        else:   
            end2 = round(start2 + cell_duration, 1)

        #print("Start2 = " + str(start2))    
        #print("End2 = " + str(end2))

        #trimming
        data2_trimmed = Trim(data2, rate2, start2, end2)

        #normalizing data
        data2_norm = Normalize_data(data2_trimmed)

        #fourier transform
        fft_out2 = rfft(data2_norm, int(cell_duration*rate2/fft_divide_const))

        #listing
        #fft_out2_list = List_data(fft_out2)

        #normalizing fft
        #fft_out2_list_norm = Normalize_fft(fft_out2_list)
        fft_out2_list_norm = Normalize_fft(fft_out2)

        #rounding fft
        Round_fft(fft_out2_list_norm, round_const)

        fft_data2_list.append(fft_out2_list_norm)


    
    results = []
    percents = []
    matched_indexes = []

    i = 0
    j = 0
    print(len(fft_data1_list))
    print(len(fft_data1_list[0]))
    print(len(fft_data2_list))

    while i < (len(fft_data1_list) - elements_to_desegment):
        elem1 = Desegment(fft_data1_list ,i , elements_to_desegment)
        while j < (len(fft_data2_list) - elements_to_desegment):
            elem2 = Desegment(fft_data2_list ,j , elements_to_desegment)

            if(len(elem1) != len(elem2)):
                ans = False
            else:
                ans = np.logical_and(
                    np.logical_and(elem1 is not None, elem2 is not None),
                    elem1 == elem2)
            results.append(ans)
            j+=1

            if(len(elem1) == len(elem2)):
                percent = CalculateMatchPercent(elem1, elem2, shaper)
                percents.append([percent,i,j-1])
            else:
                percents.append([0, i, j-1])
                
            if ans:
                break
        if(j == len(fft_data2_list) - elements_to_desegment):
            j = 0
        i+=1


    np_percents = np.array(percents)
    np_percents_values = np_percents[:,0]
    
        
    avg_percent = np.mean(np_percents_values)
    match_percent = avg_percent * percent_match_const_coef

    
    peaks, _ = signal.find_peaks(np_percents_values,prominence=prominence_const, height = match_percent, distance = 6)
    percents_values_filtered = []
    for peak in peaks:
        percents_values_filtered.append(np_percents_values[peak])

    
    matched_indexes=[]

    for i in range(len(percents)):
        if(percents[i][0] == 100.00 or i in peaks):
            matched_indexes.append([percents[i][1], percents[i][2], (percents[i][1] - percents[i][2]),0,percents[i][0]])
    
    #-----------------------------------------------------
    for i in range(1, len(matched_indexes)):
        matched_indexes[i] = [matched_indexes[i][0], matched_indexes[i][1], matched_indexes[i][2], abs(matched_indexes[i][2] - matched_indexes[i-1][2]), matched_indexes[i][4]]
    if(len(matched_indexes) > 0):
        matched_indexes[0] = [matched_indexes[0][0], matched_indexes[0][1], matched_indexes[0][2], 0, matched_indexes[0][4]]
    
        np_matched_indexes_first_deriv = np.array(matched_indexes)[:,3]
    
        peaks_matched_indexes, _1 = signal.find_peaks(np_matched_indexes_first_deriv,prominence=first_deriv_peak_prominence)
    


    #-----------------------------------------------------
    matched_x = [0] * (len(fft_data1_list) - elements_to_desegment)
    matched_y = [0] * (len(fft_data2_list) - elements_to_desegment)
    ArrangeSongsSegments(matched_indexes, matched_x, matched_y, duration1, cell_duration, elements_to_desegment, edges_of_song1, edges_of_song2)        
    



    edges = Filter_edges(matched_x, matched_y, cell_duration, start)
    
    return edges


def Make_Audio_Analysis(song1_data, song2_data, user_name, project_name):
    global rate1_orig
    global data1_orig
    global data1
    global rate1

    global rate2_orig
    global data2_orig
    global data2
    global rate2

    global duration1_total
    global duration2_total

    project_folder = 'user_projects/'+user_name+'/'+project_name+'/'
    file_path1 = project_folder + song1_data
    file_path2 = project_folder + song2_data

    rate1_orig, data1_orig = wav.read(file_path1)
    if(len(data1_orig.shape) > 1):
        data1_orig = data1_orig[:, 0]
    data1 = butter_lowpass_filter(data1_orig, cutoff, rate1_orig, order)
    data1 = data1[::4]
    #data1 = signal.resample(data1, int(len(data1_orig)/4))
    rate1 = rate1_orig/4
    #rate1 = rate1_orig


    rate2_orig, data2_orig = wav.read(file_path2)
    if(len(data2_orig.shape) > 1):
        data2_orig = data2_orig[:, 0]
    data2 = butter_lowpass_filter(data2_orig, cutoff, rate2_orig, order)  
    data2 = data2[::4]
    #data2 = signal.resample(data2, int(len(data2_orig)/4))
    rate2 = rate2_orig/4
    #rate2 = rate2_orig

    duration1_total = len(data1)/rate1
    duration2_total = len(data2)/rate2

    start_1st_iter = 0
    end_1st_iter = duration1_total

    edges_of_song1 = []
    edges_of_song2 = []

    edges_1st_iter = Analyze_sound(start_1st_iter, end_1st_iter, cell_duration_1st_iter ,elements_to_desegment_1st_iter ,shaper_1st_iter ,percent_match_const_coef_1st_iter ,round_const_1st_iter ,fft_divide_const_1st_iter, prominence_const_1st_iter, edges_of_song1, edges_of_song2)

    data1_reduced = []
    for i in range(0, len(data1_orig), 100):
        data1_reduced.append(data1_orig[i])
    data1_normalized = Normalize_data(data1_reduced)

    tx1 = np.linspace(0, len(data1_orig)/rate1_orig, len(data1_normalized))
    #tx1 = np.linspace(0, len(data1_orig)/rate1_orig, len(data1_orig)/1)
    print("Before plt.figure()")
    
    fig1 = plt.figure()
    print("After plt.figure()")
    plt.plot(tx1, data1_normalized)
    for element in edges_of_song1:
        k=element[0]
        if(k==1):
            facecolor='#2ca02c'
        elif(k==2):
            facecolor='#e2563b'
        elif(k==3):
            facecolor='#e2c33a'
        elif(k==4):
            facecolor='#e553ed'
            
        x = [element[1], element[2], element[2], element[1]]
        y = [1, 1, -1, -1]
        plt.fill(x, y, c=facecolor, alpha=0.6)
        #plt.broken_barh([(element[1], element[2]-element[1])], (-1, 2), facecolor=facecolor, alpha=0.6)
        #plt.fill_between([element[1],element[2]], -1, 1, color=facecolor, alpha=0.5)
        #plt.axvspan(element[1], element[2], ymin=0, ymax=1, facecolor=facecolor, alpha=0.5)
    plt.close()

    data2_reduced = []
    for i in range(0, len(data2_orig), 100):
        data2_reduced.append(data2_orig[i])
    data2_normalized = Normalize_data(data2_reduced)

    tx2 = np.linspace(0, len(data2_orig)/rate2_orig, len(data2_normalized))
    #tx2 = np.linspace(0, len(data2_orig)/rate2_orig, len(data2_orig)/100+1)

    fig2 = plt.figure()
    plt.plot(tx2, data2_normalized)
    for element in edges_of_song2:
        k=element[0]
        print("k = " + str(k))
        print("start = " + str(element[1]))
        print("end = " + str(element[2]))
        if(k==1):
            facecolor='#2ca02c'
        elif(k==2):
            facecolor='#e2563b'
        elif(k==3):
            facecolor='#e2c33a'
        elif(k==4):
            facecolor='#e553ed'
        
        x = [element[1], element[2], element[2], element[1]]
        y = [1, 1, -1, -1]
        plt.fill(x, y, c=facecolor, alpha=0.6)
        #plt.broken_barh([(element[1], element[2]-element[1])], (-1, 2), facecolor=facecolor, alpha=0.6)
        #plt.fill_between([element[1],element[2]], -1, 1, color=facecolor, alpha=0.5)
        #plt.axvspan(element[1], element[2], facecolor=facecolor, alpha=0.5)
    plt.close()


    amp_diff = []
    for i in range(0, min([len(data2_orig), len(data1_orig)]),100):
        if(data1_orig[i]!=0):
            amp_diff.append(data2_orig[i]/data1_orig[i])
    volume_percent = round(sum(amp_diff)/len(amp_diff)*100, 2)

    print("Edges of song1:")
    print(edges_of_song1)
    print("Edges of song2:")
    print(edges_of_song2)

    return [json.dumps(mpld3.fig_to_dict(fig1)), json.dumps(mpld3.fig_to_dict(fig2)), volume_percent]
#https://github.com/mpld3/mpld3/issues/298
#pip install "git+https://github.com/javadba/mpld3@display_fix"

