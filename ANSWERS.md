## Observed behaviour

Describe in general words the observed behaviour of each of these servers and 
how it affects the video playback experience. Then explain what you believe is
happening and what is causing the described behaviour.

* FUNKY A: Video sometimes breaks for an extremely short amount of time. It does not really cause a
		   negative video playback experience. Probobably because the frames recieved by the servers 
		   at a sligtly lower rate.

* FUNKY B: More video jitter compared to FUNKY A. This causes the video to seemingly pause a couple
		   times for a brief amount of time. This behaviour could be because the server is either
		   sending the packets at a slower rate or there are more packets that are getting lost 
		   during transmission.

* FUNKY C: The video seems discontinuos, like small parts of the video were replayed or maybe frames
		   were not sent by the server. Probably because many of the frames that are needed in 
		   sequential order were missing. 

* FUNKY D: Compared to the previous servers, FUNKY D has more breaks in the video which interrupts
		   the playback a number of times. 

* FUNKY E: Fast forwrd video experience. Server sending frames too quickly.

* FUNKY F: Slow motion video experience. Server sending frames too slowly.

* FUNKY G: Playback speed is low, with occasional pauses. Observed behavior is probably because the server is
		   sending frames at a slow rate

* FUNKY H: The video seems to pause momentarily and proceeds to skip a few frames after pause. The playback speed,however, seems
	       normal. The reason for the pauses could be becuase the server may have, for some reason, blocked transmission for a short 
		   period of time.


## Statistics

You may add additional columns with more relevant data.
Note: 
	all observations are based off movie1.Mjpeg
	FRAME RATE values below include the time taken for frame processing as well.

| FUNKY SERVER | FRAME RATE (pkts/sec) | PACKET LOSS RATE (/sec) | OUT OF ORDER |
|:------------:|-----------------------|-------------------------|--------------|
|      A       |        20.15          |         2.45            |    23 pkts   |
|      B       |        13.46          |         9.23            |    53 pkts   |
|      C       |        22.53          |         0.00            |    104 pkts  |
|      D       |        11.93          |         10.65           |    103 pkts  |
|      E       |        69.63          |         0.00            |    0 pkts    |
|      F       |        9.61           |         0.00            |    0 pkts    |
|      G       |        7.65           |         1.96            |    37 pkts   |
|      H       |        21.64          |         0.48            |    2 pkts    |


## Result of analysis

Explain in a few words what you believe is actually happening based on the statistics above.

* FUNKY A: This server is more or less the same as regular since its frame rate, packet loss rate, and out of order packets are not too high. Hence, the 
		   the playback experience is very close to the regular server.

* FUNKY B: Due to higher packet loss rate with slow transmission rate of the server, we observe brief occasional pauses when the video is played. 

* FUNKY C: Due to a large number of out-of-order packets, the played video looks distorted or discontinuous.

* FUNKY D: The played video sees more distortion because of high packet loss rate along with high number of out-of-order packets. The transmission rate of frames also seems lower.

* FUNKY E: The server is sending frames at a very fast rate, which causes the video to be played at high speed. 

* FUNKY F: The server is sending frames at a very slow rate, which causes the video to be played in slow motion.

* FUNKY G: The server is sending frames at an even slower rate, perhaps the slowest amongst all the servers.

* FUNKY H: The stats look okay; the frame rate seems relatively ok, packet loss and packet order is relatively ok as well. Probably, the server just on very
		   few occasions delays the packet transfer which causes a brief pause in the played video. 

