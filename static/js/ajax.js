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

            let del_form = $(result).find('#item_delete_form');
            if (del_form.length !== 0) {
                del_form.prop('action', del_form.attr('action') + "?usr_addr=" + web3.eth.defaultAccount)
            }

            $('#modal').html(result);
        },
    })
});

balance = 0
$(document).on('click', '#send-token', function () {
    const modal = $("#modal")
    modal.html(modal_loading);
    modal.modal('show');
    const nf = $(this).parent().data('nf')
    const token_id = $(this).parent().data('contract-id')

    let form = "<div class=\"modal-dialog modal-dialog-centered\" role=\"document\">" +
        "<div class=\"modal-content\">" +
        "<div class=\"modal-header\"><h5 class=\"modal-title\" id=\"exampleModalLongTitle\">Send</h5>" +
        "<button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>" +
        "</div><div class='modal-body' data-contract-id='" + token_id + "'>"

    if (nf === "False") {
        erc1155.methods.balanceOf(web3.eth.defaultAccount, token_id).call().then((res, err) => {
            balance = res
        });
        form += "<label for='quantityTo'>Quantity</label><input class='form-control mb-1' id='quantityTo'/>"
    }

    form +=
        "<label for='addressTo'>Address</label><input type='text' id='addressTo' class='form-control'><button class='btn btn-success float-right mt-2' id='sendIt' disabled>Ok!</button></div></div></div>"

    modal.html(form)
});

b = false
$(document).on('keyup', '#quantityTo', function () {
    let msg = '<div class="invalid-feedback">You have only ' + balance + '!</div>';
    const quantity = $('#quantityTo')
    const address = $('#addressTo')

    if (BigNumber($(quantity).val()).isGreaterThan(balance)) {
        $(quantity).addClass('is-invalid');
        if (!b) {
            $(quantity).after(msg);
            $('#sendIt').prop('disabled', true);
        }
        b = true
    } else {
        $(quantity).removeClass('is-invalid');
        $('#sendIt').prop('disabled', false);
        if (b) {
            $(".invalid-feedback")[0].remove();
        }
        b = false
    }

    if (quantity.val() === "" || address.val() === "") {
        $('#sendIt').prop('disabled', true);
    } else {
        $('#sendIt').prop('disabled', false);
    }
})

$(document).on('keyup', '#addressTo', function () {
    const quantity = $('#quantityTo')
    const address = $('#addressTo')
    if (quantity.val() === "" || address.val() === "") {
        $('#sendIt').prop('disabled', true);
    } else {
        $('#sendIt').prop('disabled', false);
    }
})


$(document).on('click', '#sendIt', function () {
    let quantity = $('#quantityTo')
    if (quantity.val() === undefined){
        quantity = "1"
    }else{
        quantity = quantity.val()
    }
    erc1155.methods.safeTransferFrom(web3.eth.defaultAccount, $('#addressTo').val(), $(this).parent().data('contract-id'), quantity, "0x01").send({from: web3.eth.defaultAccount})
        .on('receipt', receipt => {
            console.log(receipt);
            $('#modal').modal('hide');
            const newbalance = balance - parseInt(quantity)
            if (newbalance > 0) {
                $("div[data-contract-id='" + $(this).parent().data('contract-id') + "'").find('.assetvalue').text()
            }else{
                $("div[data-contract-id='" + $(this).parent().data('contract-id') + "'").remove()
            }

        })
        .on('error', (err, receipt) => {
            console.error(err);
            console.log(receipt);
            $('#modal').modal('hide');
        })
})


$(document).on('click', '.alphabet', function () {
    $.ajax({
        beforeSend: function () {
            $('#game-list').html(loading);
        },
        url: $(this).attr('data-url'),
        success: function (result) {
            result = jQuery.parseHTML(result);
            $(result).find('a[data-url*="/me"]').map(function () {
                $(this).attr('data-url', $(this).attr('data-url') + '?usr_addr=' + web3.eth.defaultAccount)
            });
            $('#game-list').html(result);
        }
    })
});

$(document).on('click', '.game_url', function () {
    $.ajax({
        beforeSend: function () {
            $('#sell_orders_table').html(loading);
            $('#buy_orders_table').html(loading);
            $('#inventory').html(loading);
        },
        url: $(this).attr('data-url'),
        success: function (result) {
            sell = jQuery.parseHTML(result.sell);
            $(sell).find('div.assetname[data-wallet!=' + web3.eth.defaultAccount + ']').find('a').hide();
            $('#sell_orders_table').html(sell);

            buy = jQuery.parseHTML(result.buy);
            $(buy).find('div.assetname[data-wallet!=' + web3.eth.defaultAccount + ']').find('a').hide();
            $('#buy_orders_table').html(buy);

            $('#inventory').html(jQuery.parseHTML(result.inventory));

            userChange();
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
        erc1155.methods.allowance(web3.eth.defaultAccount, "0x87767eca58362c54cef3dFDBf3Dcd4541bCb4dFC", contract_id).call().then(res => {
            erc1155.methods.approve("0x87767eca58362c54cef3dFDBf3Dcd4541bCb4dFC", $('#id_obj').find('option:selected').attr('contract_id'), res.toString(), $('#id_quantity').val()).send({"from": web3.eth.defaultAccount}).then((res, err) => {
                if (!err) {
                    ajaxCall()
                } else {
                    alert("Unexpected error. Please contact HuDeX administration.")
                }
            })
        });
    } else {
        erc1155.methods.allowance(web3.eth.defaultAccount, "0x87767eca58362c54cef3dFDBf3Dcd4541bCb4dFC", "1").call().then(res => {
            erc1155.methods.transferEthToContract("0x87767eca58362c54cef3dFDBf3Dcd4541bCb4dFC", res.toString()).send({
                'from': web3.eth.defaultAccount,
                'value': web3.utils.toWei($('#id_value').val(), 'ether')
            }).then(res => {
                erc1155.methods.balanceOf(web3.eth.defaultAccount, 0).call().then((res, err) => {
                    if (!err) {
                        $('#ETH').text(web3.utils.fromWei(res));
                        ajaxCall()
                    } else {
                        alert("Unexpected error. Please contact HuDeX administration.")
                    }
                })
            })
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
                window.location.href = result.url
            }

        },
    });
}


$(document).ready(function () {
    web3.eth.getAccounts().then(e => {
        web3.eth.defaultAccount = e[0]
        $('div.assetname[data-wallet!=' + web3.eth.defaultAccount + ']').find('a').hide();
        $('a[href*="/me"]').map(function () {
            if (!$(this['href*="?"']))
                $(this).prop('href', $(this).attr('href') + '?usr_addr=' + web3.eth.defaultAccount)
        });
        $('a[data-url*="/me"]').map(function () {
            if (!$(this['data-url*="?"']))
                $(this).attr('data-url', $(this).attr('data-url') + '?usr_addr=' + web3.eth.defaultAccount)
        });
    });
});
