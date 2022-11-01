#!/bin/bash
path=$1
glob=$2
root_path=$path/*.tfstate
folder_path=$path/**/*.tfstate

for filename in $root_path; do
    name=$(basename $filename)
    echo ""
    echo "****************"
    echo "Processing $filename"
    echo "****************"
    type_name=${name//.tfstate/}
    folder=${filename//$name/}
    int_name=$(basename $folder)
    output="$int_name-$type_name"
    config="$int_name-$type_name.json"
    title="$int_name ($type_name)"
    python ./drawtf/cli.py --name "$title Design" --state $filename --output-path "$folder/$output" --json-config-path "$folder/$config"
    touch  "$folder/$config"
done;

for filename in $folder_path; do
    name=$(basename $filename)
    echo ""
    echo "****************"
    echo "Processing $filename"
    echo "****************"
    type_name=${name//.tfstate/}
    folder=${filename//$name/}
    int_name=$(basename $folder)
    output="$int_name-$type_name"
    config="$int_name-$type_name.json"
    title="$int_name ($type_name)"
    python ./drawtf/cli.py --name "$title Design" --state $filename --output-path "$folder/$output" --json-config-path "$folder/$config"
    touch  "$folder/$config"
done;

#python ./drawtf/cli.py --name "apa test Design" --state "C:\Users\MichaLaw\Desktop\ipg\apa\infrastructure.tfstate" --output-path "C:\Users\MichaLaw\Desktop\ipg\apa\apa-infrastructure" --json-config-path "C:\Users\MichaLaw\Desktop\ipg\apa\apa-infrastructure.json"