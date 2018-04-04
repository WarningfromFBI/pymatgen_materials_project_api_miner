
import os

'''
function to add in new MPIDS: this function is generally important
because the search from the battery explorer may find some compounds which were not in the mpids.txt file
always creates a new file called 'discovered_mpids.txt'. You can add these mpids listed into the master
mpids file
'''

def AddMPIDtoManifest(mpid):
    '''
    :param mpid: string mpid of the form "mp-#######'
    :return:
    '''
    if(not os.path.isfile(os.path.join(os.curdir, 'discovered_mpids.txt'))):
        f = open('discovered_mpids.txt', 'w+')
        f.close();
    #get all existing mpids to check for membership
    f = open(os.path.join(os.curdir, 'discovered_mpids.txt'), 'r');
    flist = f.readlines();
    f.close();
    #reopen file for appending at the end
    f = open(os.path.join(os.curdir, 'discovered_mpids.txt'), 'a');
    found = False;
    #check if the mpid already exists or not
    for line in flist:
        if(mpid in line):
            found = True;
            print('found')
            break;
    #write new mpid because it wasn't found
    if not found:
        print('new compound')
        f.write(mpid);
        f.write('\n');
    f.close();

