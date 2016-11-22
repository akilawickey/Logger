# $dir = 'battery.csv'

# if [[ ! -e $dir ]]; then
#     mkdir $dir
# elif [[ ! -d $dir ]]; then
#     echo "$dir already exists but is not a directory" 1>&2
# fi
sudo pkill -f logger.py
sudo python logger.py
