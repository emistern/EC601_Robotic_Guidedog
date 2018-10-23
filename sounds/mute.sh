ffmpeg -i Steel-Bell-C6.wav -map_channel -1 -map_channel 0.0.1 right.wav
ffmpeg -i right.wav -map_channel 0.0.1 -map_channel 0.0.0 left.wav

ffmpeg -i Steel-Bell-C6.wav -i right.wav -filter_complex "[0:a][1:a]amerge=inputs=2,pan=stereo|c0<c0+c2|c1<c1+c3[aout]" -map "[aout]" mid_right.mp3

ffmpeg -i Steel-Bell-C6.wav -i left.wav -filter_complex "[0:a][1:a]amerge=inputs=2,pan=stereo|c0<c0+c2|c1<c1+c3[aout]" -map "[aout]" mid_left.mp3
