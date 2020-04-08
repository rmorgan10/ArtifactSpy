# Main decision maker for program

import argparse
import datetime
import glob
import numpy as np
import os
import pandas as pd
import sys

import viewer


class Data():
    def __init__(self, hep_username, minimum_images=50):

        self.minimum_images = minimum_images
        self.hep_username = hep_username
        
        # Get existing data objids
        self.finished_objid_list = []
        self.remaining_objid_list = self.get_remaining_objids()

        return

    def get_remaining_objids(self):
        all_objids = [x.split('srch')[1].split('.')[0] for x in glob.glob('../Data/Images/srch*.gif')]
        remaining_objids = list(set(all_objids) - set(self.finished_objid_list))
        return remaining_objids

    def need_more_data(self):
        return len(self.remaining_objid_list) < self.minimum_images

        
    def remove_finished_data(self):
        # Delete completed data to save disk space
        for objid in self.finished_objid_list:
            os.system('rm ../Data/Images/*{}.gif'.format(objid))

        return

    def download_from_hep(self):
        # Note that this requires a Kerberos ticket
        print("Downloading images, please wait")
        
        # Download data
        os.system('scp {}@login04.hep.wisc.edu:/afs/hep.wisc.edu/home/ramorgan2/DES_DATA/ImageBank/Batches/CURRENT--*.gz ../Data/Images/ >> ArtifactSpy.log'.format(self.hep_username))

        # Trigger organize_queue.py to queue up the next batch
        os.system("ssh {}@login04.hep.wisc.edu '/afs/hep.wisc.edu/home/ramorgan2/DES_DATA/organize_queue.py' >> ArtifactSpy.log".format(self.hep_username))

        # Unpack tarball on local machine
        os.chdir('../Data/Images/')
        os.system('tar -xzf *.gz')
        batch_name = glob.glob('*.gz')[0].split('CURRENT--')[-1].split('.')[0]
        os.system('rm *.gz')
        os.system('mv {}/*.gif .'.format(batch_name))
        os.system('rmdir ' + batch_name)
        os.chdir('../../Code')

        # Get and return metadata_stamp
        metadata_stamp = batch_name.split('--')[-1]

        # Update the log file
        stream = open('metadata_stamps.log', 'r')
        metadata_stamps = [x.strip() for x in stream.readlines()]
        stream.close()
        if len(metadata_stamps) >= 3:
            outdated_metadata_stamp = metadata_stamps.pop() #garbage
        metadata_stamps = [metadata_stamp] + metadata_stamps
        stream = open('metadata_stamps.log', 'w+')
        stream.writelines([x + '\n' for x in metadata_stamps])
        stream.close()
        
        return metadata_stamp
        

class Tracker():
    """
    Track user interaction with data
    """
    def __init__(self, data, hep_username):
        self.data = data
        self.hep_username = hep_username
        self.user_actions = []
        return

    def show_image_to_user(self, objid):

        gui = viewer.Interface(objid)

        # Handle user closing the viewer
        if gui.user_action is None:
            return "stop"

        current_time = '{:%m/%d/%y %H:%M:%S}'.format(datetime.datetime.now())

        # If user selected "Back", pass the response to go back an image
        if gui.user_action == "Back":
            return "back"
        
        # If user made a choice, track response
        if gui.user_comment is None:
            self.user_actions.append((objid, gui.user_action, "", current_time))

        else:
            self.user_actions.append((objid, gui.user_action, gui.user_comment, current_time))

        return "continue"

    def write_results(self, metadata_stamps):
        #if there are multiple entries for an objid, use the most recent one
        ### start at the end of the list, iterate backwards, and drop repeated objids
        reversed_actions = list(reversed(self.user_actions))
        found_objids = []
        keep_actions = []
        for res in reversed_actions:
            if res[0] not in found_objids:
                keep_actions = [list(res)] + list(keep_actions)
                found_objids.append(res[0])

                
        # Now make a df to output
        joined_metadata_stamps = ','.join(metadata_stamps)
        output_cols = ['OBJID', 'ACTION', 'COMMENT', 'TIME']
        df = pd.DataFrame(data=keep_actions, columns=output_cols)
        df['METADATA_STAMP'] = joined_metadata_stamps
        outfile_name = '../Results/' + self.hep_username + '--{:%m-%d-%y_%H-%M-%S}.csv'.format(datetime.datetime.now())
        
        df.to_csv(outfile_name)

        return outfile_name


    
class Session():
    def __init__(self, hep_username):

        self.date = datetime.datetime.now()
        self.hep_username = hep_username
        self.data = Data(hep_username)
        self.tracker = Tracker(self.data, self.hep_username)

        self.initialize_metadata_stamps()
        
        return

    def initialize_metadata_stamps(self):
        #deal with how to initialize this list in the case of overlap between sessions
        if not os.path.exists('metadata_stamps.log'):
            os.system('touch metadata_stamps.log')
            self.metadata_stamps = []

        else:
            #Read the log file
            stream = open('metadata_stamps.log', 'r')
            self.metadata_stamps = [x.strip() for x in stream.readlines()]
            stream.close()
        return
    
    def run(self):

        # Start off by checking if data is needed
        if self.data.need_more_data():
            # Download data                                                                                                                                                              
            metadata_stamp = self.data.download_from_hep()
            self.metadata_stamps.append(metadata_stamp)
            
            # Update list of objids to include new data                                                                                                                                  
            self.data.remaining_objid_list = self.data.get_remaining_objids()


        #Loop will exit once user closes gui
        incrementer = 0
        while True:
            incrementer += 1
            current_objid = self.data.remaining_objid_list.pop()

            user_response = self.tracker.show_image_to_user(current_objid)
            
            if user_response == "stop":
                break

            if user_response == "back":
                # put the current objid back in the list
                self.data.remaining_objid_list.append(current_objid)

                # if no previous objid exists, keep showing the current objid
                if len(self.data.finished_objid_list) == 0:
                    print("No previous objids found")
                    #This will go back to the start of the loop, but the current objid will be next up anyways
                    continue
                else:
                    #put the most recent prev objid back in the heap and go back to the top of the loop
                    most_recent_prev_objid = self.data.finished_objid_list.pop()
                    self.data.remaining_objid_list.append(most_recent_prev_objid)
                    continue

            self.data.finished_objid_list.append(current_objid)
            
            # Every 10 images, do check if more data is needed
            if incrementer % 10 == 0:

                if self.data.need_more_data():
                    # Download data
                    metadata_stamp = self.data.download_from_hep()
                    self.metadata_stamps.append(metadata_stamp)

                    # Update list of objids to include new data
                    data.remaining_objid_list = self.data.get_remaining_objids()
                
            
        # Clean up images
        self.data.remove_finished_data()

        # Write results
        outfile = self.tracker.write_results(self.metadata_stamps)
        
        # Send results to hep nodes
        self.publish_results(outfile)

        return
        
    def publish_results(self, filename):
        print("Publishing results ...")
        os.system('scp {0} {1}@login04.hep.wisc.edu:/afs/hep.wisc.edu/home/ramorgan2/DES_DATA/Results/UserResults'.format(filename, self.hep_username))

        os.system("ssh {}@login04.hep.wisc.edu '/afs/hep.wisc.edu/home/ramorgan2/DES_DATA/organize_receive.py'".format(self.hep_username))

        return
        

def start(hep_username):

    session = Session(hep_username)
    session.run()



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="HEP Login Nodes Username", type=str)
    args = parser.parse_args()

    start(args.username)