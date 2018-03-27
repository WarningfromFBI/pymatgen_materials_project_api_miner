
import os

'''
function to add in new MPIDS
again, assu
'''

def AddMPIDtoManifest(mpid):
    '''
    :param mpid: string mpid of the form "mp-#######'
    :return:
    '''

    #get all existing mpids to check for membership
    f = open(os.pathjoin(os.curdir, 'mpids.txt'), 'r');
    flist = f.readlines();
    f.close();
    #reopen file for appending at the end
    f = open(os.path.join(os.curdir, 'mpids.txt'), 'a');
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

