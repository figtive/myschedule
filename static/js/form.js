import { addEventsToCalendar } from './add-event';

var $ = require("jquery");

$(document).ready(function() {
  $('form#course-form').on("submit", function(event) {
    event.preventDefault();

    var data = $(this).serializeArray().reduce(function(obj, item) {
      if (item.name === 'check') {
        if (!(item.name in obj)) {
          obj[item.name] = [item.value]
        } else {
          obj[item.name].push(item.value)
        }
      } else { 
        obj[item.name] = item.value
      }
      return obj
    }, {});

    const submitButton = $('button#course-form-submit');
    submitButton.prop('disabled', true);

    $.ajax({
      url: "solve/",
      type: "POST",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify(data),
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", data.csrfmiddlewaretoken)
        }
      },
      success: function(result){
        addEventsToCalendar(result)
      },
      fail: function(xhr, ajaxOptions, thrownError){
        console.log(xhr.status);
        console.log(xhr.responseText);
        console.log(thrownError);
      },
      complete: function(response) {
        setTimeout(function() {
          submitButton.prop('disabled', false);
        }, 200);
      }
    });
  })

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
});