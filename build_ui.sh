#!/bin/bash

BASE_PATH="src/ui"
ASSETS_PATH="src/resources"
echo -n "Building Ui..."

files=("$BASE_PATH"/*.ui)
total=${#files[@]}
bar_size=30

if [ "$total" -eq 0 ] || [ ! -e "${files[0]}" ]; then
    echo "Nessun file .ui trovato in $BASE_PATH"
    exit 1
fi

i=1
for f in "${files[@]}"; do
    filename=$(basename "$f")
    
    completed=$((i * bar_size / total))
    remaining=$((bar_size - completed))
    
    bar=$(printf '█%.0s' $(seq 1 $completed 2>/dev/null))
    empty=$(printf '░%.0s' $(seq 1 $remaining 2>/dev/null))
    
    printf "\r[%s%s] %d/%d - %s\033[K" "$bar" "$empty" "$i" "$total" "$filename"
    
    pyside6-uic --from-imports "$f" -o "$BASE_PATH/ui_$(basename "${f%.ui}").py"
    sleep 0.1
    
    ((i++))
done
echo ""

echo -n "Building Resource file..."


output=$(pyside6-rcc "src/resources.qrc" -o "$BASE_PATH/resources_rc.py" 2>&1)
err_code=$?

if [ $err_code -eq 0 ]; then
    echo " OK!"
else
    echo " FAILED!"
    echo "Dettagli dell'errore:"
    echo "$output"
fi