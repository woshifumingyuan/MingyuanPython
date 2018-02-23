"""Main script for generating output.csv."""
import pandas as pd

def main():
    # add basic program logic here
    comb = pd.read_csv(r'python_hiring_test/combinations.txt')

    pitch = pd.read_csv(r'python_hiring_test/pitchdata.csv')

    col = ['SubjectId','Stat','Split','Subject','Value']
    outdf = None
    ans = []

    for index, row in comb.iterrows():
        #Read combfile
        st = row['Stat']
        sb = row['Subject']
        sp = row['Split']

        #Filter
        filt = None
        if sp == 'vs LHH':
            filt = pitch.loc[pitch['HitterSide']=='L']
        elif sp == 'vs RHH':
            filt = pitch.loc[pitch['HitterSide']=='R']
        elif sp == 'vs LHP':
            filt = pitch.loc[pitch['PitcherSide']=='L']
        elif sp == 'vs RHP':
            filt = pitch.loc[pitch['PitcherSide']=='R']

        #Group
        if sb == 'HitterId':
            filt = filt.groupby(['HitterId']).sum()
        elif sb == 'HitterTeamId':
            filt = filt.groupby(['HitterTeamId']).sum()
        elif sb == 'PitcherId':
            filt = filt.groupby(['PitcherId']).sum()
        else:
            filt = filt.groupby(['PitcherTeamId']).sum()

        #calculate val when PA >= 25
        filt = filt.loc[filt['PA'] >= 25]

        for index, row in filt.iterrows():
            val = 0
            if st == 'AVG':
                val = round(row['H']/row['AB'],3)
            elif st == 'OBP':
                val = round((row['H']+row['BB']+row['HBP'])/(row['AB']+row['BB']+row['HBP']+row['SF']),3)
            elif st == 'SLG':
                val = round((row['2B']+2*row['3B']+3*row['HR']+row['H'])/row['AB'],3)
            else:
                val = round((row['H']+row['BB']+row['HBP'])/(row['AB']+row['BB']+row['HBP']+row['SF'])
                +(1*row['2B']+2*row['3B']+3*row['HR']+row['H'])/row['AB'],3)
            ans.append([index,st,sp,sb,val])
    outdf = pd.DataFrame(ans,columns=col)
    outdf = outdf.sort_values(by=col)
    outdf.to_csv('python_hiring_test/data/processed/output.csv',index=False)

if __name__ == '__main__':
    main()
