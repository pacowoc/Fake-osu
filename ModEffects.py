def calculate(AR,CS,OD,mods):
    Mods_Multi = 1
    #HR
    if mods[2] == 1:
        Mods_Multi *= 1.06
        AR*=1.4
        CS*=1.4
        OD*=1.4
        if AR>10:
            AR=10
        if CS>10:
            CS=10
        if OD>10:
            OD=10

    #EZ
    if mods[2] == -1:
        Mods_Multi *= 0.3
        AR*=0.5
        CS*=0.5
        OD*=0.5

    return (AR,CS,OD,Mods_Multi)