/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    // @Override
    async _processData(loadedData) {
        await super._processData(...arguments);
        if (this.config.pw_enable_transfer) {
            this.loadTransferShops();
        }
    },
    async loadTransferShops() {
        const result = await this.orm.call("pos.config", "get_transfer_shop", [this.config.id]);
        this.db.pos_shops = result;
    }
});
