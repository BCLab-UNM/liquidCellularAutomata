import sys
import glob
import subprocess
import multiprocessing



def run_experiment(seed, agents):
    command = "python3 lca.py --seed " + str(seed) + " --agents " + str(agents)
    command_array = command.split(" ")
    print(command)
    output = subprocess.check_output(command_array)
    print(output)

def main():
    
    #Create tasks
    tasks = []
    for i in range(0,10):
        for b in range(50,100):
            tasks.append((i,b))
    p = multiprocessing.Pool(4)

    p.starmap(run_experiment, tasks)

if __name__ == "__main__":
    main()

"""
print("CREATING TEST SPECTROGRAMS")
#Convert all .wav files to spectrogram png files
for file in filenames:
    file_no_ext = file.split("/")[-1].replace(".wav","")
    command = "python3 spectrogram.py " + file + " " + "./data/png_files_test/" + file_no_ext + ".png" 
    command_array = command.split(" ")
    print(command)
    subprocess.check_output(command_array)
    #subprocess.Popen(command_array, shell=False, stdin=None, stdout=None, stderr=None)


#TRAINING DATA
filenames = glob.glob("./data/wav_files_train/*.wav")

print("CREATING TRAIN SPECTROGRAMS")
#Convert all .wav files to spectrogram png files
for file in filenames:
    file_no_ext = file.split("/")[-1].replace(".wav","")
    command = "python3 spectrogram.py " + file + " " + "./data/png_files_train/" + file_no_ext + ".png" 
    print(command)
    subprocess.check_output(command.split(" "))

"""
