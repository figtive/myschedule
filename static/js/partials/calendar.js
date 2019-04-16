import { Calendar } from '@fullcalendar/core';
import timeGridPlugin from '@fullcalendar/timegrid';

var $ = require("jquery")

$(document).ready(function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new Calendar(calendarEl, {
    plugins: [ timeGridPlugin ],
    defaultView: 'timeGridWeek',
    allDaySlot: false,
    slotDuration: '00:30:00',
    minTime: '08:00:00',
    maxTime: '19:00:00',
    height: 'auto',
    nowIndicator: false,
    header: {
      left: '',
      center: '',
      right: ''
    },
    slotLabelFormat: {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    },
    columnHeaderFormat: { 
      weekday: 'long' 
    }
  });

  calendar.render();
});

export function getCalendar(){
  return calendar;
}