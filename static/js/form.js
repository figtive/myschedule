import { addEventsToCalendar } from './add-event';
import { getCalendar } from './calendar';

var $ = require("jquery");

$(document).ready(function() {
  var selectedCourseCount = 0;

  $("form#course-form label").click(function() {
    var clickedCourseCode = $(this).attr('for');
    var associatedInput = $("form#course-form").find(`input[data-course-code=${clickedCourseCode}]`);
    associatedInput.prop('checked', !associatedInput.prop('checked')).eq(0).change();
  });

  $('#unselect-all').click(function() {
    $("input:checkbox").prop('checked', false);
    $(".selected-courses").text('');
    selectedCourseCount = 0
    $('#selected-course-count').text(selectedCourseCount);
  })

  $("input:checkbox").change(function() {
    var courseName = $(this).attr("data-course-name")
    if($(this).prop('checked') && $(`.selected-courses:contains(${courseName})`).length==0 ) {
      updateSelectedCourseCountCounter(true)
      $(".selected-courses").prepend(`<div class="card padding-small">${courseName}</div>`)
    } else if (!$(this).prop('checked')) {
      updateSelectedCourseCountCounter(false)
      $(".selected-courses").find(`div:contains(${courseName})`).eq(0).remove()
    }
  })

  function updateSelectedCourseCountCounter(increment = true) {
    if (increment)
      selectedCourseCount++;
    else if (!increment && selectedCourseCount >= 1)
      selectedCourseCount--;
    $('#selected-course-count').text(selectedCourseCount);
  }

  $('form#course-form').on("submit", function(event) {
    event.preventDefault();
    $("html, body").animate({ scrollTop: $('.navbar').height() }, "slow");
    getCalendar().removeAllEvents();
    clearSelectedClass();

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
        if (!result.data.solution_found) {
          notifyFailure()
          return
        }
        notifySuccess()
        addEventsToCalendar(result)
        var contentAdded = '';
        var i, courseInfo, classInfo;
        for (var i in result.data.result) {
          courseInfo = result.data.result[i].course.course_name
          classInfo = result.data.result[i].class.name
          contentAdded += 
          `<div class="card">
            <div class="card-content padding-small">
              <strong>${courseInfo}</strong><br>
              ${classInfo}
            </div>
          </div>`
        }

        $(".selected-classes").html(contentAdded)
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

function clearSelectedClass() {
  $(".selected-classes").html('')
}

function notifySuccess() {
  const successAlertBox = $(`
    <div class="alert-box success">
      <div style="display: flex;">
        <div style="height: 50px; width: 50px; display: inline-block">
          <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 130.2 130.2">
            <circle class="path circle" fill="none" stroke="#303030" stroke-width="6" stroke-miterlimit="10" cx="65.1" cy="65.1" r="62.1"/>
            <polyline class="path check" fill="none" stroke="#303030" stroke-width="6" stroke-linecap="round" stroke-miterlimit="10" points="100.2,40.2 51.5,88.8 29.8,67.5 "/>
          </svg>
        </div>
        <span class="text">schedule found!</span>
      </div>
    </div>
  `)
  $(".alerts").prepend(successAlertBox);
  successAlertBox.fadeIn( 300 ).delay( 1500 ).fadeOut( 400, function() {
    $(this).remove();
  })
}

function notifyFailure() {
  const failureAlertBox = $(`
    <div class="alert-box failure">
      <div style="display: flex;">
        <div style="height: 50px; width: 50px; display: inline-block">
          <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 130.2 130.2">
            <circle class="path circle" fill="none" stroke="#303030" stroke-width="6" stroke-miterlimit="10" cx="65.1" cy="65.1" r="62.1"/>
            <line class="path line" fill="none" stroke="#303030" stroke-width="6" stroke-linecap="round" stroke-miterlimit="10" x1="34.4" y1="37.9" x2="95.8" y2="92.3"/>
            <line class="path line" fill="none" stroke="#303030" stroke-width="6" stroke-linecap="round" stroke-miterlimit="10" x1="95.8" y1="38" x2="34.4" y2="92.2"/>
          </svg>
        </div>
        <span class="text">no possible schedule</span>
      </div>
    </div>
  `)
  $(".alerts").prepend(failureAlertBox);
  failureAlertBox.fadeIn( 300 ).delay( 1500 ).fadeOut( 400, function() {
    $(this).remove();
  })
}