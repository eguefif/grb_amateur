fake_messages = [
        b'TITLE:           GCN/FERMI NOTICE\nNOTICE_DATE:     Mon 17 Nov 25 12:19:53 UT\nNOTICE_TYPE:     Fermi-GBM Alert\nRECORD_NUM:      1\nTRIGGER_NUM:     785074797\nGRB_DATE:        20996 TJD;   321 DOY;   25/11/17\nGRB_TIME:        44392.14 SOD {12:19:52.14} UT\nTRIGGER_SIGNIF:  7.7 [sigma]\nTRIGGER_DUR:     0.032 [sec]\nE_RANGE:         3-4 [chan]   47-291 [keV]\nALGORITHM:       2\nDETECTORS:       0,0,0, 0,0,0, 0,1,0, 0,0,1, 0,0,\nLC_URL:          http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2025/bn251117514/quicklook/glg_lc_medres34_bn251117514.gif\nCOMMENTS:        Fermi-GBM Trigger Alert.  \nCOMMENTS:        This trigger occurred at longitude,latitude = 44.12,21.00 [deg].  \nCOMMENTS:        The LC_URL file will not be created until ~15 min after the trigger.  \n',
        b'TITLE:           GCN/FERMI NOTICE\nNOTICE_DATE:     Tue 18 Nov 25 19:02:20 UT\nNOTICE_TYPE:     Fermi-GBM Alert\nRECORD_NUM:      1\nTRIGGER_NUM:     785185339\nGRB_DATE:        20997 TJD;   322 DOY;   25/11/18\nGRB_TIME:        68534.17 SOD {19:02:14.17} UT\nTRIGGER_SIGNIF:  4.2 [sigma]\nTRIGGER_DUR:     0.256 [sec]\nE_RANGE:         3-4 [chan]   47-291 [keV]\nALGORITHM:       8\nDETECTORS:       0,1,0, 0,0,0, 0,0,0, 0,1,0, 0,0,\nLC_URL:          http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2025/bn251118793/quicklook/glg_lc_medres34_bn251118793.gif\nCOMMENTS:        Fermi-GBM Trigger Alert.  \nCOMMENTS:        This trigger occurred at longitude,latitude = 120.72,-22.63 [deg].  \nCOMMENTS:        The LC_URL file will not be created until ~15 min after the trigger.  \n'
]


if __name__ == '__main__':
    splits = fake_messages[0].decode().split('\n')
    h = {}
    for entry in splits:
        if len(entry) >= 1:
            key, value = entry.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            if key in h.keys():
                current_value = h[key]
                if isinstance(current_value, str):
                    h[key] = current_value + ' | ' + value 
                else:
                    h[key] = [value]
            else:
                h[key] = value
    print(h['comments'])


