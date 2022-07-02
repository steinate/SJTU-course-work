sysbench cpu --cpu-max-prime=2000000 --threads=2 run --time=1000 & pgrep sysbench > /proc/watch
while true;
do
cat /proc/watch >> result1.txt;
sleep 0.01;
done;
