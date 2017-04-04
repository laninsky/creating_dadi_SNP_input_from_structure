import numpy
import scipy
import matplotlib
import dadi

with open('file_name', 'r') as myfile:
    dadi_input=myfile.read().replace('\n', '')

dd = dadi.Misc.make_data_dict(dadi_input)

with open(dadi_input, 'r') as myfile:
    headerline=myfile.readline().replace('\n', '').split('\t')

headerline.remove('ingroup')
headerline.remove('outgroup')
headerline.remove('Allele1')
headerline.remove('Allele2')

no_of_pops = (len(headerline)-2)/2
pop_name = headerline[0:no_of_pops]

with open('maxcount.txt', 'r') as f:
    first_line = f.readline()
    first_line=first_line.replace('\n', '').split(' ')

first_line = [int(i) for i in first_line]
fs = dadi.Spectrum.from_data_dict(dd , pop_ids =pop_name ,projections =first_line ,polarized = False)
final_fs=fs.S()

final_spectrum = fs[:]
max_pop_projections = first_line[:]
min_pop_projections = first_line[:]
min_pop_projections = [i/2 for i in min_pop_projections]

new_fs=fs.S()

for i in range(0,no_of_pops):
    temp_first_line = first_line[:]
    temp_first_line[i] = temp_first_line[i]-1
    temp_fs = dadi.Spectrum.from_data_dict(dd , pop_ids =pop_name ,projections =temp_first_line ,polarized = False)        
    while temp_fs.S() > new_fs:
        max_pop_projections[i] = temp_first_line[i]
        new_fs=temp.S()
        temp_first_line[i] = temp_first_line[i]-1
        temp_fs = dadi.Spectrum.from_data_dict(dd , pop_ids =pop_name ,projections =temp_first_line ,polarized = False)        
        temp_fs_S = temp_fs.S()
                
#Do another run increasing the allele sample sizes starting from n=1 for all samples to see if we converge on the same outcome
first_line = [1 for i in first_line]
lil_fs = dadi.Spectrum.from_data_dict(dd , pop_ids =pop_name ,projections =first_line ,polarized = False)
for i in range(0,no_of_pops):
    new_fs=lil_fs.S()
    temp_first_line = first_line[:]
    if (temp_first_line[i]+10) <= max_pop_projections[i]:
        temp_first_line[i] = temp_first_line[i]+10            
    elif (temp_first_line[i]+5) <= max_pop_projections[i]:
        temp_first_line[i] = temp_first_line[i]+5
    elif (temp_first_line[i]+2) <= max_pop_projections[i]:
        temp_first_line[i] = temp_first_line[i]+2
    elif (temp_first_line[i]+1) <= max_pop_projections[i]:
        temp_first_line[i] = temp_first_line[i]+1
    else:
        continue
    temp_fs = dadi.Spectrum.from_data_dict(dd , pop_ids =pop_name ,projections =temp_first_line ,polarized = False)        
    while temp_fs.S() > new_fs: 
        min_pop_projections[i] = temp_first_line[i]
        new_fs=temp_fs.S()
        if (temp_first_line[i]+10) <= max_pop_projections[i]:
            temp_first_line[i] = temp_first_line[i]+10            
        elif (temp_first_line[i]+5) <= max_pop_projections[i]:
            temp_first_line[i] = temp_first_line[i]+5
        elif (temp_first_line[i]+2) <= max_pop_projections[i]:
            temp_first_line[i] = temp_first_line[i]+2
        elif (temp_first_line[i]+1) <= max_pop_projections[i]:
            temp_first_line[i] = temp_first_line[i]+1
        else:
            continue
        temp_fs = dadi.Spectrum.from_data_dict(dd , pop_ids =pop_name ,projections =temp_first_line ,polarized = False)        
        temp_fs_S = temp_fs.S()    

#If either approach (top down, bottom up) suggests down-projecting, checking for any further tweaks, otherwise writing out
if max_pop_projections == min_pop_projections:
      final_spectrum = dadi.Spectrum.from_data_dict(dd , pop_ids =pop_name ,projections =max_pop_projections ,polarized = False)
      final_spectrum.to_file("spectrum_output.txt")
      final_fs = final_spectrum.S()
      print 'The optimum fs.S. is'
      print final_fs
      print 'The projection for this optimum is'
      print pop_name
      print max_pop_projections
      print 'The spectrum for this is saved as "spectrum_output.txt"'
else:
    

