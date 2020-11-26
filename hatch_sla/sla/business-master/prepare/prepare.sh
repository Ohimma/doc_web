if [[ -d venv ]]; then
    rm -rf venv
fi
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r pip-req.txt
## 退出 deactivate
