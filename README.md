# xat Client (Free Version)

## Install
Before going to Chrome, make sure you have Python 2.7 downloaded & installed.
The following instructions apply if you are using Windows and Chrome or Opera.

##### IMPORTANT UPDATE:  xat has changed the way Clients connect, you **must** download Requestly to work around this.

1. Download Requestly (Chrome) or Modify Header Value (Opera) extensions.
2. Chrome: Open Requestly then select upload rules on the top right corner (here) then use the "requestly_rules.txt" file in your mods folder.
Opera: I haven't the opera extension but try to mimic this behavior: http://imgur.com/AQXVVO8.png
> /^https?:\/\/xat\.com\/web_gear\/chat\/ip2\.php/i > http://localhost:10101/ip2.php

#### Client Setup
1. Set your browsers PAC file by going to: Chrome://settings/search#change%20proxy
Opera: Settings > Browser > Network
2. Press "Change proxy settings..."
3. In the popup, press "LAN Settings" (near the bottom)
4. In the new popup, check the box next to: "User automatic configuration script"
5. In the textfield next to "Address", enter the proxy address | Disable autodetect configuration.
> http://client.lejonathan.com/proxy.pac
Example: http://i.imgur.com/Ljvr25d.png
6. Press "OK" to exit the popups
7. Delete your cache for the past hour by going to: Chrome://settings/clearBrowserData
Opera: Settings > Privacy
8. Tick the box next to "Cached images and files" and delete the items for the past hour
9. Run start.py, open xat (or refresh your page) then wait for your console box to say " > Connection established"
10. Once you see the connection confirmation, your xat page should say "Client enabled"
## Notes
Client users can join my discord server for instant help: https://discord.gg.FDsygwV
I cannot be held responsible for any trouble you may encounter using this client
I will not be providing free code for you to add to your client, do not nag/beg for more

Bug resolution:
* Print expected outputs or variables frequently
* Use exceptions
* [!] Double-check indents (*Very common issue people run into*) 
* Use IDLE for debugging
* Visit this website for common mistakes to avoid
* Google errors
