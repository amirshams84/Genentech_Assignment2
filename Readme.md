Genentech Assignment
========================================

This is the workflow which provide a WDL pipeline for single cell downstream analysis using scanpy


## How to Build the Docker environment:

    Download provided Docker file and run the following command:
    docker build -t amir_docker -f Docker .
    it will create a Docker image includes a conda environment including all required packages and software

## How to run on Desktop
    Assign a directory as working directory on your Dekstop or server, call that "WorkDir" or any name
    the script will use the assigned space for the result outputs
    cd ~/WorkDir
    docker run -it -v $(PWD):/result amir_docker /bin/bash /script/Genentech_Assignment/execute_desktop.sh
  
## How to run on AWS
    it will use AWS batch system to submit jobs and follow their execution
    Assign a directory as working directory on your Dekstop or server, call that "WorkDir" or any name
    the script will use the assigned space for the result outputs
    cd ~/WorkDir
    docker run -it -v $(PWD):/result amir_docker /bin/bash /script/Genentech_Assignment/execute_aws.sh

## Result
  - *.h5ad seurat object includes count matrix with all annotations
  - *.png figures generated through pipeline process


## Caveat
 - not throughly tested 
 - customized for screening only


