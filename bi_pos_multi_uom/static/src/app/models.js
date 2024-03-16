/** @odoo-module */

import { Order, Orderline, Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import {
    formatFloat,
    roundDecimals as round_di,
    roundPrecision as round_pr,
    floatIsZero,
} from "@web/core/utils/numbers";

// New orders are now associated with the current table, if any.
patch(Orderline.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.uom_id = this.uom_id || this.product.uom_id[0];
    },
    
    init_from_JSON (json) {
        super.init_from_JSON(...arguments);
        this.uom_id = json.uom_id;
    },
    set_custom_uom_id(uom_id) {
        this.uom_id = uom_id;
    },
    get_custom_uom_id() {
        return this.uom_id;
    },
   
    get_unit() {
        var res = super.get_unit();
        var unit_id = this.uom_id;
        if(!unit_id) {
            return res;
        }
        unit_id = unit_id[0] || unit_id;
        if(!this.pos) {
            return undefined;
        }
        return this.pos.units_by_id[unit_id];
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.uom_id = this.uom_id;
        return json;
    },


});
