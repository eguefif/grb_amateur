fake_messages = [
    b"TITLE:           GCN/FERMI NOTICE\nNOTICE_DATE:     Mon 17 Nov 25 12:19:53 UT\nNOTICE_TYPE:     Fermi-GBM Alert\nRECORD_NUM:      1\nTRIGGER_NUM:     785074797\nGRB_DATE:        20996 TJD;   321 DOY;   25/11/17\nGRB_TIME:        44392.14 SOD {12:19:52.14} UT\nTRIGGER_SIGNIF:  7.7 [sigma]\nTRIGGER_DUR:     0.032 [sec]\nE_RANGE:         3-4 [chan]   47-291 [keV]\nALGORITHM:       2\nDETECTORS:       0,0,0, 0,0,0, 0,1,0, 0,0,1, 0,0,\nLC_URL:          http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2025/bn251117514/quicklook/glg_lc_medres34_bn251117514.gif\nCOMMENTS:        Fermi-GBM Trigger Alert.  \nCOMMENTS:        This trigger occurred at longitude,latitude = 44.12,21.00 [deg].  \nCOMMENTS:        The LC_URL file will not be created until ~15 min after the trigger.  \n",
    #    b"TITLE:           GCN/FERMI NOTICE\nNOTICE_DATE:     Tue 18 Nov 25 19:02:20 UT\nNOTICE_TYPE:     Fermi-GBM Alert\nRECORD_NUM:      1\nTRIGGER_NUM:     785185339\nGRB_DATE:        20997 TJD;   322 DOY;   25/11/18\nGRB_TIME:        68534.17 SOD {19:02:14.17} UT\nTRIGGER_SIGNIF:  4.2 [sigma]\nTRIGGER_DUR:     0.256 [sec]\nE_RANGE:         3-4 [chan]   47-291 [keV]\nALGORITHM:       8\nDETECTORS:       0,1,0, 0,0,0, 0,0,0, 0,1,0, 0,0,\nLC_URL:          http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2025/bn251118793/quicklook/glg_lc_medres34_bn251118793.gif\nCOMMENTS:        Fermi-GBM Trigger Alert.  \nCOMMENTS:        This trigger occurred at longitude,latitude = 120.72,-22.63 [deg].  \nCOMMENTS:        The LC_URL file will not be created until ~15 min after the trigger.  \n",
    b"TITLE:           GCN/FERMI NOTICE\nNOTICE_DATE:     Sat 22 Nov 25 08:36:50 UT\nNOTICE_TYPE:     Fermi-GBM Test Position\nRECORD_NUM:      1\nTRIGGER_NUM:     99999\nGRB_RA:          324.000d {+21h 36m 00s} (J2000),\n                 324.391d {+21h 37m 34s} (current),\n                 323.243d {+21h 32m 58s} (1950)\nGRB_DEC:         -35.000d {-35d 00' 00\"} (J2000),\n                 -34.883d {-34d 52' 58\"} (current),\n                 -35.224d {-35d 13' 26\"} (1950)\nGRB_ERROR:       5.80 [deg radius, statistical plus systematic]\nGRB_INTEN:       1000 [cnts/sec]\nDATA_SIGNIF:     11.78 [sigma]\nINTEG_TIME:      0.064 [sec]\nGRB_DATE:        21001 TJD;   326 DOY;   25/11/22\nGRB_TIME:        31002.00 SOD {08:36:42.00} UT\nGRB_PHI:           0.00 [deg]\nGRB_THETA:         0.00 [deg]\nDATA_TIME_SCALE: 0.0000 [sec]\nHARD_RATIO:      3.18\nLOC_ALGORITHM:   1 (version number of)\nMOST_LIKELY:      67%  Below horizon\n2nd_MOST_LIKELY:  32%  Local Particles\nDETECTORS:       1,1,1, 0,0,0, 0,0,0, 0,0,0, 0,0,\nSUN_POSTN:       238.12d {+15h 52m 30s}  -20.21d {-20d 12' 30\"}\nSUN_DIST:         75.66 [deg]   Sun_angle= -5.8 [hr] (East of Sun)\nMOON_POSTN:      262.13d {+17h 28m 30s}  -28.20d {-28d 11' 45\"}\nMOON_DIST:        52.65 [deg]\nMOON_ILLUM:      4 [%]\nGAL_COORDS:        9.71,-47.83 [deg] galactic lon,lat of the burst (or transient)\nECL_COORDS:      314.69,-19.56 [deg] ecliptic lon,lat of the burst (or transient)\nCOMMENTS:        Fermi-GBM TEST Coordinates.  \nCOMMENTS:        This Notice was ground-generated -- not flight-generated.  \n",
]


def format_grb_position(data):
    return ", ".join([position.strip() for position in data.split(",")])


if __name__ == "__main__":
    splits = fake_messages[2].decode().replace(",\n", ", ").split("\n")
    h = {}
    for entry in splits:
        if len(entry) >= 1:
            key, value = entry.split(":", 1)
            if key == "2nd_most_likely":
                key = "second_most_likely"
            key = key.strip().lower()
            value = value.strip()
            if key in h.keys():
                current_value = h[key]
                if isinstance(current_value, str):
                    h[key] = current_value + " | " + value
                else:
                    h[key] = [value]
            else:
                h[key] = value

    if "grb_ra" in h.keys():
        h["grb_ra"] = format_grb_position(h["grb_ra"])
    if "grb_dec" in h.keys():
        h["grb_dec"] = format_grb_position(h["grb_dec"])

    for key in h:
        print(key)
    print(h["grb_ra"])

    print(h["grb_dec"])
