# Graphical User Interface for Labeling Images

import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Button
import time

class Interface():
    """
    A GUI for labeling images
    """
    def __init__(self, objid):
        """
        Set the objid and display the stamps. User selections will set 
        the 'user_action' attribute of this object.
        """
        self.objid = objid
        self.user_action = None
        self.user_comment = None

        # Show stamps to user and save action in self.user_action
        self.display(objid)

        return

    # Interface Properties
    def display(self, objid):
        """
        Display stamps in a GUI for labeling
        
        :param objid: objid to be displayed
        """
        # Load stamps 
        path = '../Data/Images/'
        srch = plt.imread(path + 'srch' + objid + '.gif')
        temp = plt.imread(path + 'temp' + objid + '.gif')
        diff = plt.imread(path + 'diff' + objid + '.gif')

        # Instantiate figure
        fig = plt.figure(figsize=(12, 3.5))
        gs = GridSpec(3, 8, figure=fig)

        # Add images to figure
        srch_ax = fig.add_subplot(gs[0:2, 0:2])
        temp_ax = fig.add_subplot(gs[0:2, 2:4])
        diff_ax = fig.add_subplot(gs[0:2, 4:6])
        srch_ax.imshow(srch, cmap='gray')
        temp_ax.imshow(temp, cmap='gray')
        diff_ax.imshow(diff, cmap='gray')

        # Format image subplots
        srch_ax.set_xticks([], [])
        srch_ax.set_yticks([], [])
        temp_ax.set_xticks([], [])
        temp_ax.set_yticks([], [])
        diff_ax.set_xticks([], [])
        diff_ax.set_yticks([], [])
        srch_ax.set_title("Search", fontsize=14)
        temp_ax.set_title("Template", fontsize=14)
        diff_ax.set_title("Difference", fontsize=14)

        # Add buttons to figure
        good_button_ax = fig.add_subplot(gs[2, 5])
        good_button = Button(good_button_ax, 'Good', color='#ccebc5', hovercolor='#4daf4a')
        good_button.on_clicked(self.label_good)

        marginal_button_ax = fig.add_subplot(gs[2, 4])
        marginal_button = Button(marginal_button_ax, 'Marginal', color='#ccebc5', hovercolor='#4daf4a')
        marginal_button.on_clicked(self.label_marginal)

        bad_sub_button_ax = fig.add_subplot(gs[2, 0])
        bad_sub_button = Button(bad_sub_button_ax, 'Bad\nSubtraction', color='#fbb4ae', hovercolor='#e41a1c')
        bad_sub_button.on_clicked(self.label_bad_subtraction)

        psf_in_temp_button_ax = fig.add_subplot(gs[2, 1])
        psf_in_temp_button = Button(psf_in_temp_button_ax, 'Point Source\nin Template', color='#fbb4ae', hovercolor='#e41a1c')
        psf_in_temp_button.on_clicked(self.label_psf_in_temp)

        noisy_temp_button_ax = fig.add_subplot(gs[2, 2])
        noisy_temp_button = Button(noisy_temp_button_ax, 'Noisy\nTemplate', color='#fbb4ae', hovercolor='#e41a1c')
        noisy_temp_button.on_clicked(self.label_noisy_template)
        
        dark_spot_in_temp_button_ax = fig.add_subplot(gs[2, 3])
        dark_spot_in_temp_button = Button(dark_spot_in_temp_button_ax, 'Dark Spot in\nTemplate\nCenter', color='#fbb4ae', hovercolor='#e41a1c')
        dark_spot_in_temp_button.on_clicked(self.label_dark_spot_in_temp)

        unsure_button_ax = fig.add_subplot(gs[1, 6:])
        unsure_button = Button(unsure_button_ax, 'Unsure\n(Send image to Rob)')
        unsure_button.on_clicked(self.label_unsure)

        help_button_ax = fig.add_subplot(gs[0, 7])
        help_button = Button(help_button_ax, 'Help')
        help_button.on_clicked(self.label_help)

        back_button_ax = fig.add_subplot(gs[0, 6])
        back_button = Button(back_button_ax, 'Back\n<--')
        back_button.on_clicked(self.label_back)

        #skip_button_ax = fig.add_subplot(gs[1, 7])
        #skip_button = Button(skip_button_ax, 'Skip\n-->')
        #skip_button.on_clicked(self.label_skip)

        other_button_ax = fig.add_subplot(gs[2, 6:])
        other_button = Button(other_button_ax, 'Other\n(Leave comment in terminal)')
        other_button.on_clicked(self.label_other)

        # Add OBJID to figure window
        back_button_ax.set_title("Object ID: " + objid, horizontalalignment='left')
        
        # Display figure
        plt.show()
        return

    # Possible actions for user
    def label_good(self, event):
        """
        Called if user labels image as 'Good'
        """
        setattr(self, 'user_action', 'Good')
        time.sleep(0.1)
        plt.close()
        return

    def label_bad_subtraction(self, event):
        """
        Called if user labels image as 'Bad Subtraction'
        """
        setattr(self, 'user_action', 'BadSubtraction')
        time.sleep(0.1)
        plt.close()
        return

    def label_psf_in_temp(self, event):
        """
        Called if user labels image as 'Point Source in Template'
        """
        setattr(self, 'user_action', 'PsfInTemplate')
        time.sleep(0.1)
        plt.close()
        return


    def label_noisy_template(self, event):
        """
        Called if user labels image as 'Noisy Template'
        """
        setattr(self, 'user_action', 'NoisyTemplate')
        time.sleep(0.1)
        plt.close()
        return

    def label_dark_spot_in_temp(self, event):
        """
        Called if user labels image as 'Dark Spot in Template Center'
        """
        setattr(self, 'user_action', 'DarkSpotInTemplateCenter')
        time.sleep(0.1)
        plt.close()
        return

    def label_marginal(self, event):
        """
        Called if user labels image as 'Marginal'
        """
        setattr(self, 'user_action', 'Marginal')
        time.sleep(0.1)
        plt.close()
        return
    
    def label_unsure(self, event):
        """
        Called if user labels image as 'Unsure'
        """
        setattr(self, 'user_action', 'Unsure')
        time.sleep(0.1)
        plt.close()
        return

    def label_other(self, event):
        """
        Called if user labels image as 'Other'. Prompts user for comment
        """
        setattr(self, 'user_action', 'Other')

        # In this case, promt the user for more information
        user_comment = input("\nUser Comment: ")
        setattr(self, 'user_comment', user_comment)

        plt.close()
        return

    def label_back(self, event):
        """
        Called if a user chooses to go back an image
        """
        setattr(self, 'user_action', 'Back')
        time.sleep(0.1)
        plt.close()
        return

    #def label_skip(self, event):
    #    """
    #    Called if a user chooses to skip an image 
    #    """
    #    setattr(self, 'user_action', 'Skip')
    #    time.sleep(0.1)
    #    plt.close()
    #    return

    def label_help(self, event):
        """
        Called if a user asks for help. Displays a sample image for each class.
        """

        #Don't close the image in this case so that the user can still classify it

        #TODO
        print("Hey, sorry I haven't gotten around to making this button do anything yet.")
        print("Just pop a screenshot in the #artifactspy channel or mark as Unsure.")
        return




