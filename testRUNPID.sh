echo $$ > runpid
until python3 computing_server.py >> servlogSinceApr23rd2018.txt 2>&1; do
    echo "$(date -u) \t Server 'myserver' crashed with exit code $?.  Respawning.." >> crashlog.txt
    sleep 1
done 
