pd.DataFrame({'real':f.Volume, 'lagged':f.Volume.shift()}).corr()