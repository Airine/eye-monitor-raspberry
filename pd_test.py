import pandas as pd

chans = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
record_data = pd.DataFrame(columns=['MIC1', 'MIC2', 'MIC3', 'MIC4'])
for i in range(len(chans[0])):
    pd.concat(record_data, pd.DataFrame([chans[0][i], chans[1][i], chans[2][i], chans[3][i]], columns=['MIC1','MIC2','MIC3','MIC4']), ignore_index=True)
    print([chans[0][i], chans[1][i], chans[2][i], chans[3][i]])
print(record_data)
