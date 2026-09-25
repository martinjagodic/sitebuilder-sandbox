#!/bin/bash
# Cuts a tall full-page screenshot into segments laid side by side, so a whole
# page can be read at a glance (a 390×9000 capture is unreadable scaled down).
#
#   tile.sh <full-page.png> <out-prefix> [segment-height=1300] [per-sheet=4]
#
# Writes <out-prefix>-0.png, -1.png, … (red fills the unused space).
in=$1; out=$2; seg=${3:-1300}; per=${4:-4}
w=$(sips -g pixelWidth "$in" | awk '/pixelWidth/{print $2}')
h=$(sips -g pixelHeight "$in" | awk '/pixelHeight/{print $2}')
n=$(( (h + seg - 1) / seg )); sheet=0
for ((i=0; i<n; i+=per)); do
  inputs=(); filt=""; k=0
  for ((j=i; j<i+per; j++)); do
    y=$((j*seg)); inputs+=(-i "$in")
    if (( y < h )); then
      ch=$(( h - y < seg ? h - y : seg ))
      filt+="[$k]crop=$w:$ch:0:$y,pad=$w+8:$seg:0:0:color=red[v$k];"
    else
      filt+="color=c=red:s=$((w+8))x$seg[v$k];"
    fi
    k=$((k+1))
  done
  for ((m=0; m<k; m++)); do filt+="[v$m]"; done
  ffmpeg -loglevel error -y "${inputs[@]}" -filter_complex "${filt}hstack=inputs=$k" -frames:v 1 "${out}-${sheet}.png"
  echo "${out}-${sheet}.png"; sheet=$((sheet+1))
done
