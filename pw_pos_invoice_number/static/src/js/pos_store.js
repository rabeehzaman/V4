/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    // @Override
    async _flush_orders(orders, options) {
        var self = this;
        var result = await super._flush_orders(...arguments);
        if (Array.isArray(result)) {
            result.forEach((order) => {
                this.get_order().invoice_number = order.invoice_number;
            });
        }
        return result
    }
});

patch(Order.prototype, {
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        if(this.invoice_number){
            result['headerData']['invoice_number'] = this.invoice_number;
        }
        return result;
    },
});
