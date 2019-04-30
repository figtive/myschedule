[![pipeline status](https://gitlab.com/myschedule/myschedule/badges/master/pipeline.svg)](https://gitlab.com/myschedule/myschedule/commits/master) [![coverage report](https://gitlab.com/myschedule/myschedule/badges/master/coverage.svg)](https://gitlab.com/myschedule/myschedule/commits/master)

# MySchedule

MySchedule is a website to help users to schedule their college subject time table. Users can choose their desired courses from all term. To arrange the schedule, the user just need to choose the courses that they want to take.

## Motivation

Susun Jadwal web app made by Ristek is the only tool to help students decide their class schedule which involves picking a class per course. Deciding which one to take can be tedious, MySchedule allows student to only choose courses and find most optimal non-clasing schedule based on some preferences.

## Methodology

AI concepts and other techniques used

- problem represents CSP with selected courses, all class for that course, non-clashing schedule as variable, value, constraint respectively
- recursive backtracking search until all posibility exhausted to find all possible solution
- most constrained variable, forward checking implemented for efficiency
- fitness function used to sort solutions to get optimal schedule to be displayed in web
- course, class data obtained from web scraping univerity's list of course page

## Tech stack

- django web framework
- bulma css framework
- webpack to bundle js and scss files
- gitlab-ci + heroku CI/CD

## Credits

Inspiration

- Susun Jadwal web app by Ristek
- [python-constraint](https://labix.org/python-constraint)

Members

- Nicolaus Christian Gozali (1706020446)
- Prudence Querida (1606863503)
- Maria Aprillia Devira (1706018920)