/** @odoo-module */

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { useState } from "@odoo/owl";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { useService } from "@web/core/utils/hooks";
import { useAsyncLockedMethod } from "@point_of_sale/app/utils/hooks";
import { parseFloat } from "@web/views/fields/parsers";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { STCustomMsgPopup } from "@pw_pos_stock_transfer/input_popups/STCustomMsgPopup";


export class StockTransferPopup extends AbstractAwaitablePopup {
    static template = "pw_pos_stock_transfer.StockTransferPopup";
    static defaultProps = {
        cancelText: _t("Cancel"),
        confirmText: _t("Create Transfer"),
        title: _t("Create Internal Transfer"),
        body: "",
        list: [],
        confirmKey: false,
    };
    setup() {
        super.setup();
        this.notification = useService("pos_notification");
        this.popup = useService("popup");
        this.orm = useService("orm");
        this.pos = usePos();
        this.state = useState({
            operation_type: "send",
            pw_shop_id: false,
            transfer_state: 'draft',
        });
        this.confirm = useAsyncLockedMethod(this.confirm);
    }
    async changeOperationType(event) {
        let operation_type = event.target.value;
        if (operation_type === 'send') {
            $('#label_operation').text('Send To: ');
        }
        else {
            $('#label_operation').text('Receive From: ');
        }
    }
    async confirm() {
        if (!this.state.pw_shop_id) {
            $('#pw_transfer_error').show().text('Please select send/receive shop.');
            return;
        }
        var order = this.pos.get_order();
        var orderlines = order.get_orderlines();
        var picking_data = {
            'config_id': this.pos.config.id,
            'session_id': this.pos.config.current_session_id[0],
            'dest_shop_id': parseInt(this.state.pw_shop_id),
            'operation_type': this.state.operation_type,
            'transfer_state': this.state.transfer_state,
            'partner_id': order.partner && order.partner.id,
        };
        var product_ids = [];
        orderlines.forEach(function(line) {
            var pack_lot_ids = [];
            if (line.pack_lot_lines){
                line.pack_lot_lines.forEach(item => {
                    return pack_lot_ids.push({'lot_name': item.lot_name});
                });
            }
            product_ids.push({'product_id': line.product.id, 'uom_id': line.uom_id, 'quantity': line.quantity, 'pack_lot_lines': pack_lot_ids})
        });
        picking_data['lines'] = product_ids
        const output = await this.orm.call("stock.picking", "create_pos_internal_transfer", [picking_data]);
        super.confirm();
        console.log('REF::::::::::::::::', output)
        if (output.result) {
            var orderlines = order.get_orderlines();
            orderlines.filter(line => line.get_product()).forEach(line => order.removeOrderline(line));
            order.set_partner(false);
            this.popup.add(STCustomMsgPopup, {
                title: _t(output.header),
                body: _t(output.body),
            });
        }
        else {
            this.popup.add(ErrorPopup, {
                title: _t(output.header),
                body: _t(output.body),
            });
        }
    }
}
