# jQuery iCalendar

Version: 1.0.0

Author: Yubaraj Rai

# Features
- jQuery + JavaScript
- Readable Script
- Basic Calendar


# Uses


  ```
  <!-- Include jQuery Library -->
   <script src="https://code.jquery.com/jquery-2.2.4.min.js"
            integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44=" crossorigin="anonymous"></script>
            
            
  <!-- Include iCalendar CSS File -->
    <link rel="stylesheet" href="./javascript-calendar.css" type="text/css">

  <!-- Structure Textarea -->
  <div class="icalendar">
    <div class="icalendar__month">
        <div class="icalendar__prev" onclick="moveDate('prev')">
            <span>&#10094</span>
        </div>
        <div class="icalendar__current-date">
            <h2 id="icalendarMonth"></h2>
            <div>
                <div id="icalendarDateStr"></div>
            </div>

        </div>
        <div class="icalendar__next" onclick="moveDate('next')">
            <span>&#10095</span>
        </div>
    </div>
    <div class="icalendar__week-days">
        <div>Sun</div>
        <div>Mon</div>
        <div>Tue</div>
        <div>Wed</div>
        <div>Thu</div>
        <div>Fri</div>
        <div>Sat</div>
    </div>
    <div class="icalendar__days"></div>


    <script src="./javascript-calendar.js" type="text/javascript"></script>
</div>

  <!-- Include iCalendar JavaScript File -->
  <script src="./javascript-calendar.js" type="text/javascript"></script>
  ```

Enjoy :)

# View Example
https://codepen.io/yubaraj/pen/ZEGdgYv
