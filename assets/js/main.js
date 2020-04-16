

//  (function($) {
//
//  $('#activity_level').parent().append('<ul class="list-item" id="newactivity_level" name="activity_level"></ul>');
//  $('#activity_level option').each(function(){
//      $('#newactivity_level').append('<li value="' + $(this).val() + '">'+$(this).text()+'</li>');
//  });
//  $('#activity_level').remove();
//  $('#newactivity_level').attr('id', 'activity_level');
//  $('#activity_level li').first().addClass('init');
//  $("#activity_level").on("click", ".init", function() {
//      $(this).closest("#activity_level").children('li:not(.init)').toggle();
//  });
//
//  var allOptions = $("#activity_level").children('li:not(.init)');
//  $("#activity_level").on("click", "li:not(.init)", function() {
//      allOptions.removeClass('selected');
//      $(this).addClass('selected');
//      $("#activity_level").children('.init').html($(this).html());
//      allOptions.toggle();
//  });

//  var marginSlider = document.getElementById('slider-margin');
//  if (marginSlider != undefined) {
//      noUiSlider.create(marginSlider, {
//            start: [50],
//            step: 50,
//            connect: [true, false],
//            tooltips: [true],
//            range: {
//                'min': 0,
//                'max': 100
//            },
//            format: {
//                decimals: 0,
//                thousand: ',',
//                prefix: 'WEIGHT ',
//            }
//    });
//  }
  $('#reset').on('click', function(){
      $('#register-form').reset();
  });

  $('#register-form').validate({
    rules : {
        name : {
            required: true,
        },
        age : {
            required: true,
        },
        food : {
            required: true
        },
        feet : {
            required: true,
        },
        inches : {
            required: true,
        },
        weight : {
            required: true,
        }

    },
    onfocusout: function(element) {
        $(element).valid();
    },
});

    jQuery.extend(jQuery.validator.messages, {
        required: "",
        remote: "",
        email: "",
        url: "",
        date: "",
        dateISO: "",
        number: "",
        digits: "",
        creditcard: "",
        equalTo: ""
    });
})(jQuery);

