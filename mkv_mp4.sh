for i in *.mkv; do
    ffmpeg -i "$i" -acodec ac3 -vcodec copy "${i%.*}.mp4"
done
