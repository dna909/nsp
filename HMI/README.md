# NSPanel Lovelance UI

The HMI Project of this project is only used to display stuff, navigation ist mostly up to the backend. This allows to be way more flexible.

Messages to the Panel can be send through the Command `CustomSend`, which is implemented in the berry driver.
You can issue this command through MQTT by sending messages to the `cmnd/XXX/CustomSend` Topic.
Messages from the Panel are send to the `tele/XXX/RESULT` Topic, encoded in json `{"CustomRecv":"message_from_screen"}`

## Startup

On startup the panel will send `{"CustomRecv":"event,startup,39,eu"}` every few seconds.

```
event,   #Every message from the screen will start with `event`
startup, #Startup Event
39,      #Current HMI Project Version
eu       #Current HMI Project Model
```

You can answer this message in many different ways, but in general the goal is to navigate way from the startup page. In the following example we will navigate to the screensaver page.

Send the following messages to the CustomSend Topic. (You can also send them on tasmota console for testing)

### Some preperation before we are acually navigating away:

Send this every minute: `time~18:17`

Send this at least once at midnight: `date~Donnerstag, 25. August 2022`

Send theese message once after receiving the startup event (parameters will be explained later):

`timeout~20`

`dimmode~10~100~6371`

### Navigate from the startup page to the screensaver, by sending this command to the CustomSend Topic.

`pageType~screensaver`

After sending this command you should already see the time and date.
To also show weather data you have to send them with weatherUpdate, but we will skip this for now.

### Exit Screensaver

Touching the panel on the screensaver will result in this MQTT Message on the result topic:

`event,buttonPress2,screensaver,bExit,1`

You can answer this by sending theese commands to the CustomSend Topic.

`pageType~cardEntities`

`entityUpd~test~1|1~light~light.schreibtischlampe~X~17299~Schreibtischlampe~0~text~sensor.server_energy_power~Y~17299~Server ENERGY Power~155 W~shutter~cover.rolladenfenster_cover_1~Z~17299~Fenster Eingang~A|B|C|disable|enable|enable~switch~switch.bad~D~63142~Bad~1`

## Messages to Nextion Display

### General Commands, implemented on all pages

set brightness of screensaver and active-brightness:

`dimmode~0~100 - (screen off)`

`dimmode~100~100 - (screen on with full brightness)`

set current time:

`time~22:26`

set current date:

`date~Di 24. Februar`

set screensaver timeout (set time in sec~ max 65):

`timeout~15 - timeout after 15 seconds`

`timeout~0 - disable screensaver`

change the page type:

`pageType~pageStartup`

`pageType~cardEntities`

`pageType~cardThermo`

`pageType~cardMedia`

`pageType~popupLight~Schreibtischlampe~light.schreibtischlampe`

`pageType~popupNotify`

`pageType~screensaver`

### screensaver page

`weatherUpdate~tMainIcon~tMainText~tForecast1~tF1Icon~tForecast1Val~tForecast2~tF2Icon~tForecast2Val~tForecast3~tF3Icon~tForecast3Val~tForecast4~tF4Icon~tForecast4Val~optionalLayoutIcon~optionalLayoutText~altIconFont~altIconFont`

`color~background~time~timeAMPM~date~tMainIcon~tMainText~tForecast1~tForecast2~tForecast3~tForecast4~tF1Icon~tF2Icon~tF3Icon~tF4Icon~tForecast1Val~tForecast2Val~tForecast3Val~tForecast4Val~bar~tMRIcon~tMR`

`notify~heading~text`

### cardEntities Page

Structure (Category): `entityUpd~title~[navigation]~[entity_information]`
Example with 4 Entities: 
```
entityUpd~LightTest~button~navigate.prev~<~65535~~~button~navigate.next~>~65535~~light~light.bed_light~A~17299~Bed Light~0~light~light.ceiling_lights~B~52231~Ceiling Lights~1~switch~switch.ac~C~17299~AC~0~switch~switch.decorative_lights~D~65222~Decorative Lights~1
```

