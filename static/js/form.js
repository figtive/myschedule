import { addEventsToCalendar } from './add-event';
import { getCalendar } from './calendar';

var $ = require("jquery");

$(document).ready(function() {
  var selectedCourseCount = 0;

  $(".modal button[aria-label='close']").click(function() {
    $(".modal").removeClass("is-active")
  })

  $('#unselect-all').click(function() {
    $("input:checkbox").prop('checked', false);
    $(".selected-courses").text('');
    selectedCourseCount = 0
    $('#selected-course-count').text(selectedCourseCount);
  })

  $("input:checkbox").change(function() {
    var courseName = $(this).attr("data-course-name")
    if($(this).prop('checked')) {
      updateSelectedCourseCountCounter(true)
      $(".selected-courses").prepend(`<div class="card padding-small">${courseName}</div>`)
    } else {
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
    $("html, body").animate({ scrollTop: 0 }, "slow");
    getCalendar().removeAllEvents();

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
          $('.modal#fail').addClass('is-active')
          return
        }
        $('.modal#success').addClass('is-active')
        addEventsToCalendar(result)
        var contentAdded = '<h2 class="title is-5">selected classes</h2>';
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