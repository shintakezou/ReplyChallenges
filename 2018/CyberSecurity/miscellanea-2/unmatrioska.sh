#! /bin/bash

cnt=1
current=matrioska

test -d _temp || mkdir _temp
test -d results || mkdir results
cp "$current" results
pushd results
ln -s "$current" $(printf "%04d" $cnt)
((cnt++))

while [[ $(file "$current" |grep -cE "archive|compress") -gt 0 ]]
do
    pushd ../_temp
    7z e "../results/$current"
    nxt=$(ls -1|head -n1)
    if [[ -z "$nxt" ]]; then
	break
    fi
    popd
    mv "../_temp/$nxt" .
    rm "../_temp/$nxt"
    ln -s "$nxt" $(printf "%04d" $cnt)
    current="$nxt"
    ((cnt++))    
done

popd

echo "CNT $cnt"