<table>
<thead>
  <tr>
    <th>Number</th>
    <th>Category</th>
    <th>Location</th>
    <th>Type</th>
    <th>Field</th>
    <th>Addional Information</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td>instruction</td>
    <td></td>
    <td>instruction</td>
    <td>entityUpd</td>
    <td></td>
  </tr>
  <tr>
    <td>1</td>
    <td>title</td>
    <td>title</td>
    <td>title</td>
    <td>title</td>
    <td></td>
  </tr>
  <tr>
    <td>2</td>
    <td rowspan="12">Navigation</td>
    <td rowspan="6">Upper Left Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>3</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>4</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>5</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>6</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>7</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>8</td>
    <td rowspan="6">Upper Right Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>9</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>10</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>11</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>12</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>13</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>14</td>
    <td rowspan="36">Entities</td>
    <td rowspan="6">First Entity</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>15</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>16</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>17</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>18</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>19</td>
    <td colspan="2">optionalValue</td>
  </tr>
  <tr>
    <td>20</td>
    <td rowspan="6">Second Entity</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>21</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>22</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>23</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>24</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>25</td>
    <td colspan="2">optionalValue</td>
  </tr>
  <tr>
    <td>26</td>
    <td rowspan="6">Thrid Entity</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>27</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>28</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>29</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>30</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>31</td>
    <td colspan="2">optionalValue</td>
  </tr>
  <tr>
    <td>32</td>
    <td rowspan="6">Forth Entiry</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>33</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>34</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>35</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>36</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>37</td>
    <td colspan="2">optionalValue</td>
  </tr>
  <tr>
    <td>38</td>
    <td rowspan="6">Fifth Entiy (US Portrait&nbsp;&nbsp;&nbsp;Version)</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>39</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>40</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>41</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>42</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>43</td>
    <td colspan="2">optionalValue</td>
  </tr>
  <tr>
    <td>44</td>
    <td rowspan="6">Sixth Entiy (US Portrait&nbsp;&nbsp;&nbsp;Version)</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>45</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>46</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>47</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>48</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>49</td>
    <td colspan="2">optionalValue</td>
  </tr>
</tbody>
</table>

### cardGird Page

cardGrid is using the exact same message cardEntities is using; it ignores the information supplied in optionalValue, because it isn't needed for cardGrid

<table>
<thead>
  <tr>
    <th>Parameter&nbsp;&nbsp;&nbsp;Number</th>
    <th>Category</th>
    <th>Location</th>
    <th>Type</th>
    <th>Field</th>
    <th>Addional Information</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td>instruction</td>
    <td></td>
    <td>instruction</td>
    <td>entityUpd</td>
    <td></td>
  </tr>
  <tr>
    <td>1</td>
    <td>title</td>
    <td>title</td>
    <td>title</td>
    <td>title</td>
    <td></td>
  </tr>
  <tr>
    <td>2</td>
    <td rowspan="12">Navigation</td>
    <td rowspan="6">Upper Left Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>3</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>4</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>5</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>6</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>7</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>8</td>
    <td rowspan="6">Upper Right Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>9</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>10</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>11</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>12</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>13</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>14</td>
    <td rowspan="36">Entities</td>
    <td rowspan="6">First Entity</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>15</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>16</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>17</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>18</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>19</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>20</td>
    <td rowspan="6">Second Entity</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>21</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>22</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>23</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>24</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>25</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>26</td>
    <td rowspan="6">Thrid Entity</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>27</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>28</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>29</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>30</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>31</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>32</td>
    <td rowspan="6">Forth Entiry</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>33</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>34</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>35</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>36</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>37</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>38</td>
    <td rowspan="6">Fifth Entiy (US Portrait&nbsp;&nbsp;&nbsp;Version)</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>39</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>40</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>41</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>42</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>43</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>44</td>
    <td rowspan="6">Sixth Entiy (US Portrait&nbsp;&nbsp;&nbsp;Version)</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>45</td>
    <td colspan="2">intNameEntity</td>
  </tr>
  <tr>
    <td>46</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>47</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>48</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>49</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
</tbody>
</table>

### cardMedia

Example without icons in bottom row: `entityUpd~Kitchen~button~navigation.up~U~65535~~~delete~~~~~~media_player.kitchen~I'm a Hurricane~~Wellmess~~100~A~64704~B~media_pl~media_player.kitchen~C~17299~Kitchen~`

