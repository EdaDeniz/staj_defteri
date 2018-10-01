var model = {
    // number of total days
    numbOfDays: 15,
    // Defining an array for students names
    students: ['Slappy the Frog', 'Lilly the Lizard', 'Paulrus the Walrus', 'Gregory the Goat', 'Adam the Anaconda','Jack the Ripper'],
    // initializes data if not found
    init: function() {
        if (!localStorage.attendance) {
            console.log('Creating attendance records...');
            function getRandom() {
                return (Math.random() >= 0.5);
            }

            var attendance = {};

            $.each(model.students, function (i) {
                 var name = model.students[i];
                 attendance[name] = []
                 for(var i = 0; i < model.numbOfDays; i++){
                    attendance[name].push(getRandom());
                 }
            });
            localStorage.attendance = JSON.stringify(attendance);
            model.data = localStorage.attendance;
        }
    },
    data: localStorage.attendance,
    changeData: function(json) {
        localStorage.attendance = JSON.stringify(json);
        this.data = localStorage.attendance;
    }
};

var octopus = {
    init: function() {
        model.init();
        view.init();
    },
    getNumbOfDays: function(){
        return model.numbOfDays;
    },
    getStudents: function(){
        return model.students;
    },
    getData: function(){
        return JSON.parse(model.data);
    },
    changeAttendance: function (student, day, val) {
        // console.log('changeAttendance called for ' + student + ', day number: ' + day + ', val to be set ' + val );
        var json = this.getData();
        json[student][day] = val;
        // console.log(json);
        model.changeData(json);
    },
    countMissing: function(student) {
        // console.log('countMissing called for ' + student);
        var countMissing = 0;
        $.each(this.getData()[student], function(i, val) {
            if(!val) {
                countMissing++;
            }
        });
        return countMissing;
    },
    getAttendance: function(student) {
        return this.getData()[student];
    },

};

var view = {
    init: function() {
        this.headRow = $('thead');
        this.tbody = $('tbody');
        this.render();
    },
    render: function() {
        var row = $('<tr></tr>');
        var headerName = $('<th>Student Name</th>');
        headerName.addClass('name-col');
        row.append(headerName);
        for(var i = 0; i < octopus.getNumbOfDays(); i++){
            var th = $('<th>' + (i + 1) + '</th>');
            row.append(th);
        }
        row.append('<th class="missed-col">Days Missed-col</th>');
        this.headRow.html(row);
        $.each(octopus.getStudents(), function(i, val){
            var tr = $('<tr id="' + val +'"></tr>');
            var misstd = $('<td class="missed-col">' + octopus.countMissing(val) + '</td>');
            tr.addClass('student');
            tr.append('<td>' + val + '</td>');
            tr.addClass('name-col');
            for(var i = 0; i < octopus.getNumbOfDays(); i++){
                var td = $('<td></td>');
                td.addClass('attend-col');
                var input = $('<input type="checkbox">');
                td.append(input);
                if(octopus.getAttendance(val)[i]){
                    input.prop('checked', true);
                }
                tr.append(td);
                $(input).on('change', (function (val,i) {

                    return function () {
                                 if($(this).is(':checked')){
                                    // console.log('checked');
                                    octopus.changeAttendance(val, i, true);
                                } else {
                                    // console.log('unchecked');
                                    octopus.changeAttendance(val, i, false);
                                }
                                // console.log(octopus.getAttendance(val));
                                $(misstd).html(octopus.countMissing(val));
                            }
                })(val,i));
            }
            tr.append(misstd);
            view.tbody.append(tr);
        });
    }
};

octopus.init();


/*
 * All this does is create an initial
 * attendance record if one is not found
 * within localStorage.
 */
(function() {
    if (!localStorage.attendance) {
        console.log('Creating attendance records...');
        function getRandom() {
            return (Math.random() >= 0.5);
        }

        var nameColumns = $('tbody .name-col'),
            attendance = {};

        nameColumns.each(function() {
            var name = this.innerText;
            attendance[name] = [];

            for (var i = 0; i <= 11; i++) {
                attendance[name].push(getRandom());
            }
        });

        localStorage.attendance = JSON.stringify(attendance);
    }
}());


/* STUDENT APPLICATION */
$(function() {
    var attendance = JSON.parse(localStorage.attendance),
        $allMissed = $('tbody .missed-col'),
        $allCheckboxes = $('tbody input');

    // Count a student's missed days
    function countMissing() {
        $allMissed.each(function() {
            var studentRow = $(this).parent('tr'),
                dayChecks = $(studentRow).children('td').children('input'),
                numMissed = 0;

            dayChecks.each(function() {
                if (!$(this).prop('checked')) {
                    numMissed++;
                }
            });

            $(this).text(numMissed);
        });
    }

    // Check boxes, based on attendace records
    $.each(attendance, function(name, days) {
        var studentRow = $('tbody .name-col:contains("' + name + '")').parent('tr'),
            dayChecks = $(studentRow).children('.attend-col').children('input');

        dayChecks.each(function(i) {
            $(this).prop('checked', days[i]);
        });
    });

    // When a checkbox is clicked, update localStorage
    $allCheckboxes.on('click', function() {
        var studentRows = $('tbody .student'),
            newAttendance = {};

        studentRows.each(function() {
            var name = $(this).children('.name-col').text(),
                $allCheckboxes = $(this).children('td').children('input');

            newAttendance[name] = [];

            $allCheckboxes.each(function() {
                newAttendance[name].push($(this).prop('checked'));
            });
        });

        countMissing();
        localStorage.attendance = JSON.stringify(newAttendance);
    });

    countMissing();
}());