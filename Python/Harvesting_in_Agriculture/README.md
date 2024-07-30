# Harvesting Behaviour in Agriculture

## Introduction
This sub-repository focuses on developing ABM model studying the harvesting behaviour in Agriculture. I used Mesa as main weapon within Python in the modelling process.
The study case will have grid cell patches as agents that represent farm block (or tree), where the model (logic decision of the farmer) are applying some rule reflecting the harvesting behaviour.
Our main objective is to evaluate and observe which input scenario would yield, and emerge into better profitability for the farmer.

## About this Sub-Repo

We have some files organized within this sub-repo. So to make everything coherence for you to follow I made some material into section:

1. To begin with, I recommend you to visit my Medium article I specifically design to accomodate the need to explain this study case [HERE](https://medium.com/@lazuardy.almuzaki/pythons-agent-based-modelling-for-agriculture-a6259081ab07). From there I believe it will be clearer.
2. The main model is written in Jupyter Notebook files [main_model.ipynb](./main_model.ipynb). It contains major explanation about what we are going to do as well, and also result visualization via the notebook.
3. Python files for Vizualization [main_model_viz.py](./main_model_viz.py). If you clone the repo, this file will run locally and open the browser on localhost server. It will give you web-based, real-time simulation, and properly designed interface feature provided by Mesa.
4. The python file of Streamlit [streamlit_model.py](./streamlit_model.py). This files is the backend source for the web app I deployed as demonstration for this study case which the website could be accessed [HERE](https://agentbasedmodelling-23jpvayz5rr9wn7y2trsqv.streamlit.app/).


## Additional Stuff

There is also file called [ExtraChart.py](./ExtraChart.py) and [FieldModel.py](./FieldModel.py) these are basically just function and class wrapper that is called to the main_model.ipynb and main_model_viz.py.
The ExtraChart holds the customized additional function to Mesa vizualisation ability that is also structured by [HistogramModule.js](./HistogramModule.js). Developing this, I am fully just copied on how official Mesa documentation did it.
The FieldModel.py is basically the main code from main_model.ipynb
