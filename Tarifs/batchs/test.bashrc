date

export EDITOR=nano
#export VISUAL=nano; crontab -e

echo "export EDITOR=nano" >> /-bashrc

30 8 * * 1 touch /Volumes/Intranet/Tarifs/batchs/test.txt >> /Volumes/Intranet/Tarifs/batchs/logs/cron.log 2>&1

