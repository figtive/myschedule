import { Calendar } from '@fullcalendar/core';
import timeGridPlugin from '@fullcalendar/timegrid';

var $ = require("jquery")

var calendar;

$(document).ready(function() {
  var calendarEl = document.getElementById('calendar');

  calendar = new Calendar(calendarEl, {
    plugins: [ timeGridPlugin ],
    defaultView: 'timeGridWeek',
    allDaySlot: false,
    slotDuration: '00:30:00', // each time row is 30 min
    minTime: '08:00:00', // start from 8.00
    maxTime: '18:00:00', // end in 18.00
    height: 'auto',
    nowIndicator: false,
    header: { // display empty header
      left: '',
      center: '',
      right: ''
    },
    slotLabelFormat: { // format time as HH:MM
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    },
    columnHeaderFormat: { // display Monday, .. as column header
      weekday: 'long' 
    },
    hiddenDays: [ 0 ], // hide sunday
    firstDay: 1 // show monday first
  });

  calendar.render();
});

// get calendar variable, used in other js files
export function getCalendar(){
  return calendar;
}