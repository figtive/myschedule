import { getCalendar } from './calendar';
import '@fullcalendar/core';

var $ = require("jquery");

export function addEventToCalendar(event_dict) {
    getCalendar().addEvent(event_dict);
}

export function addEventsToCalendar(solve_api) {
    getCalendar().removeAllEvents();

    $(solve_api['data']['result']).each(function(i, course_to_class) {
        var event_dict = {}
        
        event_dict['title'] = course_to_class['course']['course_name']
        $(course_to_class['class']['meetings']).each(function(j, meeting) {
            switch (meeting['day']) {
                case "Monday":
                event_dict['daysOfWeek'] = [1]
                break;
                case "Tuesday":
                event_dict['daysOfWeek'] = [2]
                break;
                case "Wednesday":
                event_dict['daysOfWeek'] = [3]
                break;
                case "Thursday":
                event_dict['daysOfWeek'] = [4]
                break;
                case "Friday":
                event_dict['daysOfWeek'] = [5]
                break;
                case "Saturday":
                event_dict['daysOfWeek'] = [6]
                break;
            }
            var [hour, minute] = meeting['start_time'].split(".")
            event_dict['startTime'] = `${hour}:${minute}:00`
            var [hour, minute] = meeting['end_time'].split(".")
            event_dict['endTime'] = `${hour}:${minute}:00`

            addEventToCalendar(event_dict)
        })
    })
}