<table>
<thead>
  <tr>
    <th>Parameter&nbsp;&nbsp;&nbsp;Number</th>
    <th>Category</th>
    <th>Location</th>
    <th>Type</th>
    <th>Field</th>
    <th>Addional Information</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td>instruction</td>
    <td></td>
    <td>instruction</td>
    <td>entityUpd</td>
    <td></td>
  </tr>
  <tr>
    <td>1</td>
    <td>title</td>
    <td>title</td>
    <td>title</td>
    <td>title</td>
    <td></td>
  </tr>
  <tr>
    <td>2</td>
    <td rowspan="12">Navigation</td>
    <td rowspan="6">Upper Left Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>3</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>4</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>5</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>6</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>7</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>8</td>
    <td rowspan="6">Upper Right Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>9</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>10</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>11</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>12</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>13</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>14</td>
    <td rowspan="9">cardMedia specific</td>
    <td></td>
    <td rowspan="9">cardMedia specific</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>15</td>
    <td rowspan="2">1st text row</td>
    <td>title</td>
    <td></td>
  </tr>
  <tr>
    <td>16</td>
    <td>titleColor</td>
    <td></td>
  </tr>
  <tr>
    <td>17</td>
    <td rowspan="2">2nd text row</td>
    <td>author</td>
    <td></td>
  </tr>
  <tr>
    <td>18</td>
    <td>authorColor</td>
    <td></td>
  </tr>
  <tr>
    <td>19</td>
    <td>slider</td>
    <td>volume</td>
    <td>0-100</td>
  </tr>
  <tr>
    <td>20</td>
    <td>icon middle</td>
    <td>playPauseIcon</td>
    <td></td>
  </tr>
  <tr>
    <td>21</td>
    <td>icon right side</td>
    <td>onOffBtn</td>
    <td>"disable" or color</td>
  </tr>
  <tr>
    <td>22</td>
    <td>icon left side</td>
    <td>iconShuffle</td>
    <td>"disable" or icon</td>
  </tr>
  <tr>
    <td>23</td>
    <td rowspan="36">Entities</td>
    <td rowspan="6">upper left corner media&nbsp;&nbsp;&nbsp;icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>24</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>25</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>26</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>27</td>
    <td>displayName</td>
    <td>only used for popups</td>
  </tr>
  <tr>
    <td>28</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>29</td>
    <td rowspan="6">First Entity</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>30</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>31</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>32</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>33</td>
    <td>displayName</td>
    <td>only used for popups</td>
  </tr>
  <tr>
    <td>34</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>35</td>
    <td rowspan="6">Second Entity</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>36</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>37</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>38</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>39</td>
    <td>displayName</td>
    <td>only used for popups</td>
  </tr>
  <tr>
    <td>40</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>41</td>
    <td rowspan="6">Thrid Entity</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>42</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>43</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>44</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>45</td>
    <td>displayName</td>
    <td>only used for popups</td>
  </tr>
  <tr>
    <td>46</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>47</td>
    <td rowspan="6">Forth Entiry</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>48</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>49</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>50</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>51</td>
    <td>displayName</td>
    <td>only used for popups</td>
  </tr>
  <tr>
    <td>52</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>53</td>
    <td rowspan="6">Fifth Entiy</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>54</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>55</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>56</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>57</td>
    <td>displayName</td>
    <td>only used for popups</td>
  </tr>
  <tr>
    <td>58</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
</tbody>
</table>

### cardThermo

Serial Protocol of cardThermo is about to change; table will be completed later

