let loading = '<div class="loader"></div>';
let modal_loading = '<div class="modal-dialog modal-dialog-centered"><div class="modal-content"><div class="modal-body"><div class="loader"></div></div></div></div>';
$(document).on('click', '.order-button', function () {
    $.ajax({
        beforeSend: function () {
            $('#modal').html(modal_loading);
            $('#modal').modal('show');
        },
        url: $(this).attr('data-url'),
        data: {'usr_addr': web3.eth.defaultAccount},
        success: function (result) {
            result = jQuery.parseHTML(result);
            addr = $(result).find('#id_usr_addr');
            $(addr).val(web3.eth.defaultAccount);
            $(addr).prop('readonly', true);
            $('#modal').html(result);
        },
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
            sell = jQuery.parseHTML(result.sell);
            $(sell).find('div.assetname[data-wallet!=' + web3.eth.defaultAccount + ']').find('a').hide();
            $('#sell_orders_table').html(sell);

            buy = jQuery.parseHTML(result.buy);
            $(buy).find('div.assetname[data-wallet!=' + web3.eth.defaultAccount + ']').find('a').hide();
            $('#buy_orders_table').html(buy);
        }
    })
});


$(document).on('click', 'button.save', function () {
    $('#item_create_form').submit();
});

$(document).on('submit', '#item_create_form', function (event) {
    event.preventDefault();
    $.ajax({
        beforeSend: function (xhr, settings) {
            $('#modal').html(modal_loading);
        },
        url: $(this).attr('action'),
        data: $('#item_create_form').serialize(),
        type : "POST",
        success: function (result) {
            if (result.result === 'error') {
                result = jQuery.parseHTML(result.html);
                addr = $(result).find('#id_usr_addr');
                $(addr).val(web3.eth.defaultAccount);
                $(addr).prop('readonly', true);
                $('#modal').html(result);
            }else{
                window.location.replace(result.url)
            }

        },
    });
});


$(document).ready(function () {
    $('div.assetname[data-wallet!=' + web3.eth.defaultAccount + ']').find('a').hide();
});