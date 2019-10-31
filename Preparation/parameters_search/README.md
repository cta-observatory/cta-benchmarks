# How to run these preparation data scripts:

- parametrize the notebooks stored in `tests/` through `papermill` with your `yourparameterfile.yml`
- run `param_cleaning_per_event_cam.ipynb`
- run `param_cleaning_per_event_cam_energybin.ipynb`

# Storage info:

- the output data will be stored in `prepared_data/output`
- there will be a set of data splitted by camera type (`prepared_data/output/event_cam`)
- there will be a set of data splitted by camera type and energy range (`prepared_data/output/event_cam_energybin`)
- the  output files will be compressed and stored by numpy module (`.npz`)