import settings
import os
dir = settings.basedirectory;
def AddMPIDtoManifest(mpid):
    f = open(dir+'\\APIMining\\MaterialsAPIMiner\\mpids.txt', 'r');
    flist = f.readlines();
    f.close();
    f = open(dir+'\\APIMining\\MaterialsAPIMiner\\mpids.txt', 'a');
    found = False;
    for line in flist:
        if(mpid in line):
            found = True;
            print('found')
            break;

    if not found:
        print('new compound')
        f.write(mpid);
        f.write('\n');
    f.close();

