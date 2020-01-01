let loading = '<div class="loader"></div>';
let modal_loading = '<div class="modal-dialog modal-dialog-centered"><div class="modal-content"><div class="modal-body"><div class="loader"></div></div></div></div>';
$(document).on('click', '.order-button', function () {
    $.ajax({
        beforeSend: function () {
            $('#modal').html(modal_loading);
            $('#modal').modal('show');
        },
        url: $(this).attr('data-url'),
        success: function (result) {
            result = jQuery.parseHTML(result);
            addr = $(result).find('#id_usr_addr');
            $(addr).val(web3.eth.defaultAccount);
            $(addr).parent().hide();
            $('#modal').html(result);
        }
    })
});

$(document).on('click', '.alphabet', function () {
    $.ajax({
        beforeSend: function () {
            $('#game-list').html(loading);
        },
        url: $(this).attr('data-url'),
        success: function (result) {
            $('#game-list').html(result);
        }
    })
});

$(document).on('click', '.game_url', function () {
    $.ajax({
        beforeSend: function () {
            $('#sell_orders_table').html(loading);
            $('#buy_orders_table').html(loading);
        },
        url: $(this).attr('data-url'),
        success: function (result) {
            $('#sell_orders_table').html(result.sell);
            $('#buy_orders_table').html(result.buy);
        }
    })
});