import { getCalendar } from './calendar';
import '@fullcalendar/core';

var $ = require("jquery");

export function addEventToCalendar(event_dict) {
    getCalendar().addEvent(event_dict);
}

export function addEventsToCalendar(solve_api) {
    getCalendar().removeAllEvents();

    $(solve_api['data']['result']).each(function(i, course_to_class) {
        $(course_to_class['class']['meetings']).each(function(j, meeting) {
            var event_dict = {}
            
            event_dict['title'] = course_to_class['course']['course_name'] + '\n' + meeting['class_room']
            event_dict['daysOfWeek'] = dayStringToArrayOfInt(meeting['day'])
            
            var [hour, minute] = meeting['start_time'].split(".")
            event_dict['startTime'] = `${hour}:${minute}:00`
            var [hour, minute] = meeting['end_time'].split(".")
            event_dict['endTime'] = `${hour}:${minute}:00`

            addEventToCalendar(event_dict)
        })
    })
}

function dayStringToArrayOfInt(dayString) {
    var result;
    switch (dayString) {
        case "Monday":
        result = [1]
        break;
        case "Tuesday":
        result = [2]
        break;
        case "Wednesday":
        result = [3]
        break;
        case "Thursday":
        result = [4]
        break;
        case "Friday":
        result = [5]
        break;
        case "Saturday":
        result = [6]
        break;
    }
    return result;
}