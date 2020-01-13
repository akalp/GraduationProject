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
            let addr = $(result).find('#id_usr_addr');
            $(addr).val(web3.eth.defaultAccount);
            $(addr).prop('readonly', true);

            let quantity = $(result).find('#id_quantity');
            $(quantity).parent().hide();

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
    const contract_id = $('#id_obj').find('option:selected').attr('contract_id');
    if ($('#item_create_form').attr('data-table-from') === "sell") {
        erc1155.allowance(web3.eth.defaultAccount, "0x87767eca58362c54cef3dFDBf3Dcd4541bCb4dFC", contract_id, (err, res) => {
            erc1155.approve("0x87767eca58362c54cef3dFDBf3Dcd4541bCb4dFC", $('#id_obj').find('option:selected').attr('contract_id'), res.toString(), $('#id_quantity').val(), (err, res) => {
                if (err) {
                    alert("You have to allow one of the spender in the list.");
                } else {
                    ajaxCall();
                }
            })
        });
    } else {
        erc1155.allowance(web3.eth.defaultAccount, "0x87767eca58362c54cef3dFDBf3Dcd4541bCb4dFC", "0", (err, res) => {
            console.log(res.toString())
            if(!err) {
                erc1155.transferEthToContract("0x87767eca58362c54cef3dFDBf3Dcd4541bCb4dFC", res.toString(), {'value': web3.toWei($('#id_value').val(), 'ether')}, (err, res) => {
                    if (err) {
                        alert("You have to allow one of the spender in the list.");
                    } else {
                        ajaxCall();
                    }
                })
            }else{
                alert(123)
            }
        });
    }
});

function ajaxCall() {
    $.ajax({
        beforeSend: function (xhr, settings) {
            $('#modal').html(modal_loading);
        },
        url: $('#item_create_form').attr('action'),
        data: $('#item_create_form').serialize(),
        type: "POST",
        success: function (result) {
            if (result.result === 'error') {
                result = jQuery.parseHTML(result.html);
                addr = $(result).find('#id_usr_addr');
                $(addr).val(web3.eth.defaultAccount);
                $(addr).prop('readonly', true);
                $('#modal').html(result);
            } else {
                window.location.replace(result.url)
            }

        },
    });
}


$(document).ready(function () {
    $('div.assetname[data-wallet!=' + web3.eth.defaultAccount + ']').find('a').hide();
});