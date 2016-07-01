mkdir tmp/
cd tmp/
curl -O https://pypi.python.org/packages/5c/79/5dae7494b9f5ed061cff9a8ab8d6e1f02db352f3facf907d9eb614fb80e9/virtualenv-15.0.2.tar.gz
tar xvfz virtualenv-15.0.2.tar.gz
cd -
python tmp/virtualenv-15.0.2/virtualenv.py .
bin/pip install -r requirements.txt
bin/pip install -e .
