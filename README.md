# Overview
Author: Qian Shu
Date: 09/01/2022
contact: shumarkq@gmail.com

DepoBoxToolv is an open-source, python-based tool to create a box model for testing different dry deposition algorithms over various land use categories. It can be easily used, modified, and distributed throughout the research community to help translate between deposition models and measurements. The model is developed for CMAQ dry deposition improvment projects (v5.3). 

For future use and citation, please see recent published paper.
**Shu, Q., Murphy, B., Schwede, D., Henderson, B.H., Pye, H.O., Appel, K.W., Khan, T.R. and Perlinger, J.A., 2022. 
Improving the particle dry deposition scheme in the CMAQ photochemical modeling system. Atmospheric Environment, p.119343.https://doi.org/10.1016/j.atmosenv.2022.119343**

# Notes
1. DepoBoxtool has been updated to version 2.0. Follow-up updates on github will be based on DepoBoxToolv2.0.
2. DepoBoxToolv1.0 is deprecated. Archive version can be found from 
**Shu, Qian. (2021). Particle dry deposition algorithms in CMAQ version 5.3: characterization of critical parameters and land use dependence using    DepoBoxTool version 1.0. https://doi.org/10.5281/zenodo.4749636**

# Instructions
```
To use DepoBoxTool
    1. Build: python setup.py install. It will create build, dist and DepoBoxTool.egg-info directories in your current path.

    2. Run: cd scripts/, example scripts are included to help you understand how to call the function from src and 
       output results. You are welcome to change whatever you like in example scripts. But I suggest to
       go through all example scripts and understand how to call "RUN_MOD" and "RUN_SID" to output results from depoboxtool.
       The first output in tuples is Vd but you can actually output all components or prameters for each 
       depostion scheme saved in src/func_models.py. For python users, you can directly call functions to plot figures. For
       non-python users, you can save these outputs as csv, excel or other formats to do visualization.

    3. Modify: cd src/
               add customized deposition schemes, check func_models.py
               add customized land use parameters, check func_lucs.py
               add customized evaluation metrics, check func_evals.py
               add customized particles distributions, check func_bins.py

    4. Remove: pip uninstall DepoBoxTool
               rm -r build
               rm -r dist
               rm -r DepoBoxTool.egg-info

    5. **Everytime if you change code in src/, you must remove old packages and rebuild, or it will not take effects.**
        1. follow step 4
        2. then redo step 1
```
        
# DepoBoxToolv2.0 structure
```bash
packaging_tutorial/
├── README.md
├── setup.py
├── src/
│   └── DepoBoxTool/
│   |   ├── __init__.py
│   |   └── func_bins.py
│   |   └── func_evals.py
│   |   └── func_lucs.py
│   |   └── func_models.py
├── data/
│   └── obs_combined.csv
├── scripts/
│   ├── main.py
│   └── example_eval_metrics.py
│   └── example_plt_VdoverDp_MOD_for_particle_number_multipanels.py
│   └── example_plt_VdoverDp_SID_cf_singlepanel.py
│   └── example_plt_VdoverDp_SID_df_singlepanel.py
│   └── example_plt_VdoverDp_SID_water_singlepanel.py
│   └── example_plt_VdoverDp_SID_grass_singlepanel.py
```