<table>
<thead>
  <tr>
    <th>Parameter&nbsp;&nbsp;&nbsp;Number</th>
    <th>Category</th>
    <th>Location</th>
    <th>Type</th>
    <th>Field</th>
    <th>Addional Information</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td>instruction</td>
    <td></td>
    <td>instruction</td>
    <td>entityUpd</td>
    <td></td>
  </tr>
  <tr>
    <td>1</td>
    <td>title</td>
    <td>title</td>
    <td>title</td>
    <td>title</td>
    <td></td>
  </tr>
  <tr>
    <td>2</td>
    <td rowspan="12">Navigation</td>
    <td rowspan="6">Upper Left Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>3</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>4</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>5</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>6</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>7</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>8</td>
    <td rowspan="6">Upper Right Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>9</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>10</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>11</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>12</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>13</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>14</td>
    <td rowspan="7">cardThermo specific</td>
    <td></td>
    <td rowspan="7">cardThermo specific</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>15</td>
    <td rowspan="2"></td>
    <td>currentTemp</td>
    <td></td>
  </tr>
  <tr>
    <td>16</td>
    <td>dstTemp</td>
    <td>current temp; multiplied by 10</td>
  </tr>
  <tr>
    <td>17</td>
    <td rowspan="2">4th Text Box Left Side</td>
    <td>status</td>
    <td></td>
  </tr>
  <tr>
    <td>18</td>
    <td>minTemp</td>
    <td>min temp; multiplied by 10</td>
  </tr>
  <tr>
    <td>19</td>
    <td></td>
    <td>maxTemp</td>
    <td>max temp; multiplied by 10</td>
  </tr>
  <tr>
    <td>20</td>
    <td></td>
    <td>tempStep</td>
    <td>temp adj per step; multiplied by 10</td>
  </tr>
  <tr>
    <td>21</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>22</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>23</td>
    <td rowspan="36"></td>
    <td rowspan="6"></td>
    <td rowspan="6"></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>24</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>25</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>26</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>27</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>28</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>29</td>
    <td rowspan="6"></td>
    <td rowspan="6"></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>30</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>31</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>32</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>33</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>34</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>35</td>
    <td rowspan="6"></td>
    <td rowspan="6"></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>36</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>37</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>38</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>39</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>40</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>41</td>
    <td rowspan="6"></td>
    <td rowspan="6"></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>42</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>43</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>44</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>45</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>46</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>47</td>
    <td rowspan="6"></td>
    <td rowspan="6"></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>48</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>49</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>50</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>51</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>52</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>53</td>
    <td rowspan="6"></td>
    <td rowspan="6"></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>54</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>55</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>56</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>57</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>58</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>59</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>60</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>61</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>62</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>63</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>64</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>65</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>66</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>67</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>68</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>69</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>70</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>71</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>72</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>73</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
</tbody>
</table>

### cardAlarm

<table>
<thead>
  <tr>
    <th>Parameter&nbsp;&nbsp;&nbsp;Number</th>
    <th>Category</th>
    <th>Location</th>
    <th>Type</th>
    <th>Field</th>
    <th>Addional Information</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td>instruction</td>
    <td></td>
    <td>instruction</td>
    <td>entityUpd</td>
    <td></td>
  </tr>
  <tr>
    <td>1</td>
    <td>title</td>
    <td>title</td>
    <td>title</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>2</td>
    <td rowspan="12">Navigation</td>
    <td rowspan="6">Upper Left Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>3</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>4</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>5</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>6</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>7</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>8</td>
    <td rowspan="6">Upper Right Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>9</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>10</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>11</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>12</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>13</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>14</td>
    <td rowspan="15">cardAlarm specific</td>
    <td colspan="2" rowspan="2">1st button&nbsp;&nbsp;&nbsp;right side</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>15</td>
    <td>intId</td>
    <td></td>
  </tr>
  <tr>
    <td>16</td>
    <td colspan="2" rowspan="2">2nd button&nbsp;&nbsp;&nbsp;right side</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>17</td>
    <td>intId</td>
    <td></td>
  </tr>
  <tr>
    <td>18</td>
    <td colspan="2" rowspan="2">3rd button&nbsp;&nbsp;&nbsp;right side</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>19</td>
    <td>intId</td>
    <td></td>
  </tr>
  <tr>
    <td>20</td>
    <td colspan="2" rowspan="2">4th button&nbsp;&nbsp;&nbsp;right side</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>21</td>
    <td>intId</td>
    <td></td>
  </tr>
  <tr>
    <td>22</td>
    <td colspan="2" rowspan="2">icon next to code display</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>23</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>24</td>
    <td colspan="2">numpad</td>
    <td>numpadStatus</td>
    <td>"disable" or "enable"</td>
  </tr>
  <tr>
    <td>25</td>
    <td colspan="2">flashing of icon next to code</td>
    <td>flashing status</td>
    <td>"enable" or "disable"</td>
  </tr>
  <tr>
    <td>26</td>
    <td colspan="2" rowspan="3">button bottom left corner</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>27</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>28</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
</tbody>
</table>

### cardQR

