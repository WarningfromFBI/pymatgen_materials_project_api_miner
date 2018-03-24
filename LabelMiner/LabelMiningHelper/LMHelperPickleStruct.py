import feature_miner_functions.FeatureMinerHelper.CalculationHelpers as ch

def getLiVolumeFraction(pickleStruct):
    LiVol = 0; TotVol = 0;
    for sites in pickleStruct:
        vol = ch.sphereVol(sites.specie.average_ionic_radius)
        if(sites.specie.name == 'Li'):
            LiVol += vol;
        TotVol += vol;
    return LiVol/TotVol; #this is like number of atoms normalized by volume fraction
