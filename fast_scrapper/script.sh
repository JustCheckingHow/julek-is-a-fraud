for i in $(cat links); do
    curl -L $i && echo $i >> working_links.txt
done
wait
