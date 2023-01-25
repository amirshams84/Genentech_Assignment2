# WORKFLOW DEFINITION 
workflow pipeline {

  Array[File] h5_files
   
  scatter(s in h5_files) {
    call scanpy_clustering { input: h5_file=s }
  }

}

task scanpy_clustering {
  File h5_file
  String prefix = sub(basename(h5_file), ".h5", "")

  command <<<
    set +eu && PS1=dummy && . /opt/conda/etc/profile.d/conda.sh;
    conda activate Scanpy_conda
    
    python /script/Genentech_Assignment/py_script/scanpy_clustering.py ${prefix} ${h5_file} /result/
    
  >>>

  output {
    File Seurat_Object  = "/result/${prefix}.h5ad"
  }
  runtime {}

}
