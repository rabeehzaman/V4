/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { StockTransferPopup } from "@pw_pos_stock_transfer/input_popups/StockTransferPopup";


export class TransferButton extends Component {
    static template = "pw_pos_stock_transfer.TransferButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
        this.orm = useService("orm");
    }
    async click() {
        const order = this.pos.get_order();
        const orderLines = order.get_orderlines();
        if (orderLines.length === 0) {
            await this.popup.add(ErrorPopup, {
                title: _t('Empty Order'),
                body: _t('Please add some products'),
            });
        } else {
            if (!this.pos.db.pos_shops){
                const result = await this.orm.call("pos.config", "get_transfer_shop", [this.pos.config.id]);
                this.pos.db.pos_shops = result;
            }
            this.popup.add(StockTransferPopup, {pos_configs: this.pos.db.pos_shops, pw_is_done: this.pos.config.pw_is_done});
        }
    }
}

ProductScreen.addControlButton({
    component: TransferButton,
    condition: function () {
        return this.pos.config.pw_enable_transfer;
    },
});