Example: `entityUpd~Guest Wifi~button~navigate.prev~<~65535~~~button~navigate.next~>~65535~~~WIFI:S:test_ssid;T:WPA;P:test_pw;;~text~iText.test_ssid~���~17299~Name~test_ssid~text~iText.test_pw~���~17299~Password~test_pw`

<table>
<thead>
  <tr>
    <th>Parameter&nbsp;&nbsp;&nbsp;Number</th>
    <th>Category</th>
    <th>Location</th>
    <th>Type</th>
    <th>Field</th>
    <th>Addional Information</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td>instruction</td>
    <td></td>
    <td>instruction</td>
    <td>entityUpd</td>
    <td></td>
  </tr>
  <tr>
    <td>1</td>
    <td>title</td>
    <td>title</td>
    <td>title</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>2</td>
    <td rowspan="12">Navigation</td>
    <td rowspan="6">Upper Left Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>3</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>4</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>5</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>6</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>7</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>8</td>
    <td rowspan="6">Upper Right Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>9</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>10</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>11</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>12</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>13</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>14</td>
    <td colspan="3">cardQR specific</td>
    <td>qrcode text</td>
    <td></td>
  </tr>
  <tr>
    <td>15</td>
    <td rowspan="12">Entities</td>
    <td rowspan="6">1st Entity</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>16</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>17</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>18</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>19</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>20</td>
    <td>optionalValue</td>
    <td></td>
  </tr>
  <tr>
    <td>21</td>
    <td rowspan="6">2nd Entity</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td></td>
  </tr>
  <tr>
    <td>22</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>23</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>24</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>25</td>
    <td>displayName</td>
    <td></td>
  </tr>
  <tr>
    <td>26</td>
    <td>optionalValue</td>
    <td></td>
  </tr>
</tbody>
</table>


### cardPower (in development)

<table>
<thead>
  <tr>
    <th>Parameter&nbsp;&nbsp;&nbsp;Number</th>
    <th>Category</th>
    <th>Location</th>
    <th>Type</th>
    <th>Field</th>
    <th>Addional Information</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td>instruction</td>
    <td></td>
    <td>instruction</td>
    <td>entityUpd</td>
    <td></td>
  </tr>
  <tr>
    <td>1</td>
    <td>title</td>
    <td>title</td>
    <td>title</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>2</td>
    <td rowspan="12">Navigation</td>
    <td rowspan="6">Upper Left Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>3</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>4</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>5</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>6</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>7</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>8</td>
    <td rowspan="6">Upper Right Icon</td>
    <td rowspan="6">Entity Definition</td>
    <td>type</td>
    <td>(ignored)¹</td>
  </tr>
  <tr>
    <td>9</td>
    <td>intNameEntity</td>
    <td></td>
  </tr>
  <tr>
    <td>10</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>11</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>12</td>
    <td>displayName</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>13</td>
    <td>optionalValue</td>
    <td>ignored</td>
  </tr>
  <tr>
    <td>14</td>
    <td rowspan="27">cardPower specific</td>
    <td rowspan="3">Home Icon Middle</td>
    <td></td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>15</td>
    <td></td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>16</td>
    <td></td>
    <td>text</td>
    <td></td>
  </tr>
  <tr>
    <td>17</td>
    <td rowspan="4">1st Item Upper Left</td>
    <td rowspan="4">Power Entity Definition</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>18</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>19</td>
    <td>speed</td>
    <td>numbers (-2,-1,0,1,2)</td>
  </tr>
  <tr>
    <td>20</td>
    <td>text</td>
    <td></td>
  </tr>
  <tr>
    <td>21</td>
    <td rowspan="4">2nd Item Middle Left</td>
    <td rowspan="4">Power Entity Definition</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>22</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>23</td>
    <td>speed</td>
    <td>numbers (-2,-1,0,1,2)</td>
  </tr>
  <tr>
    <td>24</td>
    <td>text</td>
    <td></td>
  </tr>
  <tr>
    <td>25</td>
    <td rowspan="4">3rd Item Bottom Left</td>
    <td rowspan="4">Power Entity Definition</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>26</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>27</td>
    <td>speed</td>
    <td>numbers (-2,-1,0,1,2)</td>
  </tr>
  <tr>
    <td>28</td>
    <td>text</td>
    <td></td>
  </tr>
  <tr>
    <td>29</td>
    <td rowspan="4">4th Item Upper Right</td>
    <td rowspan="4">Power Entity Definition</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>30</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>31</td>
    <td>speed</td>
    <td>numbers (-2,-1,0,1,2)</td>
  </tr>
  <tr>
    <td>32</td>
    <td>text</td>
    <td></td>
  </tr>
  <tr>
    <td>33</td>
    <td rowspan="4">5thItem Middle Right</td>
    <td rowspan="4">Power Entity Definition</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>34</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>35</td>
    <td>speed</td>
    <td>numbers (-2,-1,0,1,2)</td>
  </tr>
  <tr>
    <td>36</td>
    <td>text</td>
    <td></td>
  </tr>
  <tr>
    <td>37</td>
    <td rowspan="4">6th Item Bottom Right</td>
    <td rowspan="4">Power Entity Definition</td>
    <td>iconColor</td>
    <td></td>
  </tr>
  <tr>
    <td>38</td>
    <td>icon</td>
    <td></td>
  </tr>
  <tr>
    <td>39</td>
    <td>speed</td>
    <td>numbers (-2,-1,0,1,2)</td>
  </tr>
  <tr>
    <td>40</td>
    <td>text</td>
    <td></td>
  </tr>
