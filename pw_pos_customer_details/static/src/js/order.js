/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result['headerData']['partner'] = this.get_partner();
        return result;
    },
});
