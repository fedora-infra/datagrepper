# .bashrc
source /srv/venv/bin/activate

alias datanommer-consumer-start="sudo systemctl start datanommer.service && echo 'datanommer consumer is running'"
alias datanommer-consumer-logs="sudo journalctl -u datanommer.service"
alias datanommer-consumer-restart="sudo systemctl restart datanommer.service && echo 'datanommer consumer is running'"
alias datanommer-consumer-stop="sudo systemctl stop datanommer.service && echo 'datanommer service stopped'"

alias datagrepper-start="sudo systemctl start datagrepper.service && echo 'datagrepper is running'"
alias datagrepper-logs="sudo journalctl -u datagrepper.service"
alias datagrepper-restart="sudo systemctl restart datagrepper.service && echo 'datagrepper is running'"
alias datagrepper-stop="sudo systemctl stop datagrepper.service && echo 'datagrepper stopped'"