</tbody>
</table>

### cardChart Page
`entityUpd~heading~navigation~color~yAxisLabel~yAxisTick:[yAxisTick]*[~value[:xAxisLabel]?]*`  

`entityUpd~Chart Demo~1|1~6666~Gas [kWh]~20:40:60:80:100~10~7^2:00~7~6^4:00~6~7^6:00~0~7^8:00~5~1^10:00~1~10^12:00~5~6^14:00~8`


## Messages from Nextion Display

`event,buttonPress2,pageName,bNext`

`event,buttonPress2,pageName,bPrev`

`event,buttonPress2,pageName,bExit,number_of_taps`

`event,buttonPress2,pageName,sleepReached`


### startup page

`event,startup,version,model`

### screensaver page

`event,buttonPress2,screensaver,exit` - Touch Event on Screensaver

`event,screensaverOpen` - Screensaver has opened


### cardEntities Page

`event,*eventName*,*entityName*,*actionName*,*optionalValue*`

`event,buttonPress2,internalNameEntity,up`

`event,buttonPress2,internalNameEntity,down`

`event,buttonPress2,internalNameEntity,stop`

`event,buttonPress2,internalNameEntity,OnOff,1`

`event,buttonPress2,internalNameEntity,button`

### popupLight Page

`event,pageOpenDetail,popupLight,internalNameEntity`

`event,buttonPress2,internalNameEntity,OnOff,1`

`event,buttonPress2,internalNameEntity,brightnessSlider,50`

`event,buttonPress2,internalNameEntity,colorTempSlider,50`

`event,buttonPress2,internalNameEntity,colorWheel,x|y|wh`

### popupShutter Page

`event,pageOpenDetail,popupShutter,internalNameEntity`

`event,buttonPress2,internalNameEntity,positionSlider,50`

### popupNotify Page

`event,buttonPress2,*internalName*,notifyAction,yes`

`event,buttonPress2,*internalName*,notifyAction,no`

### cardThermo Page

`event,buttonPress2,*entityName*,tempUpd,*temperature*`

`event,buttonPress2,*entityName*,hvac_action,*hvac_action*`

### cardMedia Page

`event,buttonPress2,internalNameEntity,media-back`

`event,buttonPress2,internalNameEntity,media-pause`

`event,buttonPress2,internalNameEntity,media-next`

`event,buttonPress2,internalNameEntity,volumeSlider,75`

### cardAlarm Page

`event,buttonPress2,internalNameEntity,actionName,code`


# Custom Protocol

```
55 BB [payload length] [payload length] [payload] [crc] [crc]
```

Payload length contains the number of bytes of the payload.

CRC is "CRC-16 (MODBUS) Big Endian" calculated over the whole message

This protocol does not try to implement broken JSON Commands with a specified type (lol).
Instead the commands are plain text commands with parameters.

## Example for valid Message

This message has to be generated for the Message "1337" (1337 is not a valid command~ this is just an example)

```
55 BB  04 00  31 33 33 37  5F 5B
```
