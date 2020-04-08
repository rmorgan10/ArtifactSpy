# Label unsure images

import argparse
import os
import pandas as pd
import sys

import viewer

parser = argparse.ArgumentParser()
parser.add_argument("--tarball", help="Name of tarball to download from UNSURE directory", type=str, default='')
args = parser.parse_args()

# Check for the tarball argument
if args.tarball == '':
    print("Use the --tarball argument to point to the tarball on the HEP cluster")
    sys.exit()

# Print warning
print("Don't forget, you were too lazy to make the back button work for this script, so do not use it\n")
    
# Get the images
os.system('scp ramorgan2@login04.hep.wisc.edu:/afs/hep.wisc.edu/home/ramorgan2/DES_DATA/ImageBank/Unsure/{} .'.format(args.tarball))
os.system('tar -xzf ' + args.tarball)
dir_name = args.tarball.split('.')[0]
objids = [x.split('srch')[-1].split('.')[0] for x in glob.glob(dir_name + '/srch*.gif')]

# Move these images to the Data directory
os.system('mv {}/*.gif ../Data/Images/'.format(dir_name))
os.system('rm -r ' + dir_name)

# Display images and track responses
my_labels = []
for counter, objid in enumerate(objids):
    print(counter + 1, '/', len(objids), '  ')
    
    gui = viewer.Interface(objid)

    if gui.user_action == 'Back':
        print("What are you doing? I literally told you not to do that.")
        print("Lucky for you, I expected you to be a fool.")
        print("Do it right this time, please.")
        choice = gui.user_action
        while choice == "Back":
            gui = viewer.Interface(objid)
            choice = gui.user_action
        print("There, thanks for getting it right, doofus.")

    if gui.user_comment is not None:
        my_labels.append([objid, gui.user_action, gui.user_comment])
    else:
        my_labels.append([objid, gui.user_action, ""])

# Save results to a csv and send to hep cluster
outdf = pd.DataFrame(data=my_labels, columns=['OBJID', 'ACTION', 'COMMENT'])
outdf.to_csv(dir_name + '.csv', index=False)

os.system('scp {}.csv ramorgan2@login04.hep.wisc.edu:/afs/hep.wisc.edu/home/ramorgan2/DES_DATA/Results/UnsureResults/'.format(dir_name))

# Clean up this directory
os.system('rm ' + args.tarball)
for objid in objids:
    os.system("rm ../Data/Images/*{}.gif".format(objid))
os.system('mv {}.csv ../../backup'.format(dir_name))

print("All done!")
