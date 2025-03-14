.PHONY: all clean

all: venv37pt1cu11/bin/activate venv37pt1cu11/lib/python3.7/site-packages/torch

    
venv37pt1cu11/bin/activate:

	test -d venv37pt1cu11 || virtualenv -p python3.7 venv37pt1cu11

	. venv37pt1cu11/bin/activate; pip install Cython;pip install -r requirements.txt; pip install matplotlib;
	touch venv37pt1cu11/bin/activate
    
venv37pt1cu11/lib/python3.7/site-packages/torch: venv37pt1cu11/bin/activate
	. venv37pt1cu11/bin/activate; pip install pip --upgrade; pip3 install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html

clean:
	rm -fr venv37pt1cu11
	find -iname "*.pyc" -delete
