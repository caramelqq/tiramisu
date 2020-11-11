def binomial_calc(thresh : int, kc : int, drate_denom : int, dpk=1) -> float:
    # Calculate threshold and set to 9 if thresh > 9
    thresh_at_kc = kc // thresh
    if thresh_at_kc > 9:
        thresh_at_kc = 9

    # Calculate remainders and initialize KC array
    kc_arr = [0] * 10

    for i in range(len(kc_arr)):
        if kc >= thresh:
            if i == len(kc_arr)-1:
                kc_arr[i] = kc
            else:
                kc -= thresh
                kc_arr[i] = thresh
        else:
            kc_arr[i] = kc % thresh
            break

    # Binomial distribution equation
    chance = (1-
        (1-dpk*1/drate_denom)**int(kc_arr[0])*
        (1-dpk*2/drate_denom)**int(kc_arr[1])*
        (1-dpk*3/drate_denom)**int(kc_arr[2])*
        (1-dpk*4/drate_denom)**int(kc_arr[3])*
        (1-dpk*5/drate_denom)**int(kc_arr[4])*
        (1-dpk*6/drate_denom)**int(kc_arr[5])*
        (1-dpk*7/drate_denom)**int(kc_arr[6])*
        (1-dpk*8/drate_denom)**int(kc_arr[7])*
        (1-dpk*9/drate_denom)**int(kc_arr[8])*
        (1-dpk*10/drate_denom)**int(kc_arr[9])
        )*100

    return chance