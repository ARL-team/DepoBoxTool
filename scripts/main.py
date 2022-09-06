from DepoBoxTool.func_evals import *
from DepoBoxTool.func_bins import *
from DepoBoxTool.func_lucs import *
from DepoBoxTool.func_models import *
import pandas as pd
pd.set_option('display.max_rows', 1000)

dataset = pd.read_csv('../data/obs_combined.csv')
obs = dataset[dataset.Vd_cm >= 0]
df_cf = obs[obs.luc == 'coniferousforest']
df_df = obs[obs.luc == 'deciduousforest']
df_grass = obs[obs.luc == 'grass']
df_water = obs[obs.luc == 'water']

def main():
    df = dataset
    df['id'] = df['luc'] + df['researchid'] + df['researchyear']
    print(df.groupby(['id'])['density'].count())

if __name__ == '__main__':
    main()

