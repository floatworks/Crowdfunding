$(document).ready(function() {
  $('#id_pr_stock_wrap_container').bind('click', function() {
    var user_id = $('#id_pr_user_wrap_container .selectize-control .selectize-input .item').attr('data-value');
    if (typeof(user_id) != "undefined") {
      $.get("/w/profit_select/", {
          'id': user_id,
          'type': 'stock'
        },
        function(data, status) {
          if (data.status == 0) {
            $('#id_pr_stock_wrap_container .selectize-dropdown .selectize-dropdown-content').html('没有相应的认购信息');
          } else if (data.status == 1) {
            var options = '';
            projects = data.projects;
            for (var index in projects) {
              options += "<div data-value=\"" + projects[index].pid + "\" data-selectable=\"\" class=\"option\">" + projects[index].label + "</div>";
            }
            $('#id_pr_stock_wrap_container .selectize-dropdown .selectize-dropdown-content').html(options);
          }
        });
    } else {
      $('#id_pr_stock_wrap_container .selectize-dropdown .selectize-dropdown-content').html('没有相应的认购信息');
    }
  });
  $('#id_pr_bond_wrap_container').bind('click', function() {
    var user_id = $('#id_pr_user_wrap_container .selectize-control .selectize-input .item').attr('data-value');
    if (typeof(user_id) != "undefined") {
      $.get("/w/profit_select/", {
          'id': user_id,
          'type': 'bond'
        },
        function(data, status) {
          if (data.status == 0) {
            $('#id_pr_bond_wrap_container .selectize-dropdown .selectize-dropdown-content').html('没有相应的认购信息');
          } else if (data.status == 1) {
            var options = '';
            projects = data.projects;
            for (var index in projects) {
              options += "<div data-value=\"" + projects[index].pid + "\" data-selectable=\"\" class=\"option\">" + projects[index].label + "</div>";
            }
            $('#id_pr_bond_wrap_container .selectize-dropdown .selectize-dropdown-content').html(options);
          }
        });
    } else {
      $('#id_pr_bond_wrap_container .selectize-dropdown .selectize-dropdown-content').html('没有相应的认购信息');
    }
  });

});