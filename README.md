


1.) First Create a template.py : python template.py 

2.) init_setup.sh file -> write commands and run : bash init_setup.sh 
(it will create env) :- Now you will get env folder 

3.) Write requirements_dev.txt and pip install -r   requirements_dev.txt


4.) write exception.py and run python exception.py(path) 

5.) write logging.py and run python logging.py (path) 

6.) write test.py and run python test.py (path) 

7.) Write data_ingestion.py, data_transformation.py, model_evaluation.py , model_trainer.py in components and run 
      - python data_ingestion.py (path)  [will get artifacts file] 

8.) Now in pipeline folder: write training_pipeline.py file and run : python training_pipeline.py (path) 

9.) Make prediction pipeline :- write code in pipeline -> prediction_pipeline.py -> then make app.py and template folder 

10.) to solve mlflow error:- python -m venv myenv
source myenv/bin/activate  # On Mac/Linux
myenv\Scripts\activate      # On Windows
pip install setuptools


11.) mlflow ui 





