# Enc0ded

		BMO told us this server would send us a flag but its
		just sending us some stupid flipping picture! Would you 
		straighten this out? 

		host:ip

**Files:** original_qr.png
**Links:** None

## Solution 
The first QR code simply decodes to a link to the Wikipedia page on steganography. This should entice you to strings the file or something of that sort, which will lead you to find a chunk of Python code in the file. If you run this code, you will connect to the same server, but this time with a specific tag. This will prompt the server to send you a base64-encoded barcode, which will decode to the flag. 
