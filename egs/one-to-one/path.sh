#export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
#export CUDA_HOME=/usr/local/cuda
echo "path.shを実行します"
export LD_LIBRARY_PATH=/usr/local/cuda-11.1/lib64:$LD_LIBRARY_PATH
echo "LD_LIBRARY_PATHは $LD_LIBRARY_PATH"
export CUDA_HOME=/usr/local/cuda-11.1
echo "CUDA_HOMEは $CUDA_HOME"
export PRJ_ROOT=../..
ls $PRJ_ROOT
echo "PRJ_ROOTは $PRJ_ROOT"
#source $PRJ_ROOT/tools/venv/bin/activate
#source $PRJ_ROOT/tools/venv37/bin/activate
#source $PRJ_ROOT/tools/venv37pt1/bin/activate
source $PRJ_ROOT/tools/venv37pt1cu11/bin/activate
export PATH=$PATH:$PRJ_ROOT/src/bin:$PRJ_ROOT/src/utils
echo "pathは $PATH"
export PYTHONPATH=$PRJ_ROOT/src/nets:$PRJ_ROOT/src/utils
echo $PYTHONPATH
