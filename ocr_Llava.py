#'tcli' file created based on https://github.com/haotian-liu/LLaVA/issues/540
#It should be place inside 'LLaVA\llava\serve' folder
#If errors, change time.sleep(35) to 40

# #Dependencies
# git clone https://github.com/haotian-liu/LLaVA.git
# cd LLaVA
# conda create -n llava python=3.10 -y
# conda activate llava
# pip install --upgrade pip  # enable PEP 660 support
# pip install -e .

#Might also need to install the following:
#pip install protobuf
#pip install --upgrade transformers

#If we use llava-v1.6-vicuna-7b, we need to reinstall some dependencies by going to the cloned repository and running the following:
#git pull
#pip install -e .

#We might need to run the following command to install the correct version of psutil:
# pip uninstall psutil
# pip install psutil

#GPT4 Prompt:
# Given a a path with images (/home/soyrl/spyscape_test/), sort them and create a list of them. 
# Run the python command (python -m llava.serve.tcli --model-path liuhaotian/llava-v1.6-vicuna-7b --load-4bit) in terminal.
# That command should be run first. After that, some messages will be printed in the terminal from each execution. 
# Show them to the user. At some point terminal will show 'Image path:' and will wait for user input. 
# Use the path of the first image in the list as input. Then the terminal will show 'USER:' and will wait for user input. 
# Use as input there 'Extract the text in the image'. After that, you should wait for 30secs. 
# Then, the terminal will show 'ASSISTANT:' with some text after it that you should show to the user.
# Wait 2 more seconds and then the 'Image Path:' will be shown again. Repeat the above process for all the images. 
# Keep in mind that the python command should only be executed once at the beginning

import subprocess
import time
import os
import select

start=time.time()

# Get list of images
image_dir = '/home/soyrl/spyscape_test/'
image_list = sorted([os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith('.jpg')])
   
# Start the python command
process = subprocess.Popen(['python', '-m', 'llava.serve.tcli', '--model-path', 'liuhaotian/llava-v1.6-vicuna-7b', '--load-4bit'], #llava-v1.6-mistral-7b
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def read_output(timeout=1):
    ready, _, _ = select.select([process.stdout], [], [], timeout)
    if ready:
        return os.read(process.stdout.fileno(), 4096).decode('utf-8') #Read the output
    return None

for ind,image in enumerate(image_list):

    #Print progress in terminal and save to txt file
    print(str(ind)+'/'+str(len(image_list)), '('+str(round(ind/len(image_list)*100,2))+'%)') #print progress in terminal
    with open("output_llava.txt", "a") as file: #Save progress to txt file
        file.write(str(ind)+'/'+str(len(image_list))+ '('+str(round(ind/len(image_list)*100,2))+'%)'+'\n')

    # Wait for 'Image path:' prompt and send image path
    while True:
        if ind==0:
            output = read_output()

        #Second condition because sometimes not full message from LLM    
        if (output and 'Image path:' in output) or (output and 'ASSISTANT' in output and ind!=0): 

            #Print the output and save to txt file
            print('Image path:', image)
            with open("output_llava.txt", "a") as file: #First time write the command we send to LlaVa to the output file
                file.write('Image path:'+ image+'\n')

            process.stdin.write((image + '\n').encode())
            process.stdin.flush()
            break

    # Wait for 'USER:' prompt and send command
    while True:
        output = read_output()

        if output and 'USER:' in output:

            #Print the output and save to txt file
            print('USER:', 'Extract the text in the image')
            with open("output_llava.txt", "a") as file: 
                file.write('USER:'+ "Extract text in the image. If there is no text just say 'no text' \n")

            process.stdin.write(("Extract text in the image. If there is no text just say 'no text' \n").encode())
            process.stdin.flush()
            break

    # Wait for 35 seconds
    time.sleep(35)

    # Print 'ASSISTANT:' output
    while True:
        output = read_output()

        if output and output.startswith('ASSISTANT:'):

            #Print the output and save to txt file
            print('ASSISTANT:', output)
            with open("output_llava.txt", "a") as file: 
                file.write('ASSISTANT:'+ output+ '\n')

            break

    # Wait for 2 seconds
    time.sleep(2)

# Close the process
process.stdin.close()
process.terminate()
process.wait(timeout=0.2)

print('Time:', time.time()-start)
with open("output_llava.txt", "a") as file:
    file.write('Time:'+ str(time.time()-start)+'\n')