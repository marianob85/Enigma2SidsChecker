# Enigma2SidsChecker
Check if Enigma2 channel list contain channels from SID's list

## Usage

```python
python CheckSids.py -l "c:\ChannelLists\Enigma2\lamedb" -i lookupsids.txt -o notfoundSids.txt
```
Example of output contain sid which was not found in **Channel** bouquets
```
Channels
	3780:14208:	EUROSPORT 3 HD
	0DB0:3504:	EUROSPORT 5 HD
	2908:10504:	TENIS PREMIUM 1
	0C30:3120:	TENIS PREMIUM 2
```
